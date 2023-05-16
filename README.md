# API Documentation

This documentation provides an overview of the endpoints available in the API created with Django and Django REST framework. It describes each endpoint, its purpose, and the parameters that can be used for filtering the results. The API allows you to interact with the following resources: **Brand**, **Category**, and **Product**.

---

### This API is intended for use by French-speaking users

---

## Base URL

The base URL for all API endpoints is `https://my-api-url.com/`.

## Endpoints

### Brand

#### `GET /api/brand/`

Retrieve a list of brands.

##### Parameters

- `name` (optional): Filter brands by name. Only brands containing the specified name will be returned.

### Category

#### `GET /api/category/`

Retrieve a list of categories.

##### Parameters

- `name` (optional): Filter categories by name. Only categories containing the specified name will be returned.

### Product

#### `GET /api/product/`

Retrieve a list of products.

##### Parameters

- `ean` (optional): Filter products by EAN (European Article Number) code. Only products with the exact EAN code will be returned.

- `name` (optional): Filter products by name. Only products containing the specified name will be returned.

- `brand` (optional): Filter products by brand name. Only products from the specified brand will be returned.

- `categories` (optional): Filter products by a list of category names. Only products belonging to any of the specified categories will be returned. Multiple category names can be provided by separating them with commas.

## Examples

Here are some examples of how to use the API endpoints:

- Retrieve a list of all brands:
  - `GET /api/brand/`

- Retrieve a list of brands containing the name "Danone":
  - `GET /api/brand/?name=Danone`

- Retrieve a list of all categories:
  - `GET /api/category/`

- Retrieve a list of categories containing the name "Produits laitiers":
  - `GET /api/category/?name=Produits laitiers`

- Retrieve a list of all products:
  - `GET /api/product/`

- Retrieve a product with a specific EAN code:
  - `GET /api/product/?ean=1234567890123`

- Retrieve products containing the name "Actimel":
  - `GET /api/product/?name=Actimel`

- Retrieve products from the brand "Danone":
  - `GET /api/product/?brand=Danone`

- Retrieve products belonging to the categories "Produits laitiers" and "Desserts":
  - `GET /api/product/?categories=Produits laitiers,Desserts`

Please note that the API supports pagination, limiting the number of results to 25 per request.

## Additional Endpoint

### `POST /api/insert-data/`

Populate the database with data from a CSV file. This endpoint is only accessible to superusers.

- Use this endpoint to populate the database with data from a CSV file. The CSV file should be uploaded as part of the request.

- This endpoint is accessible at `/api/insert-data/`.

- Please ensure that you have the necessary permissions to access this endpoint.

---
