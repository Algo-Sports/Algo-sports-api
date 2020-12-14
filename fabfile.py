from fabric.api import env
from fabric.api import local as fabric_local
from fabric.context_managers import shell_env

DEV = "dev"
STAGING = "staging"
PRODUCTION = "production"
USE_DOCKER = "no"

# 사용할 환경
env.target = DEV
env.compose = ["local.yml"]
env.settings = "--settings=config.settings.local"


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
    env.compose = ["local.yml"]
    env.settings = "--settings=config.settings.local"


def staging():
    env.target = STAGING
    env.compose = ["staging.yml"]
    env.settings = "--settings=config.settings.production"


def prod():
    env.target = PRODUCTION
    env.compose = ["staging.yml", "production.yml"]
    env.settings = "--settings=config.settings.production"


# 장고 커맨드
# ----------------------------------------------------------------
def makemessages(locale):
    # locale에 해당하는 번역 파일 생성
    local(f"./manage.py makemessages -i venv -l {locale}")


def runserver():
    local(f"python manage.py runserver {env.settings}")


def load_languages():
    local(
        f"python manage.py loaddata algo_sports/codes/fixtures/programming_language.json {env.settings}"
    )


def shell():
    if "local" in env.settings:
        local(f"python manage.py shell_plus {env.settings}")
    else:
        local(f"python manage.py shell {env.settings}")


# Celery worker
# ----------------------------------------------------------------
def celery():
    local("celery -A config.celery_app worker -l info")


# Docker 커맨드
# ----------------------------------------------------------------
def build():
    cmd = "docker-compose "
    for compose in env.compose:
        cmd += f"-f {compose} "
    cmd += "build"
    local(cmd)


def up(app="", option=""):
    cmd = "docker-compose "
    for compose in env.compose:
        cmd += f"-f {compose} "
    cmd += "up"
    local(f"{cmd} {option} {app}")


def down(app="", option=""):
    cmd = "docker-compose "
    for compose in env.compose:
        cmd += f"-f {compose} "
    cmd += "down"
    local(f"{cmd} {option} {app}")


def push():
    cmd = "docker-compose "
    for compose in env.compose:
        cmd += f"-f {compose} "
    cmd += "push"
    local(cmd)


# Deploy 커맨드
# ----------------------------------------------------------------
def deploy():
    local(
        """
    CONFIG_NAME=algo-config
    PROJECT_NAME=algo-service

    ecs-cli compose \
    --project-name $PROJECT_NAME \
    --file staging.yml \
    --file production.yml \
    --ecs-params ./aws/ecs-params.yml \
    service up \
    --create-log-groups \
    --cluster-config $CONFIG_NAME \
    --container-name nginx \
    --container-port 80 \
    --target-group-arn arn:aws:elasticloadbalancing:ap-northeast-2:648240308375:targetgroup/target/e3086c4f494a30c4 \
    --launch-type EC2
    """
    )
