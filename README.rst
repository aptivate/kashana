Kashana
=======

Kashana is an open source logframe manangement tool for planning and evaluating 
projects, used and written by `Aptivate <http://aptivate.org/>`_.

Installation
------------

System requirements:

POSIX-compliant system (tested on Linux)
Python 2.7
Node JavaScript platform
Apache + WSGI
MySQL
Recommended at least 1GB of RAM

In the deploy directory, run:

    ./bootstrap.py
    ./tasks.py deploy:<enviroment name>


Usecases
--------
1. A multi-stakeholder and multi-organisation team operates in dozens or hundreds of villages and urban areas across Zambia. They need Android-based support to coordinate their work. They are assessing well-being, using ODK or similar on their tablets / phones. They may also be coordinating the delivery of some services -- perhaps health education, for example. They may be helping people to fill out forms to apply for various types of aid, or to register for different relations with the government bureaucracies. They need to have a well-being assessment tool that tracks the impact of their work and the work of the other development agencies in the area. How do they coordinate their activities? How do they collaborate? How are their documents hosted? Could Kashana be all or part of the solution?
2. Let us imagine that an organisation gets a grant to work with us and their Ghanaian chapter. They would like to provide an inexpensive tool for coordinating the work of their Ghanian chapter via mobile phone or very inexpensive tablet. They also need to show their donors / funders that their work in promoting local participation in Ghana is improving local life outcomes. If Kashana is to help, it needs to provide a way of assessing life impacts (or tracking life impact assessments) as well as coordinating local activities (tasks, calendar, etc. for local teams and a coordinating group).
3. We have a financial tracking system called CASH. The people using CASH want to know how money will be divided up between the different elements of the logframe, and also between the different people who are responsible for spending the money. They are only slightly concerned about tracking impacts within CASH -- as long as the money gets spent and they know what they have to do in order to effectively use their whole budget, they are happy.
4. Various triple-bottom-line companies want to keep track of key performance indicators (outputs) as well as the social and environmental impacts of their work (outcomes), in a way that integrates with their daily work. Kashana might give those small and medium-size ethical businesses a way to manage their workflows and their policies at the same time as tracking impact, in a way that makes it easy to learn and steer. Having a simple way to connect the outputs (what the business is selling) to impacts (of various kinds) within a shared collaboration-support environment (Kashana, the intranet) can let those businesses see what's going on with a minimum of switching back and forth between a dozen different applications or interfaces. Also, it can reduce the need to enter data multiple times.

API
---

All URLS except creation are ``/logframes/<logframe_pk>/<itemtype>/<item id>``
URLS for creation are ``/logframes/<logframe_pk>/<itemtype>``
Actions determined by request type::

   PUT = update
   DELETE = delete
   POST = create

The code to get the logframe exists in ``logframe.views.OverviewMixin``. It's a method called ``get_logframe``.

The code for the backend that does the work on the logframe lives under ``django/website/logframe/api``.

Running Javascript tests
------------------------

If you are using recent Ubuntu, then install npm which will also install nodejs. Because of a name conflict with another package it will be named nodejs instead of node, so you will have to create a symlink yourself (assuming you don't have amateur radio node package installed)::

   sudo ln -s /usr/bin/nodejs /usr/local/bin/node

We'll need phantomjs to run tests::

   sudo npm install -g phantomjs
   sudo npm install -g grunt

Install local dependencies by switching to directory alfie/javascript and running::

   npm install

This will install all the necessary packages including Gulp which we use for
defining and running tasks. Currently following tasks are defined (and at
least somewhat useful)::

   grunt test (runs tests)
   grunt jshint (checks code with JSHint)
   grunt templates (compiles templates to src/lib/templates.js)
   grunt watch (runs JSHint and compiles templates when either change)
