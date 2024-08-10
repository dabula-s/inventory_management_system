## Users documentation

## Table of contents

- [Users](#users)
    - [User registration](#user-registration)
    - [User verifying](#user-verifying)
    - [User log in](#user-log-in)
    - [User log out](#user-log-out)

### Users

Auto-generated API documentation you can find by [the link](http://0.0.0.0:8000/docs#/).

> NOTE: to grant superuser privileges to user change the `is_superuser` field value in `User` table for this user or
> update user info with already registered superuser via PATCH /users/{id} endpoint.

#### User registration

First of all you need to register new user.

- Registration request:
  ![img.png](./poc/user_registration_request.png)

- Registration response on success:
  ![img.png](./poc/user_registration_response.png)

After registration you need to [verify](#user-verifying) user.

#### User verifying

Verifying process includes request for token and user verification with this token.

1. Getting verification token:

    - Request token for user validation:
      ![img.png](./poc/user_request_verify_token_request.png)

    - Token is not in response:
      ![img.png](./poc/user_request_verify_token_response.png)

    - You can find token in api-service logs (since the token isn't sent via email or smth else, it's just printed in
      the service logs):
      ![img.png](./poc/user_request_verify_token_token.png)

2. Using the received token we verify the user:

    - Verifying request:
      ![img.png](./poc/user_verify_request.png)

    - Verifying response on success:
      ![img.png](./poc/user_verify_response.png)

#### User log in

1. With username and password you can log in and get token:

    - User login request:
      ![img.png](./poc/user_login_request.png)

    - User login response:
      ![img.png](./poc/user_login_response.png)

2. Or simple authorize with `Authorize` button on the docs page:

    - Authorization form:
      ![img.png](./poc/user_docs_authorization.png)

    - Successful authorization:
      ![img.png](./poc/user_docs_authorized.png)

#### User log out

To log out just send request to `/auth/logout` endpoint.

- Logout request:
  ![img.png](./poc/user_logout_request.png)

- Logout response:
  ![img.png](./poc/user_logout_response.png)

- Logout response if user is not logged in:
  ![img.png](./poc/user_logout_unaothorized.png)
