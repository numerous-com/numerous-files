# Welcome to Numerous Files

The purpose of this package is to make a simple way to interface with both cloud, local and in-memory file storage to support a development and production workflow for web applications needing file storage. The idea is to have a common inteface where the backend can be changed without making code changes by setting env variables. In this way local development and testing can use in-memory or local file storage, eventually run tests with a cloud file storage provider and use cloud file storage in production.

Simply use the factory method to get a file manager instance. You can control which file manager will be used by setting the env variable `NUMEROUS_FILES_BACKEND` to either `IN-MEMORY` to use the memory based file system, `LOCAL` to use a local folder, or `AWS_S3` to use an S3 bucket on AWS.

## Installation

Install the package using pip:

```bash
pip install numerous-files
```

## Usage

Use `file_manager_factory` to get a file manager configured based on the current environment.

```python
from numerous.files import file_manager_factory

file_manager = file_manager_factory()
```

Use `file_manager_factory` to upload and download files.
```python
# put a local file to file manager
file_manager.put("my_local_file.txt", "folder/and_name_on_file_backend.txt")

# get the file just put
file_manager.get("folder/and_name_on_file_backend.txt", "name_i_want_the_file_to_have_locally")
```

To list, copy, move and remove files.
```python
# list files in the file_managers backend
file_manager.list()

# Optionally add a subfolder to list files from
file_manger.list("my_folder")

# Remove a file
file_manager.remove("my_file.txt")

# Copy a file
file_manager.copy("from/my_file.txt","to/my_copy.txt")

# Move a file
file_manager.copy("from/my_file.txt","to/my_copy.txt")
```

## AWS Backend

You can use the AWS backend if you have an AWS account. 

To save files on AWS S3 a bucket (need to be created before using `file_manager`) and a base prefix is needed to be specified using the env variables `NUMEROUS_FILES_BUCKET` and `NUMEROUS_FILES_BASE_PREFIX`.

In order for the file_manager to access your files on aws, you need to provide authentication to access AWS.

### AWS authentication

If you set the env variables `NUMEROUS_FILES_AWS_ACCESS_KEY` and `NUMEROUS_FILES_AWS_SECRET_KEY` with your aws credentials they will be used to authenticate. In case these env variables are not set the client will authenticate with the AWS credentials from your environment.

If needed you can supply the names of the env variables you use to store information of the bucket, base_prefix, aws_access and aws_secrets to the file_manager_factory method as the following key word arguments: bucket, base_prefix, aws_access_key_id, and aws_secret_access_key.

## In Memory Backend

The in-memory backend does not need any configuration. Please be aware, files stored in the in-memory backend will not be persisted.

## Local Backend

For the local backend you can configure the base folder for the file manager from where all paths will be relative. You set the workfolder by using the `workfolder` keyword when using the factory method.

# Documentation
For a more complete documentation of `numerous-files` please visit [numerous-files-docs](https://numerous-files.readthedocs.io/en/latest/) on readthedocs.
