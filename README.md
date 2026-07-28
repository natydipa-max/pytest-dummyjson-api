# Pytest DummyJSON API Framework

[![Smoke Tests](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml/badge.svg)](https://github.com/natydipa-max/pytest-dummyjson-api/actions/workflows/test.yml)

## Overview

API test automation framework built with Python and Pytest, targeting the [DummyJSON](https://dummyjson.com) public API.

The framework covers authentication workflows, CRUD operations for the `/products` endpoint, and comprehensive test scenarios for the `/users` endpoint, including retrieval, pagination, search, filtering, sorting, field selection, and related resources.

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
│       │       ├── user_update_request_model.py      # PUT request body
│       │       └── current_user_model.py             # Authenticated user schema
│       ├── carts/
│       │       ├── cart_model.py                     # GET response schema
│       │       ├── carts_response_model.py           # GET list response schema
│       │       ├── cart_product_model.py             # Nested product schema for GET responses
│       │       ├── cart_item_request_model.py        # Nested product request schema
│       │       ├── create_cart_request_model.py      # POST request body
│       │       ├── created_cart_model.py             # POST response schema
│       │       └── created_cart_product_model.py     # Nested product schema for POST responses
│       ├── posts/
│       │       ├── post_model.py                     # Individual post schema
│       │       └── posts_response_model.py           # GET list response schema
│       ├── todos/
│       │       ├── todo_model.py                     # Individual todo schema
│       │       └── todos_response_model.py           # GET list response schema
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
│   │   ├── test_sort_users.py
│   │   ├── test_search_users.py
│   │   ├── test_select_user.py
│   │   ├── test_filter_user.py
│   │   ├── test_create_user.py
│   │   ├── test_delete_user.py
│   │   ├── test_update_user.py
│   │   ├── test_get_user_carts.py
│   │   ├── test_get_user_posts.py
│   │   ├── test_get_user_todos.py
│   │   └── test_negative_users.py
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

| Method | Endpoint          | Covered Scenarios                                                          |
| ------ | ----------------- |----------------------------------------------------------------------------|
| GET    | /users            | Retrieval, pagination, boundary values, sorting, field selection           |
| GET    | /users/{id}       | Valid ID, invalid ID, nonexistent ID                                       |
| GET    | /users/search     | Search, partial matching, empty query, empty results                       |
| GET    | /users/filter     | Supported fields, nested fields, empty results, missing parameters         |
| GET    | /users/{id}/carts | Valid user, invalid ID format, nonexistent user, response schema validation |
| GET    | /users/{id}/posts | Valid user, invalid ID format, nonexistent user, response schema validation |
| GET    | /users/{id}/todos | Valid user, invalid ID format, nonexistent user, response schema validation |
| POST   | /users/add        | Valid creation, malformed JSON                                             |
| PUT    | /users/{id}       | Successful update, partial update, invalid ID format, nonexistent ID       |
| DELETE | /users/{id} | Successful deletion, nonexistent ID                                        |


### Carts

| Method | Endpoint | Covered Scenarios |
|--------|----------|-------------------|
| GET | `/carts` | Retrieve all carts, pagination (`limit`/`skip`), boundary values |
| GET | `/carts/{id}` | Valid ID, invalid ID format, nonexistent ID |
| GET | `/carts/user/{id}` | Valid user, nonexistent user |
| POST | `/carts/add` | Valid creation, multiple products, single product, invalid product, malformed JSON, missing userId, empty products, nonexistent user |

---

## Live Data Dependency

This framework runs against the real `dummyjson.com` API, with no mocking or stubbing layer (see `docs/testing_strategy.md`). This is a deliberate design choice, not an oversight — but it has a direct consequence: some tests assert on specific seed data rather than just on response shape.

The clearest example is `test_get_users_pagination` in `tests/users/test_get_users.py`, which asserts a fixed `expected_first_id` for a given `skip` value (e.g. `skip=10 → id=11`). This assumes the underlying `/users` dataset keeps a stable order and doesn't get reseeded or resized.

If dummyjson ever reorders or resets its seed data, these tests will fail — that failure reflects a change in the external dataset, not a bug in this framework. When debugging a failure here, check whether the assumed dataset shape still holds before assuming a regression.

---

## Validation Strategy

All tests follow a consistent three-step approach:

1. **Status code** — assert the expected HTTP status code
2. **Schema** — validate the response body using Pydantic models
3. **Business rules** — assert endpoint-specific behavior

Response contracts are validated using dedicated Pydantic models organized by domain (`auth`, `products`, `users`, `carts`, `posts`, and `todos`).

- `ProductModel` — individual product returned by GET endpoints
- `ProductsResponseModel` — paginated response returned by `GET /products`
- `ProductRequestModel` — request payload used by `POST /products/add` and `PUT /products/{id}`
- `ProductCreateResponseModel` — response returned by `POST /products/add`
- `ProductDeleteResponseModel` — response returned by `DELETE /products/{id}`, including `isDeleted` and `deletedOn`
- `UserModel` — individual user returned by GET endpoints
- `UsersResponseModel` — paginated response returned by `GET /users` and `GET /users/search`
- `UserRequestModel` — request payload used by `POST /users/add` and `PUT /users/{id}`
- `UserCreateResponseModel` — response returned by `POST /users/add`
- `LoginResponseModel` — response returned by `POST /auth/login`
- `CurrentUserModel` — authenticated user returned by `GET /auth/me`
- `ErrorResponseModel` — error response returned by 4xx endpoints
- `CartModel` — individual cart returned by GET endpoints
- `CartsResponseModel` — paginated response returned by `GET /carts`
- `CreateCartRequestModel` — request payload used by `POST /carts/add`
- `CreatedCartModel` — response returned by `POST /carts/add`
- `PostModel` — individual post returned by GET endpoints
- `PostsResponseModel` — paginated response returned by `GET /posts`
- `TodoModel` — individual todo item returned by GET endpoints
- `TodosResponseModel` — paginated response returned by `GET /todos`

---

## Test Summary

The framework currently covers:

- Authentication workflows
- Product CRUD operations
- User retrieval and related resources
- Cart retrieval and creation workflows
- Response schema validation using Pydantic
- Negative testing scenarios
- Exploratory API behavior validation

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

### PUT /users/{id}

Partial updates preserve unspecified fields.

For example:

```json
{
  "lastName": "Updated"
}
```

updates only the `lastName` field while preserving all other existing user attributes.

This behavior was verified through exploratory testing and is covered by automated tests.

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

---

### Pagination behavior

The endpoint supports pagination through the `limit` and `skip` query parameters.

Observed behaviors:

- `limit=0` returns all users.
- A `limit` value greater than the total number of users returns all available users.
- A `skip` value beyond the total number of users returns an empty `users` array.

Examples:

```bash
# Returns all users
curl "https://dummyjson.com/users?limit=0"

# Returns all remaining users when limit exceeds total
curl "https://dummyjson.com/users?limit=1000"

# Returns an empty list when skip is beyond total
curl "https://dummyjson.com/users?skip=1000"
```

---

### Sorting

The endpoint supports sorting results using the `sortBy` and `order` query parameters.

Supported order values:

- `order=asc` — ascending order
- `order=desc` — descending order

Example:

```bash
curl "https://dummyjson.com/users?sortBy=firstName&order=asc"
```

#### Observed behavior

Exploratory testing showed that:

- Valid `sortBy` fields are applied correctly.
- Unknown `sortBy` values are ignored and the endpoint returns the default user list (`HTTP 200`).
- `order` only accepts `asc` or `desc`.
- Any other value returns `400 Bad Request` with the following message:

```json
{
  "message": "Invalid 'order' - should be either 'asc' or 'desc'"
}
```

---

### Field selection

The endpoint supports selecting specific fields through the `select` query parameter.

Example:

```bash
curl "https://dummyjson.com/users?select=firstName,age"
```

#### Observed behavior

Exploratory testing showed that:

- Requested valid fields are returned.
- The `id` field is always included in the response.
- Unknown fields are silently ignored.

#### Observed behavior

The API always includes the `id` field in the response, even when it is not explicitly requested.

Example response:

```json
{
  "users": [
    {
      "id": 1,
      "firstName": "Emily",
      "age": 28
    }
  ]
}
```
---

### GET /carts

Pagination behaves consistently with the Users endpoint.

Observed behavior:

- `limit=0` returns all available carts.
- `limit` greater than the total returns all available carts.
- `skip` beyond the available data returns an empty list with HTTP 200.

These behaviors were validated and covered by automated tests.

---

### POST /carts/add

Observed behavior:

- Invalid product IDs are ignored and the cart is created without those products.
- Empty product arrays are accepted.
- Missing userId returns an error response.


> **Note:** The behaviors documented in this section were verified through exploratory testing and reflect the current implementation of the DummyJSON API.

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