import json
import subprocess
from pathlib import Path

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from algo_sports.codes.models import UserCode
from algo_sports.games.models import GameMatch, GameRoom
from config import celery_app

from .choices import GameStatus

User = get_user_model()


def init_layser_game(parent, init_game_script) -> dict:
    gameinfo_path = parent / "gameinfo.json"
    with gameinfo_path.open("w", encoding="utf-8") as f:
        init_game = ["node", init_game_script]
        subprocess.run(init_game, stdout=f, check=True)

    with gameinfo_path.open("r", encoding="utf-8") as f:
        gameinfo = json.load(f)
    return gameinfo


def load_data(path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data


@celery_app.task()
def run_match(match_data):
    # 게임 진행중으로 변경
    match = get_object_or_404(GameMatch, pk=match_data.get("gamematch_id"))
    match.set_status(GameStatus.IN_PROGRESS)

    room = get_object_or_404(GameRoom, pk=match_data.get("gameroom_id"))
    competitors = UserCode.objects.filter(id__in=match_data.get("competitor_ids"))
    default_setting = room.gameversion.default_setting

    # match 루트 폴더 생성
    parent = Path(f"match_datas/room_{room.id}/match_{match.id}/")
    parent.mkdir(parents=True, exist_ok=True)

    # 게임 세팅
    init_script = "layser_game/generateGameInfo.js"
    gameinfo = init_layser_game(parent, init_script)
    gameinfo_path = parent / "gameinfo.json"

    # 제출 받은 코드들 저장
    for idx, competitor in enumerate(competitors):
        language = competitor.programming_language

        # main 렌더링
        includes = default_setting["includes"][language.name]
        arguments = default_setting["arguments"][language.name]
        solution = competitor.code
        code_string = str(language.get_main_template(includes, arguments, solution))

        # 코드 파일 생성
        file_name = f"code_{competitor.id}.{language.extension}"
        file_path = parent / file_name
        with file_path.open("w", encoding="utf-8") as f:
            gen_code = ["echo", f"{code_string}"]
            subprocess.run(gen_code, stdout=f, check=True)

    # 결과 저장 리스트
    user_result = [[{"plate": []}] for i in competitors]
    user_final = [[] for i in competitors]

    # 결과 저장 파일 패스 리스트
    user_result_paths = [
        parent / f"history_{competitor.id}.json" for competitor in competitors
    ]
    for path in user_result_paths:
        with path.open("w", encoding="utf-8") as f:
            json.dump(user_result[0], f)

    # 유저 상태
    user_status = [0 for i in competitors]
    winners = [0 for i in competitors]
    end_game = False
    lap = 0

    while not end_game and lap < gameinfo["info"]["maxlap"]:
        lap += 1

        # 실제 코드 실행
        for idx, competitor in enumerate(competitors):
            if user_status == -1:
                continue
            language = competitor.programming_language

            # 실행 변수들
            run_cmd = language.run_cmd
            compile_cmd = language.compile_cmd

            # 파일 정보
            file_name = f"code_{competitor.id}.{language.extension}"
            file_path = parent / file_name

            # 커맨드 생성
            run_code = [
                "./run.sh",
                "-r",
                f"{run_cmd}",
                "-s",
                f"{file_path}",
                "-p1",
                str(gameinfo_path),
                "-p2",
                str(user_result_paths[idx]),
            ]
            if compile_cmd:
                run_code.extend(["-c", f"{compile_cmd}"])
            # print(run_code)

            # 유저 아웃풋
            try:
                output = subprocess.run(
                    run_code,
                    capture_output=True,
                    check=True,
                    text=True,
                )
                print(f"{output.stdout}")
                plate = json.loads(f"{output.stdout}")
                plate_list = [i for i in user_result[idx][lap - 1]["plate"]]
                plate_list.append(plate)

                user_result[idx].append({"plate": plate_list})
                with user_result_paths[idx].open("w", encoding="utf-8") as f:
                    json.dump(user_result[idx], f)

            except UnboundLocalError:
                print(f"Error user! competitor id : {competitor.id}")
                user_status[idx] = -1
                continue

            # 계산 과정
            judge_code = [
                "node",
                "layser_game/gamelogic/gamelogic.js",
                str(gameinfo_path),
                str(user_result_paths[idx]),
                str(lap),
            ]
            try:
                output = subprocess.run(
                    judge_code,
                    capture_output=True,
                    check=True,
                    text=True,
                )
                print(output.stdout)
                data = json.loads(output.stdout)
                user_final[idx].append(data)
            except UnboundLocalError:
                print(f"Error judge! competitor id : {competitor.id}")
                user_status[idx] = -1
                continue

        # 게임이 끝났는지 검사
        for idx, data in enumerate(user_final):
            if user_status[idx] == -1:
                continue
            if len(data[lap - 1]) == len(gameinfo["ball"]):
                user_status[idx] = 1
                end_game = True

    for i, status in enumerate(user_status):
        if status == 1:
            winners.append(i)

    winner = ""
    if winners[0] == 1 and winners[1] == 1:
        winner = "draw"
    elif winners[0] == 1:
        winner = "user1"
        match.winner = competitors[0].user
    else:
        winner = "user2"
        match.winner = competitors[1].user

    match.history = {
        "user1": {
            "me": "user1",
            "winner": winner,
            "lap": lap,
            "gameinfo": gameinfo,
            "user1": {
                "useroutput": user_result[0],
                "userresult": user_final[0],
            },
        },
        "user2": {
            "me": "user2",
            "winner": winner,
            "lap": lap,
            "gameinfo": gameinfo,
            "user2": {
                "useroutput": user_result[1],
                "userresult": user_final[1],
            },
        },
    }
    match.score = 10
    match.save()
    match.set_status(GameStatus.FINISHED)
