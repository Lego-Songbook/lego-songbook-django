import os

from fabric import Connection, task

GIT_REPO = "https://github.com/Lego-Songbook/legoworship.life.git"

HOST = os.environ.get("LW_HOST")
USER = os.environ.get("LW_USER")
PASSWORD = os.environ.get("LW_PASSWORD")
PORT = os.environ.get("LW_PORT")

SOURCE_FOLDER = "/root/sites/legoworship.life"


@task
def deploy(c):
    """Automate the deployment process."""
    services = ['gunicorn.socket', 'gunicorn.service', 'nginx']

    c = Connection(host=HOST, user=USER, port=PORT, connect_kwargs={
        'password':
            PASSWORD
    })
    c.cd(f'{SOURCE_FOLDER}/apps')
    for service in services:
        c.run(f'systemctl stop {service}')
    c.run('git pull')
    c.run('source $HOME/.poetry/env')
    c.run('poetry shell')
    c.run('poetry install')
    c.run('python manage.py collectstatic --noinput & python manage.py migrate')
    for service in services:
        c.run(f'systemctl start {service}')
