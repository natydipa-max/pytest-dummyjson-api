# Pytest DummyJSON API Framework

## Overview

## Tech Stack

## Architecture

## Validation Strategy

All API tests follow the same validation approach:

1. Assert status code
2. Validate schema if response has body
3. Assert business rule if applicable

Examples:

- GET /products/{id}
    - Assert 200 OK
    - Validate Product schema
    - Assert returned product id

- POST /products
    - Assert 201 Created
    - Validate Product response schema
    - Assert returned values match request data

- DELETE /products/{id}
    - Assert 200 OK
    - Validate response schema if a response body exists
    - Assert deletion-specific business rules if applicable

## API Coverage

## Exploratory Findings