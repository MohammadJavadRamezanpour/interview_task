
## Author
Mohammad Javad Ramezanpour

## Installation


install pipenv
```bash
pip install pipenv
```

install all packes in pipfile
```bash
pipenv install
```

activate the enviroment
```bash
pipenv shell
```

## /

this rout lists all posts and its available for everybody
and shows you your own votings if you have any.
only admin users can make post requests to it and create a post.
this is handled via a custome Permission class.

to make a post you need to be authenticated (JWTAuthentication, BasicAuthentication or SessionAuthentication) as admin and post these fields:

title: string,
body: string

## /rate
in this route you can make votes,
only authenticated users can make votes
to make a vote you have to send these fields:
post: integer(representing post id), score: an integer between 0 and 5

it will return error if you post a score beyond the specified scope. and also if you vote for a post again, the last vote will take effect, i mean it will be updated to the last vote you made


## auth/jwt/create/
since we use djoser for jwt authentication, this route is generated by djoser, with which you can login and get a json web token and a refresh token, then you can add the token into your request headers with some tools like modheader in this format:
Authorization: JWT <jwt_token>. this is the only way for users to authenticate, but admins can also login from their panel in /admin. djoser has other routes which i listed them in my project at config/urls.py

## auth/users/
in this route you can register new normal users

## current database records
for test, i put two posts, and three users with these credentials: admin, 123 and user1, 123 and user2, 123. the first user is an admin user and others are just normal users, the admin user can login from /admin and auth/jwt/create/, but the normal user can just login from auth/jwt/create/ as i mentioned above.

