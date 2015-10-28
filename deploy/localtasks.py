import os
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
    collect_static_files()
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


def create_kashana_instance(instance, host, branch):
    """ Create a new Kashana instance

    This will add the necessary deployment files for a new kashana
    instance.

    You will still need to add, commit and push the files on the
    instance's branch - and then deploy the instance to the host.

    Args:
        instance (str): Name of the instance. This will be used
            for generating host names and so on - for example, if
            instance_name is 'brownhare', the host name will be
            'brownhare.kashana.org'
        host (str): Name of the host on which the instance will be
            deployed. This should be the name as accessible via SSH -
            including the right port. Example: 'example.com:22'
        branch (str): Name of the branch the instance will run.
            Example: 'master'.
    """
    replacements = {
        '{{instance}}': instance,
        '{{host}}': host,
        '{{branch}}': branch
    }
    deploy_dir = tasklib.env['deploy_dir']
    django_settings_dir = tasklib.env['django_settings_dir']
    apache_conf_dir = os.path.join(
        tasklib.env['vcs_root_dir'],
        'apache'
    )
    _create_kashana_instance_deploy_dir(instance, deploy_dir, replacements)
    _create_kashana_instance_apache_conf(
        instance, deploy_dir, apache_conf_dir, replacements
    )
    _create_kashana_instance_local_settings(
        instance, deploy_dir, django_settings_dir, replacements
    )

    instructions = [
        '### All done. You will need to:',
        '###',
        '### - Add, commit and push the newly added files located in {deploy_dir}, {apache_conf}, {local_settings} to branch {branch};',
        '### - Deploy the instance by running DEPLOYDIR={deploy_dir_abs} {fab_dir}/fab.py {instance} deploy'
    ]
    print '###'
    print "\n".join(instructions).format(
        fab_dir=deploy_dir,
        deploy_dir=os.path.join(deploy_dir, instance),
        deploy_dir_abs=os.path.abspath(os.path.join(deploy_dir, instance)),
        apache_conf=apache_conf_dir,
        local_settings=django_settings_dir,
        branch=branch,
        instance=instance
    )


def _create_kashana_instance_deploy_dir(
        instance, deploy_dir_root, replacements):
    """ Create the deploy directory of a kashana instance.

    Args:
        instance (str): Instance name
        deploy_dir_root (str): Path to the root deploy dir
        replacements (dict): Dictionary of replacements as label to value
    """
    deploy_dir = os.path.join(deploy_dir_root, instance)
    deploy_dir_files = ['localfab.py', 'localtasks.py', 'project_settings.py']

    print '### Creating Kashana instance deploy directory in {}'.format(
        deploy_dir
    )

    os.mkdir(deploy_dir)
    for file_name in deploy_dir_files:
        _replace_to_copy(
            os.path.join(deploy_dir_root, 'templates', file_name),
            os.path.join(deploy_dir, file_name),
            replacements
        )


def _create_kashana_instance_apache_conf(
        instance, deploy_dir_root, apache_conf_dir, replacements):
    """ Create the apache conf file of a kashana instance

    Args:
        instance (str): Instance name
        deploy_dir_root (str): Path to the root deploy dir
        apache_conf_dir (str): Path to the apache conf dir
        replacements (dict): Dictionary of replacements as label to value
    """

    print '### Creating Kashana instance apache configuration in {}'.format(
        apache_conf_dir
    )

    _replace_to_copy(
        os.path.join(deploy_dir_root, 'templates', 'apache.conf'),
        os.path.join(apache_conf_dir, '{}.conf'.format(instance)),
        replacements
    )


def _create_kashana_instance_local_settings(
        instance, deploy_dir_root, django_settings_dir, replacements):
    """ Create the django local settings file of a kahana instance

    Args:
        instance (str): Instance name
        deploy_dir_root (str): Path to the root deploy dir
        django_settings_dir (str): Path to the django settings dir
        replacements (dict): Dictionary of replacements as label to value
    """

    print '### Create Kashana instance django settings in {}'.format(
        django_settings_dir
    )

    _replace_to_copy(
        os.path.join(
            deploy_dir_root, 'templates', 'local_settings.py.instance'
        ),
        os.path.join(
            django_settings_dir, 'local_settings.py.{}'.format(instance)
        ),
        replacements
    )


def _replace_to_copy(source_file_name, dest_file_name, replacements):
    """ Replace strings in file, and save results as a copy.

    Args:
        source_file_name (str): Name of the source file
        dest_file_name (str): Name of the destination file
        replacements (dict): Dictionary of placeholder to value to
            replace in the file
    """
    with open(source_file_name) as f:
        content = f.read()

    for (key, value) in replacements.items():
        content = content.replace(key, value)

    with open(dest_file_name, 'w') as f:
        f.write(content)
