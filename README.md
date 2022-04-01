# appForTesting

### Description:
   Film rating service. 
   For authentication Basic Auth is used, 
   before starting to use the service, create 
   an account, send a post request on `/users/`
   with password and name in the body,
   and use it as credentials. Run the app and go to
   `/docs` to see more. Also, admin 
   panel is available,
   run admin and follow `/admin/`.
   In the admin panel, you can edit comments of reviews,
   create, delete movies and see detailed 
   information about users

### Create venv:
    make venv

### Run application
    make up

### Run admin
    make admin

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Create Docker image:
    docker build . -t kinoapp

### Create and run docker container
    docker run -dp 80:80 --rm --name mycontainer kinoapp

