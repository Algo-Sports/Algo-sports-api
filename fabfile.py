from fabric.api import env
from fabric.api import local as fabric_local
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


def local(string):
    if env.target == STAGING:
        fabric_local(string)
    elif env.target == PRODUCTION:
        fabric_local(string)
    elif env.target == DEV:
        with shell_env(DJANGO_READ_DOT_ENV_FILE="True"):
            fabric_local(string)


def build():
    if env.target == DEV:
        local("docker-compose -f local.yml build")
    elif env.target in [STAGING, PRODUCTION]:
        local("docker-compose -f production.yml build")


def runserver():
    if env.target == DEV:
        if env.USE_DOCKER == "yes":
            local("docker-compose -f local.yml up")
        else:
            local("./manage.py migrate")
            local("./manage.py runserver")


def makemessages(locale):
    if locale:
        local(f"./manage.py makemessages -i venv -l {locale}")
    else:
        print("usage: fab makemessages:locale")
