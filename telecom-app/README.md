# telecom-app

Simple Python Flask application for Jenkins CI/CD demo okay!

## Endpoints

- GET /health → health check
- GET /users  → returns users list

## Project Structure

```
telecom-app/
├── app.py
├── requirements.txt
├── test_app.py
├── Dockerfile
├── Jenkinsfile
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

## Pipeline Flow

```
GitHub → Jenkins → Test → Docker Build → Push to ECR → Deploy to EKS okay!
```
