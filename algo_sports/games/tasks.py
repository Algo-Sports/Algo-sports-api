import subprocess
from pathlib import Path

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from algo_sports.codes.models import UserCode
from algo_sports.games.models import GameMatch, GameRoom
from config import celery_app

from .choices import GameStatus

User = get_user_model()


@celery_app.task()
def run_match(match_data):
    # 게임 진행중으로 변경
    match = get_object_or_404(GameMatch, pk=match_data.get("gamematch_id"))
    match.set_status(GameStatus.IN_PROGRESS)

    room = get_object_or_404(GameRoom, pk=match_data.get("gameroom_id"))
    competitors = UserCode.objects.filter(id__in=match_data.get("competitor_ids"))
    default_setting = room.gameversion.default_setting

    for competitor in competitors:
        language = competitor.programming_language

        # 실행 변수들
        run_cmd = language.run_cmd
        compile_cmd = language.compile_cmd

        # main 렌더링
        includes = default_setting["includes"][language.name]
        arguments = default_setting["arguments"][language.name]
        solution = competitor.code
        code_string = str(language.get_main_template(includes, arguments, solution))

        # 코드 파일 생성
        parent = Path(f"match_datas/room_{room.id}/match_{match.id}/")
        parent.mkdir(parents=True, exist_ok=True)
        file_name = f"code_{competitor.id}"
        file_path = parent / file_name
        with file_path.open("w", encoding="utf-8") as f:
            gen_code = ["echo", f"{code_string}"]
            subprocess.run(gen_code, stdout=f, check=True)

        # 커맨드 생성
        run_code = ["./run.sh", "-r", f"{run_cmd}", "-s", f"{file_path}"]
        if compile_cmd:
            run_code.extend(["-c", f"{compile_cmd}"])

        # output
        output = subprocess.run(run_code, check=True, capture_output=True)
        print(output)
    match.set_status(GameStatus.FINISHED)
