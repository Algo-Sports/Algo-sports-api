from fabric.api import local


def isort():
    local("isort .")


def runserver():
    settings = "core.settings.dev"
    local(f"python manage.py migrate --settings={settings}")
    local(f"python manage.py runserver --settings={settings}")


def staging():
    settings = "core.settings.prod"
    local(f"python manage.py migrate --settings={settings}")
    local(f"python manage.py collectstatic --settings={settings}")
    local(f"python manage.py runserver --settings={settings}")


def deploy():
    print("Not implemented")
