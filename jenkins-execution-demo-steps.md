# Jenkins — Complete Execution Steps (Demo Class) okay!
# From Launching Server to Deployment

---

# PHASE 1 — Jenkins Server Setup

## STEP 1 — Launch EC2 Instance

```
AWS Console → EC2 → Launch Instance

Name            = jenkins-server
AMI             = Ubuntu 24.04 LTS
                  (ubuntu-noble-24.04-amd64-server-20260424)
Instance type   = m7i-flex.large
Key pair        = your existing key pair

Security Group — create new:
Name = jenkins-sg
Rules:
→ SSH        port 22    → My IP
→ Custom TCP port 8080  → Anywhere (Jenkins UI)
→ Custom TCP port 50000 → Anywhere (Jenkins agents)

Storage = 20 GB
→ Launch Instance okay!
```

---

## STEP 2 — SSH into EC2

```bash
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>
```

---

## STEP 3 — Update System

```bash
sudo apt update -y
sudo apt upgrade -y
```

---

## STEP 4 — Install Java 21

```bash
sudo apt install openjdk-21-jdk -y
java -version
```

---

## STEP 5 — Download and Install Jenkins 2.492.3

```bash
wget https://pkg.jenkins.io/debian-stable/binary/jenkins_2.492.3_all.deb
sudo apt install ./jenkins_2.492.3_all.deb -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
sudo systemctl status jenkins
```

---

## STEP 6 — Install Docker

```bash
sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker jenkins
sudo usermod -aG docker ubuntu
sudo systemctl restart jenkins
docker --version
```

---

## STEP 7 — Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws --version
```

---

## STEP 8 — Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client
```

---

## STEP 9 — Install eksctl

```bash
curl --silent --location "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

---

# PHASE 2 — Jenkins UI Setup

## STEP 10 — Get Initial Admin Password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

---

## STEP 11 — Open Jenkins UI

```
http://<EC2-PUBLIC-IP>:8080

1. Paste initial admin password → Continue
2. Click "Install suggested plugins" → wait
3. Create Admin User:
   Username  = admin
   Password  = your password
   Full name = Admin
   Email     = your email
   → Save and Continue
4. Jenkins URL → keep default → Save and Finish
5. Click "Start using Jenkins" okay!
```

---

## STEP 12 — Install Additional Plugins

```
Jenkins UI → Manage Jenkins → Plugins → Available plugins

Search and install:
→ Docker Pipeline
→ Amazon ECR
→ AWS Credentials
→ Kubernetes CLI
→ Pipeline (if not installed)
→ Git (if not installed)

Click Install → Restart Jenkins okay!
```

---

## STEP 13 — Add AWS Credentials

```
Jenkins UI → Manage Jenkins → Credentials
→ System → Global credentials → Add Credentials

Kind              = AWS Credentials
Scope             = Global
Access Key ID     = <your AWS access key>
Secret Access Key = <your AWS secret key>
ID                = aws-credentials
Description       = AWS Credentials
→ Create okay!
```

---

## STEP 14 — Add GitHub Credentials

```
Jenkins UI → Manage Jenkins → Credentials
→ System → Global credentials → Add Credentials

Kind        = Username with password
Scope       = Global
Username    = your GitHub username
Password    = your GitHub Personal Access Token
ID          = github-credentials
Description = GitHub Credentials
→ Create okay!

To create GitHub Personal Access Token:
GitHub → Settings → Developer settings
→ Personal access tokens → Tokens (classic)
→ Generate new token
→ Select scope = repo
→ Generate and copy token okay!
```

---

# PHASE 3 — AWS Setup

## STEP 15 — Create ECR Repository

```
AWS Console → ECR → Create Repository

Visibility = Private
Name       = telecom-ap
Region     = us-east-1
→ Create okay!

Copy repository URI:
550651695287.dkr.ecr.us-east-1.amazonaws.com/telecom-ap
```

---

## STEP 16 — Create EKS Cluster

```bash
# Run on Jenkins server
eksctl create cluster \
  --name jenkins-demo-1 \
  --region us-east-1 \
  --nodegroup-name demo-workers \
  --node-type t3.small \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

```
Wait 15-20 minutes okay!
```

---
If Node Role is not created , create using below steps, without this nodes will not be created !!!
```bash
# Create IAM role for nodes
cat > node-trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
  --role-name eksNodeRole \
  --assume-role-policy-document file://node-trust-policy.json

aws iam attach-role-policy \
  --role-name eksNodeRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy

aws iam attach-role-policy \
  --role-name eksNodeRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy

aws iam attach-role-policy \
  --role-name eksNodeRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly



---

## STEP 18 — Configure EKS Access on Jenkins Server

```bash
# Configure AWS CLI
aws configure
# Enter access key, secret key, us-east-1, json

# Update kubeconfig
aws eks update-kubeconfig \
  --region us-east-1 \
  --name jenkins-demo-1

# Copy to jenkins user
sudo mkdir -p /var/lib/jenkins/.kube
sudo cp ~/.kube/config /var/lib/jenkins/.kube/config
sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube

