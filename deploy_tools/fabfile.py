import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/john-rigas/sportsweb'  

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  
    run(f'mkdir -p {site_folder}')  
    with cd(site_folder):  
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        _add_cronjobs()

def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}') 

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):  
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt') 

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')  
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')  
    if 'DJANGO_SECRET_KEY' not in current_contents:  
        new_secret = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files():
    run('./virtualenv/bin/python manage.py collectstatic --noinput') 

def _update_database():
    run('./virtualenv/bin/python manage.py migrate --noinput') 

def _add_cronjobs():
    #run('crontab -r')
    #run('crontab -l > /tmp/crondump')
    run('rm /tmp/crondump')             
    run('echo "*/15 * * * * export PATH=$PATH:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:~/sites/fredandfred.tk/virtualenv/lib/python3.6/site-packages/selenium/webdriver/firefox/webdriver.py && DISPLAY=:0 && cd ~/sites/fredandfred.tk  &&  ./virtualenv/bin/python save_schedule.py" >> /tmp/crondump')
    run('echo "*/15 * * * * cd ~/sites/fredandfred.tk && ./virtualenv/bin/python run_updates.py"  >> /tmp/crondump')
    run('echo "0 0 4 9-12 3 cd ~/sites/fredandfred.tk && ./virtualenv/bin/python set_currentweek_cron_emails.py" >> /tmp/crondump')
    run('crontab /tmp/crondump')
