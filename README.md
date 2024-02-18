# FastAPI Authentication App

##### Application was created using pattern DDD

<br>


### To run application:
`docker network create auth_external`

`docker-compose up --build -d`


### To run tests:
`docker-compose exec fastapi bash`

`python -m pytest`


## API docs


**POST /api/users/register** - Register new user
	
_required fields: username, email, password_

  responses:

	422 - 'password too short or too long'
	400 - 'Username is already taken.'
	400 - 'Email is already taken.'
 
	200 - {'success': true, 'user_id': '<user_id>'}

**POST /api/users/auth** - Auth by username
	
_required fields: username, password_

  responses:

	401 - 'Invalid credentials'
 
	200 - {'success': true, 'access_token': '<access_token>'}


**GET /api/users/me** - Get user info by access_token

    responses:
	
    400 - 'Invalid token'
    400 - 'User not found'
    
    200 - {'username': '<username>', 'email': '<email>'}


### Demo


https://github.com/kairkhan24/fastapi_authentication_app/assets/70207201/b9779ea5-7bdc-4fce-b4ac-7284c0ed6948




