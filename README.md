# Casting Agency Backend

## Getting Started

### Install Dependencies

1. **Python 3.9.6** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Set up the environment variables

```bash
# You should have setup.sh available
chmod +x setup.sh
source setup.sh

# The setup.sh will run the following:
# #Auth0
# export AUTH0_DOMAIN='' # the auth0 domain
# export ALGORITHMS=['']
# export API_AUDIENCE='' # the audience set for the auth0 app
# #DB
# export DATABASE_URL=''
# #Auth0 Test
# export JWT_ASSISTANT=''
# export JWT_DIRECTOR=''
# export JWT_EXECUTIVE_PRODUCER=''

# Change the Auth0, DB and Auth0 Test as applicable to you.
```

##### Auth0 Authorize Link To Generate JWT

```bash
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}

# Change the {{YOUR_DOMAIN}}, {{API_IDENTIFIER}}, {{YOUR_CLIENT_ID}} and {{YOUR_CALLBACK_URI}} as applicable to you.
```

### Database Migrations

To apply the schema changes described by the migration script to your database

```bash
flask db upgrade
```

### Run Server

To run the server, execute:

```bash
python app.py
```

### Run Unit Test(s)

To run the unit tests, execute:

```bash
dropdb casting_agency_test; createdb casting_agency_test; psql casting_agency_test < casting_agency.psql; python test_app.py;
```

## Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, regular web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `post:actors`
   - `patch:actors`
   - `delete:actors`
   - `get:movies`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`
6. Create new roles for:
   - Casting Assistant
     - can `get:actors`
     - can `get:movies`
   - Casting Director
     - all permissions a Casting Assistant has and
     - can `post:actors`
     - can `patch:actors`
     - can `delete:actors`
     - can `patch:movies`
   - Casting Executive Producer
     - all permissions a Casting Driector has and
     - can `post:movies`
     - can `delete:movies`