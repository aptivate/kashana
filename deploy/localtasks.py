from dye import tasklib
from dye.tasklib.django import _manage_py, _install_django_jenkins, create_private_settings, link_local_settings, clean_db, update_db, _manage_py_jenkins
from dye.tasklib.environment import env
from dye.tasklib.util import _rm_all_pyc

def build_webassets():
    print "### Build assets"
    _manage_py(['assets', 'clean'])
    _manage_py(['assets', 'build'])

def run_jenkins():
    """ make sure the local settings is correct and the database exists """
    env['verbose'] = True
    # don't want any stray pyc files causing trouble
    _rm_all_pyc()
    _install_django_jenkins()
    create_private_settings()
    link_local_settings('jenkins')
    clean_db()
    update_db()
    build_webassets()
    _manage_py_jenkins()

def collect_static_files():
    """ Collect static files """
    _manage_py(['collectstatic', '--noinput'])


def post_deploy(environment):
    """ This function is called by the main deploy in dye/tasklib after
    all the other tasks are done.  So this is the place where you can
    add any custom tasks that your project requires, such as creating
    directories, setting permissions etc."""
    setup_group_permissions()
    build_webassets()


def setup_group_permissions():
    """
    Programatically create the django.auth Group objects
    we depend on, and allocate them the permissions we
    think they should have .
    """
    print "### Setting up group permissions"
    command = ['setup_group_permissions']
    if tasklib.env['verbose']:
        command.append('--verbosity=2')
    _manage_py(command)
