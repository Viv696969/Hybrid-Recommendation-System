# Hybrid-Recommendation-System

- access tokens from the idea and approach .txt for login and signup also for testing other apis 
- while sending jwt token send as Bearer __token__string

### 2. **`/store/show_products`**

- **Method:** `POST`
- **Description:** Returns a list of products. Optionally, can filter based on user activity.
- **Data Accepted:**
  ```json
  {
    "activity": "array"  // Optional. Filters products based on activity. should be array of integers keep it a queue with len =5
  }
  ```
- **Response:**
  ```json
  {
    "data": [
      {
        "id": 1,
        "name": "Product Name",
        "description": "Product Description",
        "image_url": "URL to image",
        "price": 100.0
      },
      ...
    ]
  }
  ```
- **Status Codes:**
  - `200 OK`: Successfully retrieved products.


### 4. **`store/show_product`**

- **Method:** `POST`
- **Description:** Retrieves a specific product and its recommendations based on the provided product ID.
- **Data Accepted:**
  ```json
  {
    "product_id": "int"  // ID of the product to retrieve.
  }
  ```
- **Response:**
  ```json
  {
    "product": {
      "id": 1,
      "name": "Product Name",
      "description": "Product Description",
      "image_url": "URL to image",
      "price": 100.0
    },
    "recommended_products": [
      {
        "id": 2,
        "name": "Recommended Product",
        "description": "Description of recommended product",
        "image_url": "URL to image",
        "price": 50.0
      },
      ...
    ]
  }
  ```
- **Status Codes:**
  - `200 OK`: Successfully retrieved product and recommendations.

### 5. **`store/add_to_cart`**

- **Method:** `POST`
- **Description:** Adds a product to the user's cart.
- **Data Accepted:**
  ```json
  {
    "product_id": "int"  // ID of the product to add to cart.
  }
  ```
- **Response:**
  ```json
  {
    "status": true,
    "mssg": "Product Name added to cart."
  }
  ```
- **Status Codes:**
  - `200 OK`: Product was successfully added to cart.
  - `404 Not Found`: Product not found.

### 6. **`store/show_cart`**

- **Method:** `POST`
- **Description:** Retrieves all items in the user's cart.
- **Data Accepted:** None
- **Response:**
  ```json
  {
    "quantity": 2,
    "data": [
      {
        "id": 1,
        "name": "Product Name",
        "description": "Product Description",
        "image_url": "URL to image",
        "price": 100.0,
        "total_price": 200.0
      },
      ...
    ],
    "status": true
  }
  ```
- **Status Codes:**
  - `200 OK`: Successfully retrieved cart items.
  - `404 Not Found`: No items in the cart.

### 7. **`store/place_order`**

- **Method:** `POST`
- **Description:** Places an order for all items in the user's cart and clears the cart.
- **Data Accepted:** None
- **Response:**
  ```json
  {
    "mssg": "Order Placed successfully!",
    "order_id": 123
  }
  ```
- **Status Codes:**
  - `201 Created`: Order was successfully placed.

### 8. **`store/checkout_recommendation`**

- **Method:** `POST`
- **Description:** Provides product recommendations based on the user's activity profile.
- **Data Accepted:**
  ```json
  {
    "activity": "string"  // User's activity.
  }
  ```
- **Response:**
  ```json
  {
    "data": [
      {
        "id": 1,
        "name": "Recommended Product",
        "description": "Description of recommended product",
        "image_url": "URL to image",
        "price": 50.0
      },
      ...
    ]
  }
  ```
- **Status Codes:**
  - `200 OK`: Successfully retrieved recommendations.

### Authentication Endpoints

### 9. **`/authentication/login_user`**

- **Method:** `POST`
- **Description:** Authenticates a user and provides an access token.
- **Data Accepted:**
  ```json
  {
    "uname": "string",     // Username
    "password": "string"  // Password
  }
  ```
- **Response:**
  ```json
  {
    "access": "string"  // Access token
  }
  ```
- **Status Codes:**
  - `200 OK`: Authentication successful.
  - `400 Bad Request`: Incorrect credentials.

### 10. **`/authentication/register_user`**

- **Method:** `POST`
- **Description:** Registers a new user and creates a profile.
- **Data Accepted:**
  ```json
  {
    "uname": "string",       // Username
    "password1": "string",   // Password
    "password2": "string",   // Confirm password
    "name": "string",        // User's full name
    "mobile": "string",      // Mobile number
    "email": "string"        // Email address
  }
  ```
- **Response:**
  ```json
  {
    "mssg": "Profile created Successfully...",
    "status": true,
    "access_token": "string"  // Access token
  }
  ```
- **Status Codes:**
  - `201 Created`: User registration successful.
  - `400 Bad Request`: Invalid input or username already taken.

### URL Configuration

