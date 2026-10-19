# Task Manager - CI/CD with Jenkins, Docker and Minikube

A small Flask task manager used to demonstrate an automated CI/CD pipeline.

## Pipeline stages
1. **Checkout** - Jenkins pulls the latest code from GitHub.
2. **Build & Test** - creates a virtualenv, installs dependencies, syntax-checks and runs pytest.
3. **Docker Build** - builds the image, tagged with the build number and `latest`.
4. **Push Image** - logs in with Jenkins-stored credentials and pushes to Docker Hub.
5. **Deploy to Minikube** - applies `k8s/` manifests and sets the new image tag.
6. **Verify** - checks pods, deployment, service and the `/health` endpoint.

## Run locally
    pip install -r requirements.txt
    python app.py        # http://localhost:5000

## TODO for the submission
- AWS / Jenkins setup notes
- How the image is pushed and the app is accessed
- What changed for the second run
- Screenshots
