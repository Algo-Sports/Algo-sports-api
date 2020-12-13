from fabric.api import env
from fabric.api import local as fabric_local
from fabric.context_managers import shell_env

DEV = "dev"
STAGING = "staging"
PRODUCTION = "production"
USE_DOCKER = "no"

# 사용할 환경
env.target = DEV
env.compose = "local.yml"


# 커스텀 local 메소드
# ----------------------------------------------------------------
def local(string):
    if env.target == STAGING:
        fabric_local(string)
    elif env.target == PRODUCTION:
        fabric_local(string)
    elif env.target == DEV:
        with shell_env(DJANGO_READ_DOT_ENV_FILE="True"):
            fabric_local(string)


# 환경 세팅 커맨드
# ----------------------------------------------------------------
def dev():
    env.target = DEV
    env.compose = "local.yml"


def staging():
    env.target = STAGING
    env.compose = "production.yml"


def prod():
    env.target = PRODUCTION
    env.compose = "production.yml"


# 장고 커맨드
# ----------------------------------------------------------------
def makemessages(locale):
    # locale에 해당하는 번역 파일 생성
    local(f"./manage.py makemessages -i venv -l {locale}")


def runserver():
    local("python manage.py runserver")


def load_languages():
    local(
        "python manage.py loaddata algo_sports/codes/fixtures/programming_language.json"
    )


def shell():
    local("python manage.py shell_plus")


# Celery worker
# ----------------------------------------------------------------
def celery():
    local("celery -A config.celery_app worker -l info")


# Docker 커맨드
# ----------------------------------------------------------------
def build():
    local(f"docker-compose -f {env.compose} build")


def up(app="", option=""):
    local(f"docker-compose -f {env.compose} up {option} {app}")


def down(app="", option=""):
    local(f"docker-compose -f {env.compose} down {option} {app}")