# Verify as jenkins user
sudo su - jenkins
kubectl get nodes
# Should show 2 nodes okay!
```

---

# PHASE 4 — Application Setup

## STEP 19 — Flask App Files

```
Create these files on your laptop:

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

### app.py

```python
from flask import Flask, jsonify

app = Flask(__name__)

users = [
    {'id': 1, 'name': 'Rahul',  'email': 'rahul@telecom.com'},
    {'id': 2, 'name': 'Priya',  'email': 'priya@telecom.com'},
    {'id': 3, 'name': 'Amit',   'email': 'amit@telecom.com'}
]

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'telecom-app'})

@app.route('/users')
def get_users():
    return jsonify({'users': users, 'count': len(users)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### requirements.txt

```
flask==3.0.0
pytest==7.4.0
```

### test_app.py

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert data['count'] == 3
```

### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Jenkinsfile

```groovy
pipeline {
    agent any

    environment {
        AWS_REGION   = 'us-east-1'
        ECR_REGISTRY = '550651695287.dkr.ecr.us-east-1.amazonaws.com'
        ECR_REPO     = 'telecom-ap'
        IMAGE_TAG    = "v1.0.${BUILD_NUMBER}"
        NAMESPACE    = 'dev'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Cloning repository okay!'
                checkout scm
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests okay!'
                sh '''
                    cd telecom-app
                    pip3 install -r requirements.txt --break-system-packages
                    python3 -m pytest test_app.py -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_TAG} okay!"
                sh '''
                    cd telecom-app
                    docker build -t ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                echo 'Pushing image to ECR okay!'
                withCredentials([aws(credentialsId: 'aws-credentials',
                                     region: 'us-east-1')]) {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS \
                        --password-stdin ${ECR_REGISTRY}

                        docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                echo "Deploying to ${NAMESPACE} namespace okay!"
                sh '''
                    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

                    sed "s|IMAGE_PLACEHOLDER|${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}|g" telecom-app/k8s/deployment.yaml | kubectl apply -f - -n ${NAMESPACE}

                    kubectl apply -f telecom-app/k8s/service.yaml -n ${NAMESPACE}

                    kubectl rollout status deployment/telecom-app -n ${NAMESPACE}
                '''
            }
        }

    }

    post {
        success {
            echo "Pipeline SUCCESS okay!"
            echo "Deployed ${IMAGE_TAG} to ${NAMESPACE}"
        }
        failure {
            echo "Pipeline FAILED okay!"
        }
        always {
            cleanWs()
        }
    }
}
```

### k8s/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telecom-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: telecom-app
  template:
    metadata:
      labels:
        app: telecom-app
    spec:
      containers:
      - name: telecom-app
        image: IMAGE_PLACEHOLDER
        ports:
        - containerPort: 5000
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
```

### k8s/service.yaml

```yaml
apiVersion: v1
kind: Service
metadata:
  name: telecom-app-service
spec:
  selector:
    app: telecom-app
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

---

## STEP 20 — Push to GitHub

```bash
cd telecom-app
git init
git add .
git commit -m "Initial telecom app okay!"
git branch -M main
git remote add origin https://github.com/<your-username>/telecom-app.git
git push -u origin main
```

---

# PHASE 5 — Jenkins Pipeline

## STEP 21 — Create Jenkins Pipeline Job

```
Jenkins UI → New Item

Name = telecom-app-pipeline
Type = Pipeline
→ OK

Scroll to Pipeline section:
Definition   = Pipeline script from SCM
SCM          = Git
Repository URL = https://github.com/pallavimlops/telecom-app.git
Credentials  = github-credentials
Branch       = */main
Script Path  = telecom-app/Jenkinsfile
→ Save okay!
```

---

## STEP 22 — Run Pipeline

```
Jenkins → telecom-app-pipeline
→ Click "Build Now"
→ Click Build #1
→ Click "Console Output"
→ Watch all stages run okay!

Expected:
✓ Checkout      → green
✓ Test          → green
✓ Docker Build  → green
✓ Push to ECR   → green
✓ Deploy to EKS → green
```

---

## STEP 23 — Verify Deployment

```bash
# Check pods
kubectl get pods -n dev

# Check service
kubectl get svc -n dev

# Get external IP
kubectl get svc -n dev
# Copy EXTERNAL-IP

# Test app
curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/users
```

---

# PHASE 6 — Cleanup (After Class)

```bash
# Delete EKS cluster
eksctl delete cluster \
  --name jenkins-demo-1 \
  --region us-east-1

# Stop Jenkins EC2 (not terminate)
AWS Console → EC2 → jenkins-server
→ Instance State → Stop okay!

# Delete ECR images (optional)
AWS Console → ECR → telecom-ap
→ Delete images okay!
```

---

# SUMMARY

```
PHASE 1 → Jenkins server setup (Steps 1-9)
PHASE 2 → Jenkins UI setup (Steps 10-14)
PHASE 3 → AWS setup - ECR + EKS (Steps 15-18)
PHASE 4 → Flask app + GitHub (Steps 19-20)
PHASE 5 → Jenkins pipeline (Steps 21-23)
PHASE 6 → Cleanup after class okay!
```
