# Docker Image CI

This GitHub Actions workflow automates the process of building and pushing a Docker image to Docker Hub whenever changes are pushed to the `main` branch or a pull request is made targeting the `main` branch. The workflow ensures that Docker images are consistently built, tagged, and pushed to the Docker Hub registry.

## Workflow Overview

- **Trigger**: The workflow is triggered on `push` and `pull_request` events to the `main` branch.
- **Actions**: The workflow performs the following actions:
  1. **Checkout code**: Retrieves the latest code from the repository.
  2. **Set up Docker Compose**: Installs Docker Compose to help manage multi-container applications.
  3. **Build Docker image**: Builds the Docker image using `docker-compose`.
  4. **Tag Docker image**: Tags the built Docker image with the commit SHA.
  5. **Log in to Docker Hub**: Logs in to Docker Hub using credentials stored in GitHub secrets.
  6. **Push Docker image**: Pushes the tagged image to Docker Hub.


