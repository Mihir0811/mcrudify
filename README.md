# MCRUDify

 mcrudify is a Python library that simplifies performing CRUD (Create, Read, Update, Delete) operations on both SQL (SQLite, MySQL, PostgreSQL) and MongoDB databases using Flask. It allows developers to integrate easy-to-use CRUD functionality into their applications, with minimal configuration.

 =======================================================================================================================================================

 ## Features

- **CRUD Operations for SQL (SQLite, MySQL, PostgreSQL)**: Supports common relational databases using SQLAlchemy.
- **CRUD Operations for MongoDB**: Seamlessly integrates with MongoDB.
- **Dynamic CRUD Routes**: Automatically generates RESTful routes for CRUD operations.
- **Database Abstraction**: Abstracts database interactions so that you can focus on your application logic.

 =======================================================================================================================================================


## Creator Information

- **Creator** : Mihir Sudani

- **Email** : mihirsudani128@gmail.com

- **GitHub** : https://github.com/Mihir0811/mcrudify

- **Description** : mcrudify was created by Mihir to simplify the integration of CRUD operations into Flask applications. The library supports both SQL and NoSQL databases and allows developers to focus on application logic without worrying about repetitive CRUD implementations.

 =======================================================================================================================================================

## Installation

- You can install the mcrudify library using pip:

```bash

pip install mcrudify

```
 =======================================================================================================================================================

## Requirements

- Python 3.6+

- Flask

- SQLAlchemy (for SQL databases)

- PyMongo (for MongoDB)

 =======================================================================================================================================================

--------------------------------------------
## 1. Set up a Flask application            
--------------------------------------------

from flask import Flask
from mcrudify import MCRUDify

app = Flask(__name__)

# Initialize the MCRUDify library
crudify = MCRUDify(app, db_uri="sqlite:///mydatabase.db", db_type="sqlite")

# Register a table (SQL) or MongoDB collection
table = crudify.register_table("users", {"name": "string", "age": "integer"})

# Register CRUD routes for the 'users' resource
crudify.register_crud_routes("users", table)

if __name__ == "__main__":
    app.run(debug=True)


--------------------------------------------
## 2. Perform CRUD Operations
--------------------------------------------


# Create a record (POST request):

- **Endpoint** : /users
- **Request body** :
    {
        "name": "John Doe",
        "age": 30
    }

***********************************

# Read records (GET request):

- **Endpoint** :  /users

***********************************

# Update a record (PUT request):

- **Endpoint** : /users/<int:record_id>
- **Request body** :
    {
        "name": "John Doe",
        "age": 25
    }

***********************************

# Delete a record (DELETE request):

- **Endpoint** : /users/<int:record_id>

 =======================================================================================================================================================

## Example Request

- Here is how you might create a new record using curl:
```bash

curl -X POST http://localhost:5000/users \
    -H "Content-Type: application/json" \
    -d '{"name": "John Doe", "age": 30}'

```
 =======================================================================================================================================================

## Configuration

- You can configure the database URI and database type during the initialization of MCRUDify. The supported database types are:

- **sqlite**

- **mysql**

- **postgres**

- **mongodb**

 =======================================================================================================================================================

# Example for MySQL:

- crudify = MCRUDify(app, db_uri="user:password@localhost/mydatabase", db_type="mysql")

*****************************************************************************************************

# Example for MongoDB:

- crudify = MCRUDify(app, db_uri="mongodb://localhost:27017/mydatabase", db_type="mongodb")

 =======================================================================================================================================================

## License

- This project is licensed under the MIT License - see the LICENSE file for details.

 =======================================================================================================================================================

## Contributing

1. Fork the repository.

2. Create your feature branch (git checkout -b feature-name).

3. Commit your changes (git commit -m 'Add new feature').

4. Push to the branch (git push origin feature-name).

5. Open a pull request.







