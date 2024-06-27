# Inventory Management System (Python🐍)

Features of the Inventory management system:
- 📦 Manage products (Add, Update, Delete and Search) 
- 🔎 Perform a global search on all data based on keyword
- 🔻 List and alert for low stock items
- 📊 Tracks inventory levels and generates reports
- 💾 Persists data in JSON format

## Usage
- Default version (Prioritizes code readability)
```shell
python inventory_management.py
```

- Search optimized version (Optimized for speed)
```shell
python inventory_management_search_optimized.py
```

## Abstract
This Inventory Management System provides a structured approach to manage products within an inventory. It utilizes object-oriented programming principles to define products and manage inventory operations.

The code consist of 2 main classes:
#### Product class
Contains attributes
- ID
- Name
- Price
- Quantity

Further, this class also contains thier getter, setter and type validators
#### Inventory class
Contains attributes
- Items (List of products)
- Low Stock alert threshold
- Filepath to save data

### 1. Default version
Saves data in JSON in the given format:
```json
[
    {
        "_id": "A1",
        "_name": "iPhone 16",
        "_price": 2000.0,
        "_quantity": 20
    },
    {
        "_id": "A2",
        "_name": "Samsung",
        "_price": 1300.0,
        "_quantity": 12
    }
]
```

Time Complexity:
- For all operations including search, add, update, delete: O(n)

Since to perform any operation you have to iterate the list atleast once


### 2. Search optimized version
Saves data in JSON in given format:
```json
{
    "A1": {
        "_id": "A1",
        "_name": "iPhone 16",
        "_price": 2000.0,
        "_quantity": 12
    },
    "A2": {
        "_id": "A2",
        "_name": "Samsung",
        "_price": 1200.0,
        "_quantity": 2
    }
}
```

Time Complexity:
- For search, add, update, delete: O(1)
- For search everywhere, generate reports etc.: O(n)

Since product id is the key for map search by id can be done in O(1)
## Assumptions
- No upper limit to inventory values
- Product Id is unique and non nullable and can be alphanumeric
- Attributes of a product are fixed to id, name, price, quantity (no new attributes can be added)
