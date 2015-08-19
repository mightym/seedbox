from fabric.api import *
from fabric.operations import _prefix_commands, _prefix_env_vars
from fabric.contrib import project


# Host
env.disable_known_hosts = True # always fails for me without this

env.user = 'root'
env.hosts = ['146.01.167.57']
env.proj_repo = 'git@github.com:lincolnloop/seedbox.git'
env.roledefs['static'] = ['root@146.01.167.57', ]

# Where the static files get collected locally. Your STATIC_ROOT setting.
env.local_static_root = '/Users/mark/Developer/seedbox_env/var/static'

# Where the static files should go remotely
env.remote_static_root = '/srv/seedbox_env/var/'

# Paths
env.root = '/srv/seedbox_env'
env.proj_root = env.root + '/src/seedbox'
env.pip_file = env.proj_root + '/requirements.txt'

# ============================================================================
# Git
# ============================================================================

def push(remote=None, branch=None, reqs='no'):
    """Pushes the local git repo to the given remote and branch. Then pulls it
    on the server."""
    remote = remote or 'origin'
    branch = branch or 'master'
    local('git push %s %s' % (remote, branch))
    with cd(env.proj_root):
        ve_run('git pull %s %s' % (remote, branch))
        if reqs == 'yes':
            update_reqs()
        collect()

def switch(branch):
    """Switch the repo branch which the server is using"""
    with cd(env.proj_root):
        ve_run('git checkout %s' % branch)
        collect()
    restart_server()

def version():
    """Show last commit to repo on server"""
    with cd(env.proj_root):
        sshagent_run('git log -1')

def quick():
    push()
    restart_server()

def update(remote=None, branch=None):
    push(remote, branch, reqs='yes')
    migrate()
    # flush()
    deploy_static()
    restart_server()

# ============================================================================
# Server
# ============================================================================

def stop_server():
    ve_run('service seedbox stop')

def start_server():
    ve_run('service seedbox start')

def restart_server():
    ve_run('service seedbox restart')

# def flush():
#     """Flush memcache"""
#     sshagent_run('/etc/init.d/memcached restart')

def update_reqs():
    """Update pip requirements"""
    ve_run('yes w | pip install -r %s' % env.pip_file)

# ============================================================================
# Django
# ============================================================================


@roles('static')
def deploy_static():
    local('npm run postinstall')
    local('./manage.py collectstatic --noinput')
    project.rsync_project(
        remote_dir=env.remote_static_root,
        local_dir=env.local_static_root,
        delete=True,
    )
    require('root')
    sshagent_run('chown -R www-data:www-data %s/var/static/' % (env.root))



def collect():
    manage('collectstatic --noinput')

def migrate():
    # manage('syncdb --noinput')
    manage('migrate --noinput')

# ============================================================================
# SSH funcs
# ============================================================================

def manage(cmd):
    return ve_run('python %s/manage.py %s' % (env.proj_root, cmd))

def ve_run(cmd):
    """
    Helper function.
    Runs a command using the virtualenv environment
    """
    require('root')
    return sshagent_run('source %s/bin/activate; %s' % (env.root, cmd))

def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.
    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )