Kashana deploy
==============

It is possible to deploy multiple instances of Kashana on a single host. To do this we create a separate deploy directory, settings file and apache config file for each instance.

This process is automated by running, in the deploy folder:

    ./tasks.py create_kashana_instance:instance=sitename,host=server:port,branch=mybranch

Where:

- `sitename` is the name of the kashana instance. The instance will then be available at `sitename.kashana.org`;
- `server:port` is the host name of the server we are deploying to;
- `mybranch` is the branch we want to deploy.

This will create a number of files:

- A custom deploy directory under `deploy/sitename` with several files;
- An apache config file in `apache/sitename.conf`;
- A settings file in `django/website/local_settings.py.sitename`.

All these files must be added, commited and pushed to the git repository on branch `mybranch`. (Note that if you want to use a custom git repository, you'll need to edit `deploy/sitename/project_settings.py`).

Once this is done, you can run, from the `deploy` folder:

    DEPLOYDIR=/path/to/deploy/sitename fab.py sitename deploy

And this will deploy the site, and make it available at `sitename.kashana.org` (providing DNS settings point to the correct server).
