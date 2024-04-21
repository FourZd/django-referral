# API Documentation

This document provides detailed information about the REST API endpoints available in this Django project. Each endpoint is described with its method, URL, required parameters, and possible responses.

## Authentication


## Refresh Token

### Refresh Access Token

- **URL:** `/api/auth/refresh/`
- **Method:** `POST`
- **Data Parameters:**
  - `refresh` (string): The refresh token received during the initial authentication.

- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "access": "new_access_token"
    }
    ```

- **Error Response:**
  - **Code:** 401 UNAUTHORIZED
  - **Content:**
    ```json
    {
      "detail": "Token is invalid or expired"
    }
    ```

- **Description:** Provides a new access token using the provided refresh token. If the refresh token is valid and not expired, a new access token is returned. If the refresh token is invalid or expired, an error is returned.


### Request Authentication Code

- **URL:** `/api/auth/request_code`
- **Method:** `POST`
- **Data Parameters:**
  - `phone_number` (string): The phone number to which the verification code will be sent. Starting with +. Example: +79998089217.

- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "message": "Code sent",
      "code": "1234"
    }
    ```

- **Error Response:**
  - **Code:** 400 BAD REQUEST
  - **Content:**
    ```json
    {
      "phone_number": [
        "This field is required."
      ]
    }
    ```

- **Description:** Mock the sending of a 4-digit verification code to the specified phone number. The code is returned in the response for testing purposes.

### Verify Code

- **URL:** `/api/auth/verify_code`
- **Method:** `POST`
- **Data Parameters:**
  - `phone_number` (string): The phone number to verify. The phone number to which the verification code will be sent. Starting with +. Example: +79998089217.
  - `code` (string): The 4-digit verification code.

- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "message": "Verification successful",
      "access": "access_token",
      "refresh": "refresh_token"
    }
    ```

- **Error Response:**
  - **Code:** 400 BAD REQUEST
  - **Content:**
    ```json
    {
      "code": [
        "Invalid or expired code"
      ]
    }
    ```

- **Description:** Verifies the 4-digit code sent to the phone number and returns JWT tokens for authentication.

## User Profile

### Get User Profile

- **URL:** `/api/profile`
- **Method:** `GET`
- **Headers:**
  - `Authorization`: `Bearer {access_token}`

- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "phone_number": "+1234567890",
      "invite_code": "ABC123"
    }
    ```

- **Error Response:**
  - **Code:** 404 NOT FOUND
  - **Content:**
    ```json
    {
      "message": "User not found"
    }
    ```

- **Description:** Fetches the profile of the authenticated user.

## Invite Activation

### Activate Invite Code

- **URL:** `/api/profile/activate_invite`
- **Method:** `POST`
- **Headers:**
  - `Authorization`: `Bearer {access_token}`

- **Data Parameters:**
  - `invite_code` (string): The invite code to be activated.

- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "message": "Invite code activated successfully"
    }
    ```

- **Error Response:**
  - **Code:** 400 BAD REQUEST
  - **Content:**
    ```json
    {
      "message": "Invite code already activated or invalid"
    }
    ```

- **Description:** Activates an invite code if it is valid and user hasn't activated another code yet.
# django-referral
