# API Endpoints Documentation

This file provides a summary of all the available API endpoints in the project.

## Auth Module (`/auth`)

The `auth` module handles user authentication, including registration, login, and Google Sign-In.

-   **POST `/register`**
    -   **Description:** Registers a new user with email and password.
    -   **Request Body:** `schemas.UserCreate` (email, password, first_name, last_name, phone_number).
    -   **Response:** A confirmation message and user data.

-   **POST `/token`**
    -   **Description:** Authenticates a user with email and password and returns a JWT access token.
    -   **Request Body:** `OAuth2PasswordRequestForm` (username, password).
    -   **Response:** An access token and token type.

-   **GET `/google/login`**
    -   **Description:** Redirects the user to Google's authentication page to initiate Google Sign-In.

-   **GET `/google/callback`**
    -   **Description:** Handles the callback from Google after authentication. It creates or logs in the user and returns a JWT access token.

## Embeddings Module (`/embeddings`)

The `embeddings` module is responsible for creating text embeddings.

-   **POST `/embeddings/`**
    -   **Description:** Creates an embedding for a given text.
    -   **Request Body:** `schemas.TextToEmbed` (text).
    -   **Response:** A dummy embedding `[0.1, 0.2, 0.3, 0.4]`.

## Xero Module (`/xero`)

The `xero` module interacts with the Xero accounting software.

-   **GET `/invoices`**
    -   **Description:** Retrieves invoices from Xero.
    -   **Response:** A JSON object `{"module": "xero"}`.

## Voice Module (`/voice`)

The `voice` module currently has no endpoints defined.

## WhatsApp Module (`/whatsapp`)

The `whatsapp` module currently has no endpoints defined.
