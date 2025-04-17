from flask import Flask, request, jsonify
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float
from sqlalchemy.exc import SQLAlchemyError
from pymongo import MongoClient
from bson import ObjectId

class MCRUDify:
    def __init__(self, app=None, db_uri=None, db_type="sqlite"):
        """
        Initialize the MCRUDify class with app, database URI, and database type.
        Supported database types: 'sqlite', 'mysql', 'postgres', 'mongodb'.
        """
        self.app = app
        self.db_type = db_type
        self.db_uri = db_uri
        self.metadata = MetaData()
        self.engine = None
        self.mongo_client = None
        self.db = None

        if db_type in ["sqlite", "mysql", "postgres"]:
            self.engine = self._initialize_sql_engine()
        elif db_type == "mongodb":
            self.mongo_client = MongoClient(self.db_uri)
            self.db = self.mongo_client.get_database()
        else:
            raise ValueError("Unsupported database type. Choose 'sqlite', 'mysql', 'postgres', or 'mongodb'.")

    def _initialize_sql_engine(self):
        """
        Create a SQLAlchemy engine based on the database type and URI.
        """
        if self.db_type == "sqlite":
            return create_engine(f"sqlite:///{self.db_uri}")
        elif self.db_type == "mysql":
            return create_engine(f"mysql+pymysql://{self.db_uri}")
        elif self.db_type == "postgres":
            return create_engine(f"postgresql://{self.db_uri}")
        else:
            raise ValueError("Unsupported SQL database type.")

    def register_table(self, table_name, schema):
        """
        Register a table in the database based on the given schema.
        """
        if self.db_type == "mongodb":
            return self.db[table_name]  # Return MongoDB collection
        else:
            # SQL tables
            columns = [Column("id", Integer, primary_key=True, autoincrement=True)]
            for column_name, column_type in schema.items():
                columns.append(Column(column_name, self._get_column_type(column_type)))
            table = Table(table_name, self.metadata, *columns)
            self.metadata.create_all(self.engine)
            return table

    def _get_column_type(self, column_type):
        """
        Map schema data types to SQLAlchemy types.
        """
        mapping = {
            "integer": Integer,
            "string": String,
            "float": Float
        }
        return mapping.get(column_type, String)  # Default to String if type is unknown

    # CRUD Operations for SQL
    def create_record(self, table, data):
        """
        Insert a new record into the SQL table and return the inserted row as a dictionary.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(table.insert().values(data))
                inserted_id = result.inserted_primary_key[0]  # Get the inserted ID
                conn.commit()  # Ensure transaction is committed
                return {"message": "Record added successfully", "id": inserted_id}, 201
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    def read_records(self, table):
        """
        Retrieve all records from the SQL table.
        Convert Row objects to dictionaries for JSON serialization.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(table.select())
                records = [dict(row._mapping) for row in result]  # Convert Row objects to dicts
            return records
        except SQLAlchemyError as e:
            return jsonify({"error": str(e)}), 500

    def update_record(self, table, record_id, data):
        """
        Update an existing record in the SQL table by ID.
        """
        try:
            with self.engine.begin() as conn:
                # print(record_id)
                # print(data)
                result = conn.execute(table.update().where(table.c.id == record_id).values(**data))
                # print(f"Row count: {result.rowcount}")
                if result.rowcount == 0:
                    return {"message": "Record not found"}, 404
            return {"message": "Record updated successfully"}, 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    def delete_record(self, table, record_id):
        """
        Delete a record from the SQL table by ID.
        """
        try:
            with self.engine.begin() as conn:
                result = conn.execute(table.delete().where(table.c.id == record_id))
                if result.rowcount == 0:
                    return {"message": "Record not found"}, 404
            return {"message": "Record deleted successfully"}, 200
        except SQLAlchemyError as e:
            return {"error": str(e)}, 500

    # CRUD Operations for MongoDB
    def create_mongo_record(self, collection, data):
        """
        Insert a new record into a MongoDB collection.
        """
        try:
            print(data)
            result = collection.insert_one(data)
            print(f"Inserted ID: {result.inserted_id}")
            
            return {"message": "Record added successfully", "id": str(result.inserted_id)}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def read_mongo_records(self, collection):
        """
        Retrieve all records from the MongoDB collection.
        """
        try:
            result = collection.find()
            # records = [{"id": str(record["_id"]), **record} for record in result]
            records = [{**record, "id": str(record["_id"])} for record in result]
            for record in records:
                record.pop("_id")
            return jsonify(records), 200
        except Exception as e:
            return {"error": str(e)}, 500

    def update_mongo_record(self, collection, record_id, data):
        """
        Update an existing record in the MongoDB collection by ID.
        """
        try:
            result = collection.update_one({"_id": ObjectId(record_id)}, {"$set": data})
            if result.matched_count == 0:
                return {"message": "Record not found"}, 404
            return {"message": "Record updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def delete_mongo_record(self, collection, record_id):
        """
        Delete a record from the MongoDB collection by ID.
        """
        try:
            result = collection.delete_one({"_id": ObjectId(record_id)})
            if result.deleted_count == 0:
                return {"message": "Record not found"}, 404
            return {"message": "Record deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    # Register CRUD Routes for SQL or MongoDB
    def register_crud_routes(self, resource_name, table_or_collection, permissions=None):
        """
        Register CRUD routes dynamically for a SQL table or MongoDB collection based on user permissions.
        Permissions could be a list like ['create', 'read', 'update', 'delete'].
        """
        if permissions is None:
            permissions = ['create', 'read', 'update', 'delete']  # Default: All permissions

        # Create route
        if 'create' in permissions:
            @self.app.route(f"/{resource_name}", methods=["POST"])
            def create():
                data = request.json
                if self.db_type == "mongodb":
                    return self.create_mongo_record(table_or_collection, data)
                return self.create_record(table_or_collection, data)

        # Read route
        if 'read' in permissions:
            @self.app.route(f"/{resource_name}", methods=["GET"])
            def read_all():
                if self.db_type == "mongodb":
                    return self.read_mongo_records(table_or_collection)
                return self.read_records(table_or_collection)

        # Update route
        if 'update' in permissions:
            @self.app.route(f"/{resource_name}/<int:record_id>", methods=["PUT"])
            def update(record_id):
                data = request.json
                if self.db_type == "mongodb":
                    return self.update_mongo_record(table_or_collection, record_id, data)
                return self.update_record(table_or_collection, record_id, data)

        # Delete route
        if 'delete' in permissions:
            @self.app.route(f"/{resource_name}/<int:record_id>", methods=["DELETE"])
            def delete(record_id):
                if self.db_type == "mongodb":
                    return self.delete_mongo_record(table_or_collection, record_id)
                return self.delete_record(table_or_collection, record_id)

    def get_user_by_id(self, table, user_id):
        """
        Fetch a user from the database by user_id.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(table.select().where(table.c.id == user_id))
                user = result.fetchone()  # Fetch the first matching record
                if user:
                    return dict(user._mapping)  # Return user as a dictionary
                return None  # Return None if no user is found
        except SQLAlchemyError as e:
            return {"error": str(e)}


