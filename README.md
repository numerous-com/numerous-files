# Numerous Files

The purpose of this package is to make a simple way to interface both with AWS S3 buckets, an in-memory file storage and a local file storage. The idea is to have a common inteface where the backend can be changed transperently without making code changes. 

Simply use the factory method to get a file manager instance. You can control which file manager will be used by setting the env variable NUMEROUS-FILES-BACKEND to either IN-MEMORY to use the memory based file system or AWS_S3 to use an S3 bucket on AWS.

## AWS Backend

To save files on AWS S3 a bucket and a base prefix is needed to be specified using the env variables NUMEROUS_FILES_BUCKET and NUMEROUS_FILES_BASE_PREFIX.

## In Memory Backend

The in-memory backend does not need any configuration. Please be aware all files stored in the in-memory backend will not be persisted.