#!/usr/bin/env python
# a script to set up the virtualenv so we can use fabric and tasks

import os
from os import path
import re
import sys
import subprocess
from ve_mgr import check_python_version, UpdateVE
from project_settings import server_home

# check python version is high enough
check_python_version(2, 6, __file__)

if 'VIRTUAL_ENV' in os.environ:
    ve_dir = os.environ['VIRTUAL_ENV']
else:
    from project_settings import local_vcs_root, relative_ve_dir
    ve_dir = path.join(local_vcs_root, relative_ve_dir)

if not os.path.exists(ve_dir):
    print "Expected virtualenv does not exist"
    print "(required for correct version of fabric and dye)"
    print "Please run './bootstrap.py' to create virtualenv"
    sys.exit(1)

updater = UpdateVE(ve_dir=ve_dir)
if updater.virtualenv_needs_update():
    print "VirtualEnv needs to be updated"
    print 'Run deploy/bootstrap.py'
    sys.exit(1)

# depending on how you've installed dye, you may need to edit this line
tasks = path.join(ve_dir, 'bin', 'tasks.py')

current_dir = path.dirname(__file__)

# call the tasks.py in the virtual env
tasks_call = [tasks]

# Find the deployment directory depending on the deployment target. Failing that,
# use the current path to determine if we are using a custom deployment directory.
# Otherwise use the current folder.
alt_settings_dir = None
for arg in sys.argv:
    matches = re.match('deploy:(.+)$', arg)
    if matches:
        alt_settings_dir = os.path.join(current_dir, matches.group(1))
if alt_settings_dir is None:
    matches = re.match(re.escape(server_home) + '/?([^/]+)\.kashana', current_dir)
    if matches:
        alt_settings_dir = os.path.join(current_dir, matches.group(1))
if alt_settings_dir is not None and os.path.isdir(alt_settings_dir):
    deploy_dir = alt_settings_dir
else:
    deploy_dir = current_dir
tasks_call += ['--deploydir=' + deploy_dir]

# add any arguments passed to this script
tasks_call += sys.argv[1:]

if '-v' in sys.argv or '--verbose' in sys.argv:
    print "Running tasks.py in ve: %s" % ' '.join(tasks_call)

# exit with the tasks.py exit code
sys.exit(subprocess.call(tasks_call))
