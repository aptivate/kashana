Alfie install
=============


Setting up new instance
-----------------------

1. Bootstrap environment by running `./bootstrap.py` in `deploy` directory

2. Deploy locally with `./tasks.py deploy:dev` in the same directory



Setting up from empty database
------------------------------

1. Create superuser account with `./manage.py createsuperuser`

   You can now log in but the app crashes saying no logframe is present.

2. Run local Alfie server with `./manage.py runserver`

3. Add a logframe with the admin interface http://127.0.0.1:8000/admin/

4. Add the top level Result ("Impact/Goal") with level = 1 and no parent

   Now you can add Outcomes via previously crashing interface

5. Add Risk Ratings

   You can pick them on edit (plan) page of result objects.

6. Add milestones

   Now you can add targets for indicators

7. Add (RAG) Ratings

   You can rate results and indicators

8. Add TA Types and Status code

