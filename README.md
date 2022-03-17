# flaskr

Based on Flask 2.0 official docs, and more.

## How to build

You can use pipx to load a pipenv shell and the provided Pipfile to automatically generate a venv.  
I also used pipenv to generate a pinned requirements.txt file, if that helps.

## How to run

`export FLASK_APP=.`  
`export FLASK_ENV=development`  
`flask init-db`  
`flask run`

or

## .env

`.env.sh` generates this `.env` file:

```dotenv
FLASK_APP=.
FLASK_ENV=development
```

`flask init-db`  
`flask run`
