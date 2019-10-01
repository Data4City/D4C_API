Deployment with Docker
----------------------

You must have ``docker`` and ``docker-compose`` tools installed to work with material in this section.

    docker-compose up -d

Application will be available on ``localhost`` or ``127.0.0.1`` in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` directory. ``alembic`` is directory with sql migrations.
Application parts are:

::

    models  - pydantic models that used in crud or handlers
    crud    - CRUD for types from models (create new user/article/comment, check if user is followed by another, etc)
    db      - db specific utils
    core    - some general components (jwt, security, configuration)
    api     - handlers for routes
    main.py - FastAPI application instance, CORS configuration and api router including



Upgrade DB
----------
Alembic is used to keep track of the migrations and uses SQLAlchemy as its backend.

To create a new migration modify the models inside of db_models and if you add/delete models make sure to change the imports inside of app/db/base.py

After all of that is done run:

::

        alembic revision -m "Add a column"

This will create a new migration inside of alembic/versions.
Modify it accordingly so other automatic changes aren't inserted.

To apply the changes to the DB run

::

    alembic upgrade head


Todo
----
1) Add python tests
