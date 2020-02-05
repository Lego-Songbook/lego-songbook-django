from invoke import task

SOURCE_FOLDER = "/root/sites/legoworship.life"
SERVICES = ['gunicorn.socket', 'gunicorn.service', 'nginx']


@task
def update(c):
    """Update the files on the server."""

    c.cd(f'{SOURCE_FOLDER}/apps')

    # Stop the services
    for service in SERVICES:
        c.run(f'systemctl stop {service}')

    # Pull from remote
    c.run('git checkout master')
    c.run('git pull')

    # Update server files
    c.run('source $HOME/.poetry/env')
    c.run('poetry shell')
    c.run('poetry install')
    c.run('python manage.py collectstatic --noinput & python manage.py migrate')

    # Restart the services
    for service in SERVICES:
        c.run(f'systemctl start {service}')
