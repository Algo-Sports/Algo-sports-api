import subprocess

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from algo_sports.codes.models import UserCode
from algo_sports.games.models import GameMatch, GameRoom
from config import celery_app

User = get_user_model()


@celery_app.task()
def run_match(match_data):
    room = get_object_or_404(GameRoom, pk=match_data.get("gameroom_id"))
    match = get_object_or_404(GameMatch, pk=match_data.get("gamematch_id"))
    competitors = UserCode.objects.filter(id__in=match_data.get("competitor_ids"))
    # print(room, match, competitors)

    for competitor in competitors:
        language = competitor.programming_language

        # 실행 변수들
        run_cmd = language.run_cmd
        compile_cmd = language.compile_cmd

        # 코드 파일 생성
        filename = f"room_{room.id}_match_{match.id}_code_{competitor.id}"
        file = open(filename, "w")
        gen_code = ["echo", f"{competitor.code}"]
        subprocess.run(gen_code, stdout=file, check=True)

        # 커맨드 생성
        run_code = ["./run.sh", "-r", f"{run_cmd}", "-s", f"{filename}"]
        if compile_cmd:
            run_code.extend(["-c", f"{compile_cmd}"])

        # output
        output = subprocess.run(run_code, check=True, capture_output=True)
        print(output)
