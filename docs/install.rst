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

   You can now log in but the app crashes saying no logframe is present.

3. Add a logframe with the `admin interface`_:
   
   http://127.0.0.1:8000/admin/logframe/logframe/add/

.. _admin interface: `http://127.0.0.1:8000/admin/`

4. Add the top level Result ("Impact/Goal") with level = 1 and no parent

   Now you can add Outcomes via previously crashing interface

5. Add Risk Ratings

   You can pick them on edit (plan) page of result objects.

6. Add milestones

   Now you can add targets for indicators

7. Add (RAG) Ratings

   You can rate results and indicators

8. Add TA Types and Status code

