# API Test Validation Strategy

The framework follows a three-step validation approach:

## 1. Status Code Validation

Verify that the API returns the expected HTTP status code.

## 2. Schema Validation

Validate the response contract using Pydantic models when a response body exists.

## 3. Business Rule Validation

Verify endpoint-specific business behavior.

Examples:

- Product id matches requested id
- Created product contains submitted values
- Deleted resource is marked as deleted