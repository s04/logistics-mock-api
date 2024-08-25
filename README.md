# Items and Orders API

This project is a FastAPI-based API for managing items and orders in an e-commerce system. It uses SQLite as the database and is containerized using Docker.

## Prerequisites

- A Hetzner VPS with Ubuntu 20.04 or later
- SSH access to your VPS
- Docker installed on your VPS

## Setup Instructions

1. SSH into your Hetzner VPS:
   ```
   ssh username@your_server_ip
   ```

2. Update the system and install Docker (if not already installed):
   ```
   sudo apt update
   sudo apt upgrade -y
   sudo apt install docker.io -y
   ```

3. Start and enable Docker:
   ```
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. Clone the repository (replace with your actual repository URL):
   ```
   git clone https://github.com/yourusername/items-orders-api.git
   cd items-orders-api
   ```

5. Build the Docker image:
   ```
   sudo docker build -t items-orders-api .
   ```

6. Run the Docker container, exposing it on port 9000:
   ```
   sudo docker run -d -p 9000:80 --name items-orders-api items-orders-api
   ```

7. Configure the firewall to allow traffic on port 9000:
   ```
   sudo ufw allow 9000/tcp
   sudo ufw reload
   ```

## Testing the API

You can now access the API from outside the server using the following URL:

```
http://your_server_ip:9000
```

Replace `your_server_ip` with the actual IP address of your Hetzner VPS.

To access the OpenAPI documentation and test the endpoints, visit:

```
http://your_server_ip:9000/docs
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
sudo docker stop items-orders-api
```

To remove the container:

```
sudo docker rm items-orders-api
```

## Updating the API

To update the API with new changes:

1. Pull the latest changes from your repository
2. Rebuild the Docker image:
   ```
   sudo docker build -t items-orders-api .
   ```
3. Stop and remove the old container:
   ```
   sudo docker stop items-orders-api
   sudo docker rm items-orders-api
   ```
4. Run a new container with the updated image:
   ```
   sudo docker run -d -p 9000:80 --name items-orders-api items-orders-api
   ```

## Troubleshooting

- If you can't access the API, ensure that port 9000 is open in your Hetzner VPS firewall settings.
- Check the Docker logs for any errors:
  ```
  sudo docker logs items-orders-api
  ```

For any other issues or questions, please open an issue in the GitHub repository.