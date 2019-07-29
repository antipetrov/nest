# Nest
Rebuilding flat dicts into nested stricture  

## Installation

Only Python 3.6 (or higher) is required for script start.

## Usage

Example data is prepared in file `input.txt`. 

Possible usage looks like this 
```
cat input.txt|python nest.py currency city country
```

## Tests

For tests `pytest` is used. 

Install pytest with

```
pip install -r requirements.txt
```


Run tests with 
```
pytest test.py
```


## Web service

You can run nesting procedure as a web-service. 
Web-service utilizes Flask to handle requests.


### Install web-service
Install web-part with

```
pip install -r requirements.web.txt
```

### Start web-service
Run service with

```
export FLASK_APP=nest_web.py
flask run 
```

After that web-service starts in DEBUG-mode on `http://127.0.0.1:5000`

### Authentication 

Web-service supports basic-basic-authentication. 
To turn it on, modify the following environment variables and re-run flask.

```
export NEST_WEB_AUTH_ENABLED=True
export NEST_WEB_LOGIN='testuser'
export NEST_WEB_PASSWORD='testpassword'
``` 

**Warning:** This is in no way a secure auth-scheme. 
Secure storage for login-credentials is needed and I did not implement it here.    

### Web-requests

Web-service handles single URL with input data passed as json-object in the request body 
and keys list as query-parameters.

Example:

```
POST http://127.0.0.1:5000/?keys=currency,country,city
[{"country":"US","city":"Boston","currency":"USD","amount":100},{"country":"FR","city":"Paris","currency":"EUR","amount":20},{"country":"FR","city":"Lyon","currency":"EUR","amount":11.4},{"country":"ES","city":"Madrid","currency":"EUR","amount":8.9},{"country":"UK","city":"London","currency":"GBP","amount":12.2},{"country":"UK","city":"London","currency":"FBP","amount":10.9}]
``` 

same as CURL (without HTTP-auth headers):

```
curl -X POST \
  'http://localhost:5000/?keys=currency,country' \
  -H 'Content-Type: application/json' \
  -H 'cache-control: no-cache' \
  -d '[{"country":"US","city":"Boston","currency":"USD","amount":100},{"country":"FR","city":"Paris","currency":"EUR","amount":20},{"country":"FR","city":"Lyon","currency":"EUR","amount":11.4},{"country":"ES","city":"Madrid","currency":"EUR","amount":8.9},{"country":"UK","city":"London","currency":"GBP","amount":12.2},{"country":"UK","city":"London","currency":"FBP","amount":10.9}]'

```

## Web tests

Run web-part tests with 
```
pytest test_web.py
```
Warning: tests for web part run only with flask started. For some reason I did not use flask testing tools and went on with requests-library. 