# Dockerfile Hints

## To build image from Dockerfile and add a `Tag` to it called my-react-vite-app-v1`
`docker build -t python-flask-parquet-backend-v1 .`

## To create a container based upon the created docker image and expose port 80 to local machine
`docker run -p 5000:5000 python-flask-parquet-backend-v1`