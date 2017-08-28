# Andela Shopping List API
====================================

The andela shopping list api that allows users plan shopping experiences.


Heroku deployment URL
--------------------

https://andela-flask-api.herokuapp.com/


Python Dependancy
--------------------

Python v3.5.2 used


Installation
------------

After cloning, create a virtual environment and install the requirements. For Linux and Mac users:

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

If you are on Windows, then use the following commands instead:

    $ virtualenv venv
    $ venv\Scripts\activate
    (venv) $ pip install -r requirements.txt


Running
-------

To run the server use the following command:

    (venv) $ python app/views.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Then from a different terminal window you can send requests or an API test client like Postman.


API Documentation
-----------------

The following routes are accessible publicly i.e. you don't need to log in.

- POST **/auth/register**

    Register a new user.<br>
    The body must contain a JSON object that defines `email`, ``username`, `password` and `password2` fields.<br>
    The passwords must match and the email should have the proper email format <br>
    On success a status code 201 is returned. The body of the response contains a JSON object with the newly added user. <br>
    On failure status code 200 is returned with a JSON object with an error message.<br>
    Notes:
    - The password is hashed before it is stored in the database. Once hashed, the original password is discarded.
    - In a production deployment secure HTTP must be used to protect the password in transit.

- POST **/auth/login**

    Login to access protected routes.<br>
    The body must contain a JSON object that defines `username` and `password` fields.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the a success message and a token that should be used for subsequent requests to protected routes.<br>
    On failure status code 200 (bad request) is returned with a JSON object with an error message<br>
    Notes:
      - The token is valid for 10 minutes
      - Good news is you can use this token to generate other tokens through the `/api/token` route and therefore have an uninterrupted experience with the service

- POST **/auth/logout**

    Logs you out and invalidates the token assigned to you.<br>

- POST **/auth/reset-password**

    Submit you email address to reset your password.<br>
    The body must contain a JSON object that defines `email` of a valid active user.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with a success message.<br>
    On failure status code 404 (bad request) or a status code 200 with an error message is returned.<br>
    Notes:
    - If successful, an email is sent to your email address with a link that will allow you to set a new password
    - This link is invalidated 10 minutes after sending the email.


- POST **/auth/reset-password<some-long-identification-token>**

    Reset password endpoint.<br>
    The body must contain a JSON object that defines `password` and `password_confirm` fields.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with a success message. You will be able to login with your new details after this.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the token used does not exists.<br>
      - 401 (Unauthorized) is returned if the token is used after 10 minutes beyond which its invalid.<br>
      - 200 is returned. The body of the response contains a JSON object with an error message..<br>



The following routes are not accessible publicly i.e. you need to log in and use your token returned on login to access them.


- POST **/shoppinglists**

    Add a new shopping list.<br>
    The body must contain a JSON object that defines a `name` field.<br>
    On success a status code 201 is returned. The body of the response contains a JSON object with the newly added list.<br>
    On failure status code<br>
      - 200 is returned with a JSON object with an error message.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.

- GET **/shoppinglists**

    Get all your shopping lists.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with all your shopping lists.<br>
    On failure status code 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>


- GET **/shoppinglists/<id>**

    Get all shopping list items under list with id : <id> .<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the items under the specified list.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id provided does not belong to any existing list.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>


- PUT **/shoppinglists/<id>**

    Update shopping list with id : <id> .<br>
    The body must contain a JSON object that defines a `name` field.<br>
    On success a status code 201 is returned. The body of the response contains a JSON object with a success attribute.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id provided does not belong to any existing list.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>


- DELETE **/shoppinglists/<id>**

    Delete shopping list with id : <id> .<br>
    On success a status code 202 is returned. The body of the response contains a JSON object with a success attribute.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id provided does not belong to any existing list.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>




- POST **/shoppinglists/<id>/items/**

    Add a new shopping list item.<br>
    The body must contain a JSON object that defines `name` and `amount` fields.<br>
    On success a status code 201 is returned. The body of the response contains a JSON object with the newly added shopping list item.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id provided does not belong to any existing list.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>




 - PUT **/shoppinglists/<id>/items/<item_id>**

    Update a shopping list item.<br>
    The body must contain a JSON object that defines `name` and `amount` fields.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with a success attribute.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id and item_id provided does not belong to any existing list or item respectively.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id or item_id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>

 - DELETE **/shoppinglists/<id>/items/<item_id>**

    Register a new user.<br>
    On success a status code 202 is returned. The body of the response contains a JSON object with a success property.<br>
    On failure status code<br>
      - 404 (bad request) is returned if the id or item_id provided does not belong to any existing list or item respectively.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>
      - 500 is returned if the id is not a valid integer.<br>
      - 200 is returned with a JSON object with an 'errors' attribute.<br>


 - POST **/api/token**

    Request a new authentication token.<br>
    On success a status code 200 is returned. The body of the response contains a JSON object with the token as a property.<br>
    On failure status code.<br>
      - 401 (unauthorized) is returned if the user is not logged in or the token is not sent with the request.<br>



### TravisCI
[![Build Status](https://travis-ci.org/VincentHokie/andela-flask-api.svg?branch=master)](https://travis-ci.org/VincentHokie/andela-flask-api)

### Coveralls
[![Coverage Status](https://coveralls.io/repos/github/VincentHokie/andela-flask-api/badge.svg?branch=master)](https://coveralls.io/github/VincentHokie/andela-flask-api?branch=master)

### Code Climate
[![Code Climate](https://codeclimate.com/github/VincentHokie/andela-flask-api.svg)](https://codeclimate.com/github/VincentHokie/andela-flask-api)

## Enjoy
