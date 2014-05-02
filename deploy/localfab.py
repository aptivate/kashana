from os import path
from datetime import datetime
from fabric.context_managers import settings
from fabric.api import env, require
import fablib
from dye.fabfile import _server_setup


def deploy(revision=None, keep=None, full_rebuild=True):
    """ update remote host environment (virtualenv, deploy, update)

    It takes three arguments:

    * revision is the VCS revision ID to checkout (if not specified then
      the latest will be checked out)
    * keep is the number of old versions to keep around for rollback (default
      5)
    * full_rebuild is whether to do a full rebuild of the virtualenv
    """
    require('server_project_home', provided_by=env.valid_envs)

    # this really needs to be first - other things assume the directory exists
    fablib._create_dir_if_not_exists(env.server_project_home)

    # if the <server_project_home>/previous/ directory doesn't exist, this does
    # nothing
    fablib._migrate_directory_structure()
    fablib._set_vcs_root_dir_timestamp()

    fablib.check_for_local_changes(revision)
    # TODO: check for deploy-in-progress.json file
    # also check if there are any directories newer than current ???
    # might just mean we did a rollback, so maybe don't bother as the
    # deploy-in-progress should be enough
    # _check_for_deploy_in_progress()

    # TODO: create deploy-in-progress.json file
    # _set_deploy_in_progress()
    fablib.create_copy_for_next()
    fablib.checkout_or_update(in_next=True, revision=revision)
    # remove any old pyc files - essential if the .py file is removed by VCS
    if env.project_type == "django":
        fablib.rm_pyc_files(path.join(env.next_dir, env.relative_django_dir))
    # create the deploy virtualenv if we use it
    fablib.create_deploy_virtualenv(in_next=True, full_rebuild=full_rebuild)

    # we only have to disable this site after creating the rollback copy
    # (do this so that apache carries on serving other sites on this server
    # and the maintenance page for this vhost)
    downtime_start = datetime.now()
    fablib.link_webserver_conf(maintenance=True)
    with settings(warn_only=True):
        fablib.webserver_cmd('reload')
    # TODO: do a database dump in the old directory
    fablib.point_current_to_next()

    # Use tasks.py deploy:env to actually do the deployment, including
    # creating the virtualenv if it thinks it necessary, ignoring
    # env.use_virtualenv as tasks.py knows nothing about it.
    fablib._tasks('deploy:' + env.environment)

    ensure_webassets_cache_writeable_by_apache()
    # bring this vhost back in, reload the webserver and touch the WSGI
    # handler (which reloads the wsgi app)
    fablib.link_webserver_conf()
    fablib.webserver_cmd('reload')
    downtime_end = datetime.now()
    fablib.touch_wsgi()

    fablib.delete_old_rollback_versions(keep)
    if env.environment == 'production':
        fablib.setup_db_dumps()

    # TODO: _remove_deploy_in_progress()
    # move the deploy-in-progress.json file into the old directory as
    # deploy-details.json
    fablib._report_downtime(downtime_start, downtime_end)


def ensure_webassets_cache_writeable_by_apache():
    webassets_cache = path.join(fablib.env.django_dir, 'static')
    fablib.sudo_or_run('chown -R apache %s' % webassets_cache)

def alfie_demo():
    """Run alfie demo on shared host"""
    _server_setup('alfie_demo')
