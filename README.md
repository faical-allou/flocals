# flocals

This is the back end flask app for flocals, this only works with the front end app: [flocals-app](https://github.com/faical-allou/flocals-app)

This was written and contains all the set up to be used with [pipenv](https://pipenv.readthedocs.io/en/latest/) and an account on [heroku](https://www.heroku.com/)

You'll need to add a file called configdatabase with the following content:

```
connectionStringDatabase = "host='xxx' port='5432' dbname='xxx' user='xxx' password='xxx'"

CLIENT_ID = 'xx-xx'
CLIENT_SECRET = 'xxx'
AUTH_REDIRECT_URI = 'http://localhost:5000/google/auth'
BASE_URI = 'http://localhost:5000'
FLASK_SECRET_KEY = 'xxx'
G_API_KEY = 'xxx'
```

