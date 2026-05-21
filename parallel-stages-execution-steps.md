# Parallel Stages — Execution Steps !

---

## STEP 1 — Push Jenkinsfile-parallel to GitHub

```bash
# On your laptop
cd telecom-app
git add Jenkinsfile-parallel
git commit -m "Added parallel stages Jenkinsfile okay!"
git push origin main
```

---

## STEP 2 — Create New Jenkins Job

```
Jenkins UI → New Item

Name = telecom-app-parallel
Type = Pipeline
→ Click OK

Scroll to Pipeline section:
Definition   = Pipeline script from SCM
SCM          = Git
Repository URL = https://github.com/pallavimlops/telecom-app.git
Credentials  = github-credentials
Branch       = */main
Script Path  = telecom-app/Jenkinsfile-parallel

→ Click Save okay!
```

---

## STEP 3 — Run Pipeline

```
Jenkins → telecom-app-parallel
→ Click "Build Now"
→ Click Build #1
→ Click "Console Output" okay!
```

---

## STEP 4 — Watch Parallel Stages Run

```
In Pipeline view you will see:

Checkout
    ↓
┌─────────────────────────────────┐
│  Unit Tests  │  Lint Check      │  ← both run simultaneously
└─────────────────────────────────┘
    ↓
Docker Build
    ↓
Push to ECR
    ↓
Deploy to EKS okay!
```

---

## STEP 5 — See the Time Difference 

```
First run WITHOUT parallel:
→ Note the build time okay!

Then run WITH parallel:
→ Note the build time
→ Show it is faster okay!

Jenkins → Build History
→ Compare build times okay!
```

---

## STEP 6 — Verify Deployment

```bash
kubectl get pods -n dev
kubectl get svc -n dev

curl http://<EXTERNAL-IP>/health
curl http://<EXTERNAL-IP>/users
```

---

## What Will See in Console Output

```
[Pipeline] stage (Test and Lint)
[Pipeline] parallel
[Pipeline] { (Branch: Unit Tests)
[Pipeline] { (Branch: Lint Check)
+ pip3 install flake8          ← Lint running
+ pip3 install -r requirements ← Tests running simultaneously
+ python3 -m pytest test_app.py
+ flake8 telecom-app/app.py
PASSED test_health
PASSED test_get_users
[Pipeline] } (Branch: Unit Tests)
[Pipeline] } (Branch: Lint Check)
[Pipeline] // parallel okay!
```

---

## Difference — Without vs With Parallel

```
WITHOUT Parallel:
→ Unit Tests run first  (2 min)
→ Then Lint Check runs  (1 min)
→ Total = 3 minutes okay!

WITH Parallel:
→ Unit Tests and Lint Check run together
→ Total = 2 minutes (longest one)
→ Saves 1 minute okay!

In large projects:
→ Saves 10-15 minutes per build okay!
```
