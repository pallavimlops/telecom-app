# Parameterized Pipeline — Execution Steps!

---

## STEP 1 — Push Jenkinsfile-parameterized to GitHub

---

## STEP 2 — Create New Jenkins Job

```
Jenkins UI → New Item

Name = telecom-app-parameterized
Type = Pipeline
→ Click OK

Scroll to Pipeline section:
Definition   = Pipeline script from SCM
SCM          = Git
Repository URL = https://github.com/pallavimlops/telecom-app.git
Credentials  = github-credentials
Branch       = */main
Script Path  = telecom-app/Jenkinsfile-parameterized

→ Click Save okay!
```

---

## STEP 3 — First Run to Initialize Parameters

```
Jenkins → telecom-app-parameterized
→ Click "Build Now" once
→ Wait for it to complete

After first run:
→ Button changes from "Build Now"
→ to "Build with Parameters" okay!
```

---

## STEP 4 — Run With Parameters (dev)

```
Jenkins → telecom-app-parameterized
→ Click "Build with Parameters"

Fill the form:
ENVIRONMENT = dev
IMAGE_TAG   = v1.0.1
RUN_TESTS   = true (checked)

→ Click Build okay!
```

---

## STEP 5 — Verify Dev Deployment

```bash
kubectl get pods -n dev
kubectl get svc -n dev

# Copy EXTERNAL-IP from svc output
curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/users
```

---

## STEP 6 — Run With Parameters (staging)

```
Jenkins → telecom-app-parameterized
→ Click "Build with Parameters"

Fill the form:
ENVIRONMENT = staging
IMAGE_TAG   = v1.0.1
RUN_TESTS   = true

→ Click Build okay!
```

---

## STEP 7 — Verify Deployment

```bash
kubectl get pods -n staging
kubectl get svc -n staging
```

---

## STEP 8 — Skip Tests Demo

```
Jenkins → telecom-app-parameterized
→ Click "Build with Parameters"

Fill the form:
ENVIRONMENT = staging
IMAGE_TAG   = v1.0.1
RUN_TESTS   = false  ← uncheck this!

→ Click Build okay!

Watch pipeline:
→ Checkout       ✓
→ Test            SKIPPED ← because RUN_TESTS = false
→ Docker Build   ✓
→ Push to ECR    ✓
→ Deploy to EKS  ✓
```

---

## STEP 9 — Verify All Namespaces

```bash
kubectl get namespaces
kubectl get pods -n dev
kubectl get pods -n staging
kubectl get svc -n dev
kubectl get svc -n staging
```

---

