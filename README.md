# API Documentation

This document provides detailed information about the REST API endpoints available in this Django project. Each endpoint is described with its method, URL, required parameters, and possible responses.

## Swagger UI

The project includes an interactive Swagger UI that provides detailed information about all the API endpoints, their required parameters, and possible responses. This tool allows you to test API endpoints directly from your web browser.

### Accessing Swagger UI

To access the Swagger UI, navigate to the following URL:

[{URL}/api/schema/swagger-ui/]

This URL will lead you to the interactive API documentation where you can:

- **Explore all available API endpoints**: Each endpoint is listed with HTTP methods and a brief description.
- **Try out the API calls**: You can execute requests to the API directly from the Swagger interface. To do so, expand the endpoint details, fill in the required parameters, and click the "Try it out" button.
- **View the request and response details**: Swagger UI provides a detailed view of the request headers, response body, status code, and headers.

### Using Swagger UI

To make effective use of the Swagger UI, follow these steps:

1. **Authenticate**: For endpoints requiring authentication, obtain a token via the authentication endpoints and use this token by clicking the "Authorize" button at the top of the Swagger page.
2. **Select an endpoint**: Click on any endpoint to expand its details.
3. **Set parameters**: If the endpoint requires parameters, enter them in the respective fields.
4. **Send the request**: Click the "Execute" button to send the request to the API and view the response directly in the Swagger UI.

This interactive documentation is an excellent resource for developers looking to integrate with or explore the API, providing a hands-on approach to learning how each part of the API functions.


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
