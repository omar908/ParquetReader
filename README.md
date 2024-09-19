# Parquet Reader Application

This application consists of a backend built with Pyton, Flask, DuckDB. Also a frontend built with React, TypeScript, and Vite. 


## Features

- **Upload Parquet Files**: Allows users to upload parquet files to the backend.
- **View Uploaded Files**: Displays a list of existing uploaded files.
- **Read Parquet Files**: Parses and displays parquet file contents in the browser using DuckDB.

## Getting Started

### Pre-requisites
To run the application, you'll need `Docker` and `Docker Compose` installed on your system.

### Docker Compose Setup

1. **Clone the Repository**:

   ```bash
   git clone git@github.com:omar908/ParquetReader.git
   cd ParquetReader
   ```

2. **Start the Application**:

   Use Docker Compose to build and start the services:

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images for the backend and frontend, then start the services. By default, the application will be available at `http://localhost:80` for the frontend and `localhost:5000` for the backend.

4. **Access the Application**:

   Open your browser and navigate to `http://localhost:80` to use the application.

## Dockerfiles and Docker Compose

### Docker Compose Configuration

The `docker-compose.yaml` file defines the services for both the frontend and backend.


### Dockerfile(s) for Frontend

The frontend Dockerfile includes configurations for both docker-compose and standalone usage.

**Standalone Dockerfile**

If you want to run the frontend container standalone (not through Docker Compose), use the following `Dockerfile.standalone`, please note that CORS errors will occur with this approach in the browser.

**Dockerfile (docker-compose)**

The difference between `Dockerfile` file vs the `Dockerfile.standalone`, is we add the capability to override the base API url environment value through docker compose. Additionaly we copy over ngnix conf file to proxy the calls to the backend container.

Here's a `README-Endpoints.md` that documents the available endpoints for your Flask backend:

### Dockerfile for backend

**Dockerfile (docker-compose and standalone)**
There is only one Dockerfile for the backend which can be used for both docker-compose and for a standalone container. Which uses the base image of `continuumio/miniconda3` to install dependencies and run the flask app.

## Endpoints

>Note: There is a Insomnia JSON Collection for these endpoints in the repo called `ParquetReader_Insomnia_Collection.json` which can be used to import the endpoints

### 1. **List Uploaded Parquet Files**

- **Endpoint**: `/file/parquet/list`
- **Method**: `GET`
- **Description**: Returns a list of uploaded parquet files in the `uploads` directory.

### 2. **Search for Parquet File by Filename**

- **Endpoint**: `/file/parquet`
- **Method**: `GET`
- **Query Parameter**:
  - `filename` (required): The name or partial name of the parquet file to search for.
- **Description**: Searches for parquet files by filename and returns the content of the first matching file.

### 3. **Get Sample Parquet Data**

- **Endpoint**: `/file/parquet/sample`
- **Method**: `GET`
- **Description**: Returns the contents of a predefined sample parquet file (`sample1.parquet` found in the `test-data` directory).

### 4. **Upload a Parquet File**

- **Endpoint**: `/file/parquet`
- **Method**: `POST`
- **Description**: Uploads a parquet file and immediately returns its contents.
- **Request Body**:
  - Multipart form-data with the `file` field containing the parquet file.

## Notes

- **Allowed File Types**: The only allowed file extension for upload is `.parquet`.
- **Uploads Directory**: Files are uploaded to the `./uploads` directory by default in the backend directory.
- **DuckDB**: DuckDB is used to parse parquet files and convert the contents into JSON.