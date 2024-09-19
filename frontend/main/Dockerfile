# Use an official Node.js image as the base image
FROM node:18 AS build

# Define build-time arguments with default values
# Required to override values when using docker-compose.yaml file
ARG VITE_BACKEND_API_URL=http://localhost:5000
ENV VITE_BACKEND_API_URL=$VITE_BACKEND_API_URL

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the entire project into the working directory
COPY . .

# Build the React app
RUN npm run build

# Use a lightweight web server to serve the static files
FROM nginx:alpine

# Copy the custom Nginx configuration file
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy the build directory from the previous stage to the nginx container
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for the web server
EXPOSE 80

# Start the nginx server
CMD ["nginx", "-g", "daemon off;"]
