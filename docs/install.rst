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

Now you can add Results via the dashboard_. The first couple of levels of the
results hierarchy have only one entry. These are usually:

  1. Impact/Goal
  2. Outcome

The next two levels can have many items:

  3. Output
  4. Sub-output level 

.. _dashboard: http://127.0.0.1:8000/dashboard/

If you expand the tree beyond this level you're adding Activities.



3. Add Risk Ratings

   You can pick them on edit (plan) page of result objects.

4. Add milestones

   Now you can add targets for indicators

5. Add (RAG) Ratings

   You can rate results and indicators

6. Add TA Types and Status code

