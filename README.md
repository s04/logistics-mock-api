# Logistics Mock API

This project is a FastAPI-based mock API for logistics operations. It uses SQLite as the database and is containerized using Docker.

## Prerequisites

- Docker
- Make (optional, for using the Makefile commands)

## Local Development Setup

1. Clone the repository:
   ```
   git clone https://github.com/s04/logistics-mock-api.git
   cd logistics-mock-api
   ```

2. Build the Docker image:
   ```
   make build
   ```
   or
   ```
   docker build -t logistics-mock-api .
   ```

3. Run the Docker container:
   ```
   make run
   ```
   or
   ```
   docker run -d -p 8000:80 --name logistics-mock-api-local logistics-mock-api
   ```

4. The API will now be accessible at `http://localhost:8000`

## Makefile Commands

This project includes a Makefile to simplify common development tasks. Here are the available commands:

- `make build`: Build the Docker image
- `make run`: Run the Docker container
- `make stop`: Stop the Docker container
- `make clean`: Stop and remove the Docker container
- `make restart`: Rebuild and restart the Docker container
- `make logs`: Show container logs
- `make shell`: Enter the container shell
- `make test`: Run tests (if configured)
- `make help`: Show all available make commands

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

## Testing the API

You can access the OpenAPI documentation and test the endpoints by visiting:

```
http://localhost:8000/docs
```

## Deployment on Hetzner VPS

For deploying this API on a Hetzner VPS, follow these steps:

1. SSH into your Hetzner VPS:
   ```
   ssh username@your_server_ip
   ```

2. Install Docker following the official Docker documentation for Ubuntu:
   https://docs.docker.com/engine/install/ubuntu/

3. Start and enable Docker:
   ```
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. Clone the repository and navigate to the project directory.

5. Build and run the Docker container:
   ```
   sudo docker build -t logistics-mock-api .
   sudo docker run -d -p 80:80 --name logistics-mock-api logistics-mock-api
   ```

6. Configure the firewall to allow traffic on port 80 (HTTP):
   ```
   sudo ufw allow 80/tcp
   sudo ufw reload
   ```

The API will now be accessible at `http://your_server_ip`

## Updating the API

To update the API with new changes:

1. Pull the latest changes from the repository:
   ```
   git pull origin main
   ```

2. Rebuild and restart the container:
   ```
   make restart
   ```
   or
   ```
   sudo docker stop logistics-mock-api
   sudo docker rm logistics-mock-api
   sudo docker build -t logistics-mock-api .
   sudo docker run -d -p 80:80 --name logistics-mock-api logistics-mock-api
   ```

## Troubleshooting

- If you can't access the API, ensure that the correct port is open in your firewall settings.
- Check the Docker logs for any errors:
  ```
  make logs
  ```
  or
  ```
  sudo docker logs logistics-mock-api
  ```

For any other issues or questions, please open an issue in the GitHub repository.

## Security Considerations

For production use, consider the following:

1. Set up HTTPS using a reverse proxy like Nginx and Let's Encrypt for SSL/TLS certificates.
2. Implement proper authentication and authorization mechanisms in your API.
3. Regularly update your server and Docker images to patch any security vulnerabilities.
4. Consider using a Web Application Firewall (WAF) for additional protection.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
