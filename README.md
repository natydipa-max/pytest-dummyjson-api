# Pytest DummyJSON API Framework

[![Smoke Tests](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml/badge.svg)](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml)

## Overview

API test automation framework built with Python and Pytest, targeting the [DummyJSON](https://dummyjson.com) public API.

The framework covers authentication workflows, CRUD operations for the `/products` endpoint, retrieval and search operations for the `/users` endpoint, and retrieval and creation workflows for the `/carts` endpoint, using Pydantic for request/response schema validation and GitHub Actions for continuous integration.

---

## Tech Stack

- Python 3.12
- Pytest
- Requests
- Pydantic v2
- GitHub Actions

---

## Architecture

The framework is organized in layers:

HTTP clients share a common base client that centralizes session configuration, default headers, and request timeouts.

```
pytest-dummyjson-api/
├── src/
│   ├── client/
│   │   ├── base_client.py       # HTTP session, shared methods
│   │   ├── product_client.py    # Products endpoint abstraction
│   │   ├── user_client.py       # Users endpoint abstraction
│   │   ├── cart_client.py       # Carts endpoint abstraction
│   │   └── auth_client.py       # Authentication endpoint client
│   └── models/
│       ├── products/
│       │       ├── product_model.py                  # GET response schema
│       │       ├── product_request_model.py          # POST/PUT request body
│       │       ├── product_create_response_model.py  # POST response schema
│       │       ├── product_delete_response_model.py  # DELETE response schema
│       │       └── product_response_model.py         # GET list response schema
│       ├── users/
│       │       ├── user_model.py                     # GET response schema
│       │       ├── user_response_model.py            # GET list response schema
│       │       ├── user_create_response_model.py     # POST response schema
│       │       ├── user_request_model.py             # POST/PUT request body
│       │       └── current_user_model.py             # Authenticated user schema
│       ├── carts/
│       │       ├── cart_model.py                     # GET response schema
│       │       ├── carts_response_model.py           # GET list response schema
│       │       ├── cart_product_model.py             # Nested product schema for GET responses
│       │       ├── cart_item_request_model.py        # Nested product request schema
│       │       ├── create_cart_request_model.py      # POST request body
│       │       ├── create_cart_request_model.py      # POST request body
│       │       ├── created_cart_model.py             # POST response schema
│       │       └── created_cart_product_model.py     # Nested product schema for POST responses
│       ├── auth/
│       │       └── login_response_model.py           # Login response schema
│       └── error_response_model.py           # 4xx error response schema
├── tests/
│   ├── products/
│   │   ├── test_get_products.py
│   │   ├── test_create_product.py
│   │   ├── test_update_product.py
│   │   ├── test_delete_product.py
│   │   └── test_negative_products.py
│   ├── users/
│   │   ├── test_get_users.py
│   │   ├── test_negative_users.py
│   │   ├── test_search_users.py
│   │   └── test_create_user.py
│   ├── carts/
│   │   ├── test_get_carts.py
│   │   ├── test_create_carts.py
│   │   └── test_negative_carts.py
│   └── auth/
│       ├── test_auth.py
│       └── test_current_user.py
├── docs/
│   └── testing_strategy.md
├── conftest.py
├── pytest.ini
└── requirements.txt
```

---

## Authentication

Authenticated endpoint tests use a reusable session-scoped `auth_token` fixture.

The fixture performs login once per test session and provides a valid access token for protected endpoint testing.

---

## API Coverage

### Authentication

| Method | Endpoint | Covered Scenarios |
|--------|----------|-------------------|
| POST | `/auth/login` | Valid credentials, invalid username, invalid password, missing credentials |
| GET | `/auth/me` | Valid token, invalid/expired token |

### Products

| Method | Endpoint | Covered Scenarios |
|--------|----------|-------------------|
| GET | `/products` | Retrieve all products, response schema validation |
| GET | `/products/{id}` | Valid ID, invalid ID format, nonexistent ID |
| POST | `/products/add` | Valid creation, malformed JSON |
| PUT | `/products/{id}` | Successful update, nonexistent ID |
| DELETE | `/products/{id}` | Successful deletion, nonexistent ID |

### Users

| Method | Endpoint | Covered Scenarios |
|--------|----------|-------------------|
| GET | `/users` | Retrieve all users, response schema validation |
| GET | `/users/{id}` | Valid ID, invalid ID format, nonexistent ID |
| GET | `/users/search` | Successful search, partial matching, empty results |
| POST | `/users/add` | Valid creation, malformed JSON |

### Carts

| Method | Endpoint | Covered Scenarios |
|--------|----------|-------------------|
| GET | `/carts` | Retrieve all carts, pagination (`limit`/`skip`), boundary values |
| GET | `/carts/{id}` | Valid ID, invalid ID format, nonexistent ID |
| GET | `/carts/user/{id}` | Valid user, nonexistent user |
| POST | `/carts/add` | Valid creation, multiple products, single product, invalid product, malformed JSON, missing userId, empty products, nonexistent user |
---

## Validation Strategy

All tests follow a consistent three-step approach:

1. **Status code** — assert the expected HTTP status code
2. **Schema** — validate the response body using Pydantic models
3. **Business rules** — assert endpoint-specific behavior

Response contracts are validated using dedicated Pydantic models organized by domain (`auth`, `products`, `users`, and `carts`).

- `ProductModel` — individual product returned by GET endpoints
- `ProductsResponseModel` — paginated response returned by `GET /products`
- `ProductRequestModel` — request payload used by `POST /products/add` and `PUT /products/{id}`
- `ProductCreateResponseModel` — response returned by `POST /products/add`
- `ProductDeleteResponseModel` — response returned by `DELETE /products/{id}`, including `isDeleted` and `deletedOn`
- `UserModel` — individual user returned by GET endpoints
- `UsersResponseModel` — paginated response returned by `GET /users` and `GET /users/search`
- `UserRequestModel` — request payload used by `POST /users/add`
- `UserCreateResponseModel` — response returned by `POST /users/add`
- `LoginResponseModel` — response returned by `POST /auth/login`
- `CurrentUserModel` — authenticated user returned by `GET /auth/me`
- `ErrorResponseModel` — error response returned by 4xx endpoints
- `CartModel` — individual cart returned by GET endpoints
- `CartsResponseModel` — paginated response returned by `GET /carts`
- `CreateCartRequestModel` — request payload used by `POST /carts/add`
- `CreatedCartModel` — response returned by `POST /carts/add`

---

## CI Pipeline

The pipeline runs on every push and pull request to `main` with two sequential jobs:

```
Smoke Tests → Full Test Suite
```

The full suite only runs if smoke passes first. If the API is down, smoke fails fast and the full suite does not start.

```bash
# Trigger smoke only locally
pytest -m smoke --tb=short -v

# Trigger full suite locally
pytest --tb=short -v
```

---

## Design Choices

- Reusable API clients encapsulate endpoint communication and keep HTTP logic separate from test assertions.
- Response contracts are validated with Pydantic models to improve readability and maintainability.
- Smoke tests provide a fast feedback loop before running the full test suite in CI.
- Request timeouts are centralized in the base client to prevent hanging test executions.

---

## Exploratory Findings

#### Authentication Security Observation: GET /auth/me

The authenticated user endpoint returns sensitive user information, including the user's password.

Example fields returned:

```json
{
  "username": "emilys",
  "password": "emilyspass"
}
```

This behavior is acceptable for a public demo API but would be considered a security issue in a production environment, where password fields should never be returned in API responses.

### POST Validation Behavior

Exploratory testing of the `/products/add` and `/users/add` endpoints revealed that both endpoints perform JSON syntax validation but very limited business validation.

Both endpoints:

- accept empty request bodies;
- accept partial payloads;
- accept incorrect field types;
- return `400 Bad Request` only when the request contains malformed JSON.

An additional behavioral difference was identified:

- `/products/add` returns a **partial response**, containing only the fields provided in the request (plus the generated `id`).
- `/users/add` returns a **complete user object**, populating unspecified fields with empty strings or `null` values.

These behaviors appear to be implementation-specific characteristics of the DummyJSON API rather than expected production-grade validation rules.

Raw request methods are used exclusively for negative testing scenarios where malformed JSON must be sent intentionally, bypassing client serialization.

### GET /products

DummyJSON wraps the list response in a pagination envelope:

```
{
  "products": [...],
  "total": 194,
  "skip": 0,
  "limit": 30
}
```

The `products` key must be accessed explicitly — the response is not a direct array.

### PUT /products/{id}

Behaves consistently with GET and DELETE for nonexistent IDs — returns `404 Not Found` with a message body.

### DELETE /products/{id}

Returns the full product object with two additional fields confirming deletion:

```
{
  "isDeleted": true,
  "deletedOn": "2026-06-17T17:38:54.060Z"
}
```

### OPTIONS /products/add

Returns `204 No Content` with allowed methods only. No schema or field validation contract is exposed.

### brand field

Not all products include a `brand` field. The `ProductModel` defines it as optional (`brand: str | None = None`) to avoid schema validation failures on products without brand.

### GET /users/search

The endpoint supports searching through the `q` query parameter.

Example:

```text
GET /users/search?q=Noah
```

The response follows the same paginated structure as `GET /users`, returning a `users` array together with `total`, `skip`, and `limit`.

#### Observed search behavior

Based on exploratory testing with `curl` requests:

- ✅ Performs partial (substring) matching on `firstName`.
- ✅ Performs partial (substring) matching on `lastName`.
- ✅ Supports searching by `username`.
- ❌ Does not search by `email`.
- ❌ Does not search by `maidenName`.

Examples:

```bash
# Partial match on firstName
curl "https://dummyjson.com/users/search?q=na"

# Match by lastName
curl "https://dummyjson.com/users/search?q=Hernandez"

# Match by username
curl "https://dummyjson.com/users/search?q=noahh"

# No results when searching by email
curl "https://dummyjson.com/users/search?q=@dummyjson.com"

# No results when searching by maidenName
curl "https://dummyjson.com/users/search?q=Morgan"
```

> **Note:** These behaviors were verified through exploratory testing and reflect the current implementation of the DummyJSON API.

---

### GET /carts

Pagination behaves consistently with the Users endpoint.

Observed behavior:

- `limit=0` returns all available carts.
- `limit` greater than the total returns all available carts.
- `skip` beyond the available data returns an empty list with HTTP 200.

These behaviors were validated and covered by automated tests.

## Running the Tests

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest --tb=short -v

# Run smoke tests only
pytest -m smoke --tb=short -v

# Run a specific file
pytest tests/products/test_negative_products.py -v
```

### Test markers

- `negative`: Tests that verify the API correctly handles invalid input, malformed requests, and expected error responses.

Example:

```bash
pytest -m negative
```