Alfie install
=============


Setting up new instance
-----------------------

1. Bootstrap environment by running::

     deploy/bootstrap.py

2. Deploy locally with::
   
     deploy/tasks.py deploy:dev

   This script wants to create a MySql database.  DYE_'s `MySql database
   manager`__ assumes your MySQL root password is in
   `/root/mysql_root_password`; this task will ask for a sudo password in order
   to access this file.

.. _DYE: https://github.com/aptivate/dye
.. __: https://github.com/aptivate/dye/blob/develop/dye/tasklib/database.py#L157

Setting up from empty database
------------------------------

1. Create superuser account with `./manage.py createsuperuser` in `django/website`

2. Run local Alfie server with `./manage.py runserver`

Now you can add Results via the dashboard.  (e.g.  http://127.0.0.1:8000/dashboard/) 
The first couple of levels of the results hierarchy have only one entry. These are usually:

  1. Impact/Goal
  2. Outcome

The next two levels can have many items:

  3. Output
  4. Sub-output level 

If you expand the tree beyond this level, you're adding Activities.



3. Add Risk Ratings (e.g. http://127.0.0.1:8000/admin/logframe/riskrating/add/)

   You can pick them on planning page (click edit from Dashboard) for Result objects.

4. Add milestones for your LogFrame (e.g.  http://127.0.0.1:8000/admin/logframe/milestone/add/)
   These have a name and a date like "Baseline": 01/01/2014, "Quarter 2": 01/04/2014

   Now you can add targets for Indicators

5. Add (RAG) Ratings (e.g. http://127.0.0.1:8000/admin/logframe/rating/add/)
   These are something like:  ("On plan", Green), ("Behind plan", Orange), ("Seriously behind", Red), ("Unrated", Grey)

   You can rate results and indicators

6. Add TA (Technical Assistance) Types (e.g.  http://127.0.0.1:8000/admin/logframe/tatype/add/)
   and Activity Status codes (e.g. http://127.0.0.1:8000/admin/logframe/statuscode/add/)

