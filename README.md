# Pytest DummyJSON API Framework

[![Smoke Tests](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml/badge.svg)](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml)

## Overview

API test automation framework built with Python and Pytest, targeting the [DummyJSON](https://dummyjson.com) public API.

The framework covers authentication workflows and CRUD operations on the `/products` endpoint, using Pydantic for schema validation and GitHub Actions for CI execution.

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
│   │   └── auth_client.py       # Authentication endpoint client
│   └── models/
│       ├── product_model.py                  # GET response schema
│       ├── product_request_model.py          # POST/PUT request body
│       ├── product_create_response_model.py  # POST response schema
│       ├── product_delete_response_model.py  # DELETE response schema
│       ├── error_response_model.py           # 4xx error response schema
│       ├── login_response_model.py           # Login response schema
│       └── current_user_model.py             # Authenticated user schema
├── tests/
│   ├── products/
│   │   ├── test_get_products.py
│   │   ├── test_create_product.py
│   │   ├── test_update_product.py
│   │   ├── test_delete_product.py
│   │   └── test_negative_products.py
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

| Method | Endpoint | Test | Type |
|----------|----------|----------|----------|
| POST | /auth/login | test_login_with_valid_credentials | smoke |
| POST | /auth/login | test_login_with_invalid_username | negative |
| POST | /auth/login | test_login_with_invalid_password | negative |
| POST | /auth/login | test_login_with_empty_credentials | negative |
| GET | /auth/me | test_get_current_user | smoke |
| GET | /auth/me | test_get_current_user_with_invalid_token | negative |

### Products Endpoint

| Method | Endpoint | Test | Type |
|--------|----------|------|------|
| GET | /products | test_get_all_products | smoke |
| GET | /products/{id} | test_get_product_by_id | smoke |
| GET | /products/{id} | test_get_product_with_nonexistent_id_returns_404 | negative |
| GET | /products/{id} | test_get_product_with_non_numeric_id_returns_404 | negative |
| POST | /products/add | test_create_product | smoke |
| PUT | /products/{id} | test_update_product | smoke |
| PUT | /products/{id} | test_update_product_with_nonexistent_id_returns_404 | negative |
| DELETE | /products/{id} | test_delete_product | smoke |
| DELETE | /products/{id} | test_delete_product_with_nonexistent_id_returns_404 | negative |

---

## Validation Strategy

All tests follow a consistent three-step approach:

1. **Status code** — assert the expected HTTP status code
2. **Schema** — validate the response body using Pydantic models
3. **Business rules** — assert endpoint-specific behavior

Each HTTP operation has its own Pydantic model to reflect the actual response contract:

- `ProductModel` — key product fields returned by GET
- `ProductCreateResponseModel` — object returned by POST
- `ProductDeleteResponseModel` — object returned by DELETE, validates `isDeleted` and parses `deletedOn` as a timestamp
- `ErrorResponseModel` — error object returned by 4xx responses
- `LoginResponseModel` — response returned by /auth/login
- `CurrentUserModel` — authenticated user returned by /auth/me

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

- Reusable API clients keep endpoint logic separate from test assertions.
- Pydantic models validate response contracts while keeping tests readable.
- Smoke tests provide a fast signal before running the full suite in CI.
- Request timeouts are centralized to avoid hanging test runs.

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

### POST /products/add

Returns `201 Created` with the full created object, including the fields sent in the request body.

The API does not enforce required fields — requests with an empty body return `201 Created`. No business validation is implemented.

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

---

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