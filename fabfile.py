import os

from fabric import Connection

GIT_REPO = "https://github.com/Lego-Songbook/legoworship.life.git"

HOST = os.environ.get("LW_HOST")
USER = os.environ.get("LW_USER")
PASSWORD = os.environ.get("LW_PASSWORD")
PORT = os.environ.get("LW_PORT")

SOURCE_FOLDER = "/root/sites/legoworship.life"


def deploy():
    """Automate the deployment process."""

    c = Connection(host=HOST, user=USER, port=PORT, connect_kwargs={
        'password':
            PASSWORD
    })
    c.cd(f'{SOURCE_FOLDER}/apps')
    c.run('git pull')
    c.run('poetry shell')
    c.run('poetry install')
    c.run('python manage.py collectstatic --noinput && python manage.py migrate')
    c.run('systemctl stop gunicorn.socket && systemctl start gunicorn.socket')
    for service in ['gunicorn.service', 'nginx']:
        c.run(f'systemctl reload {service}')
