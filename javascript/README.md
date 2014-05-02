Setting up fron-end environment
===============================

If you are using recent Ubuntu, then install npm which will also install
nodejs. Because of a name conflict with another package it will be named
nodejs instead of node, so you will have to create a symlink yourself
(assuming you don't have amateur radio node package installed):

    sudo ln -s /usr/bin/nodejs /usr/local/bin/node

We'll need phantomjs to run tests:

    sudo npm install -g phantomjs
    sudo npm install -g gulp

Install local dependencies by switching to directory
v4clogframe/javascript and running:

    npm install

This will install all the necessary packages including Gulp which we use for
defining and running tasks. Currently following tasks are defined (and at
least somewhat useful):

    gulp test (runs tests)
    gulp jshint (checks code with JSHint)
    gulp templates (compiles templates to src/lib/templates.js)
    gulp watch (runs JSHint and compiles templates when either change)

