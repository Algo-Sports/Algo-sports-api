from fabric.api import env, local
from fabric.context_managers import shell_env

DEV = "dev"
STAGING = "staging"
PRODUCTION = "production"
USE_DOCKER = "no"

# 사용할 환경
env.target = DEV
env.USE_DOCKER = "no"


def docker():
    env.USE_DOCKER = "yes"


def dev():
    env.target = DEV


def staging():
    env.target = STAGING


def prod():
    env.target = PRODUCTION


def build():
    if env.target == DEV:
        local("docker-compose -f local.yml build")
    elif env.target in [STAGING, PRODUCTION]:
        local("docker-compose -f production.yml build")


def runserver():
    if env.target == DEV:
        if env.USE_DOCKER == "yes":
            local("docker-compose -f local.yml up")
        with shell_env(DJANGO_READ_DOT_ENV_FILE="True"):
            local("./manage.py migrate")
            local("./manage.py runserver")


def makemessages(locale):
    if locale:
        local(f"./manage.py makemessages -i venv -l {locale}")
    else:
        print("usage: fab makemessages:locale")
