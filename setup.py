from setuptools import setup, find_packages

setup(
    name="mcrudify",
    version="1.0.0",
    author="Mihir Sudani",
    author_email="mihirsudani128@gmail.com",
    description="A simple Python library for CRUD operations in Flask applications with support for SQL and MongoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mihir0811/mcrudify",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "SQLAlchemy",
        "PyMongo",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
