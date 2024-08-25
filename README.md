# Logistics Mock API

This project is a FastAPI-based mock API for logistics operations. It uses SQLite as the database and is containerized using Docker.

## Prerequisites

- A Hetzner VPS with Ubuntu 20.04 or later
- SSH access to your VPS
- Docker installed on your VPS

## Setup Instructions

1. SSH into your Hetzner VPS:
   ```
   ssh username@your_server_ip
   ```

2. Install Docker following the official Docker documentation for Ubuntu:
   https://docs.docker.com/engine/install/ubuntu/

   Follow the steps in the "Install using the repository" section, which includes:
   - Updating the apt package index
   - Installing packages to allow apt to use a repository over HTTPS
   - Adding Docker's official GPG key
   - Setting up the stable repository
   - Installing Docker Engine

3. Start and enable Docker:
   ```
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. Clone the repository:
   ```
   git clone https://github.com/s04/logistics-mock-api.git
   cd logistics-mock-api
   ```

5. Build the Docker image:
   ```
   sudo docker build -t logistics-mock-api .
   ```

6. Run the Docker container, exposing it on port 80:
   ```
   sudo docker run -d -p 80:80 --name logistics-mock-api logistics-mock-api
   ```

7. Configure the firewall to allow traffic on port 80 (HTTP):
   ```
   sudo ufw allow 80/tcp
   sudo ufw reload
   ```

   Note: If you haven't already allowed SSH access, make sure to do so:
   ```
   sudo ufw allow 22/tcp
   ```

## Testing the API

You can now access the API from outside the server using the following URL:

```
http://your_server_ip
```

Replace `your_server_ip` with the actual IP address of your Hetzner VPS or your domain name if you've set up DNS.

To access the OpenAPI documentation and test the endpoints, visit:

```
http://your_server_ip/docs
```

## API Endpoints

- `GET /items`: List all items
- `POST /items`: Create a new item
- `GET /items/{item_id}`: Get a specific item
- `PUT /items/{item_id}`: Update an item
- `DELETE /items/{item_id}`: Delete an item
- `GET /orders`: List all orders
- `POST /orders`: Create a new order
- `GET /orders/{order_id}`: Get a specific order
- `PUT /orders/{order_id}`: Update an order
- `DELETE /orders/{order_id}`: Delete an order

## Stopping and Removing the Container

To stop the container:

```
sudo docker stop logistics-mock-api
```

To remove the container:

```
sudo docker rm logistics-mock-api
```

## Updating the API

To update the API with new changes:

1. Pull the latest changes from the repository:
   ```
   git pull origin main
   ```
2. Rebuild the Docker image:
   ```
   sudo docker build -t logistics-mock-api .
   ```
3. Stop and remove the old container:
   ```
   sudo docker stop logistics-mock-api
   sudo docker rm logistics-mock-api
   ```
4. Run a new container with the updated image:
   ```
   sudo docker run -d -p 80:80 --name logistics-mock-api logistics-mock-api
   ```

## Troubleshooting

- If you can't access the API, ensure that port 80 is open in your Hetzner VPS firewall settings.
- Check the Docker logs for any errors:
  ```
  sudo docker logs logistics-mock-api
  ```
- If you're using a domain name and it's not working, check your DNS settings to ensure they're pointing to the correct IP address.

For any other issues or questions, please open an issue in the GitHub repository: https://github.com/s04/logistics-mock-api

## Security Considerations

Running a service on port 80 exposes it to the public internet. For production use, consider the following:

1. Set up HTTPS using a reverse proxy like Nginx and Let's Encrypt for SSL/TLS certificates.
2. Implement proper authentication and authorization mechanisms in your API.
3. Regularly update your server and Docker images to patch any security vulnerabilities.
4. Consider using a Web Application Firewall (WAF) for additional protection.