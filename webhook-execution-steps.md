# Webhook Setup — Execution Steps!

---

## STEP 1 — Enable Webhook Trigger in Jenkins Job

```
Jenkins → telecom-app-pipeline → Configure

Scroll to "Build Triggers" section:
→ Check "GitHub hook trigger for GITScm polling"
→ Click Save okay!
```

---

## STEP 2 — Add Webhook in GitHub

```
GitHub → pallavimlops/telecom-app
→ Settings
→ Webhooks
→ Add webhook

Fill:
Payload URL  = http://<JENKINS-EC2-IP>:8080/github-webhook/
Content type = application/json
Secret       = (leave empty)
Events       = Just the push event (selected by default)

→ Click "Add webhook" okay!
```

---

## STEP 3 — Verify Webhook is Working

```
GitHub → Settings → Webhooks
→ Click on your webhook
→ Scroll down to "Recent Deliveries"
→ You will see a ping request
→ Green tick = webhook connected okay!

If you see red cross:
→ Check Jenkins EC2 IP is correct
→ Check port 8080 is open in Security Group okay!
```

---

## STEP 4 — Test Webhook

```bash
# Make any small change to app.py on your laptop
# Example: add a comment

# Push to GitHub
git add .
git commit -m "Testing webhook trigger okay!"
git push origin main
```

```
Immediately go to Jenkins UI:
→ Pipeline should start automatically
→ No clicking Build Now okay!
```

---

## STEP 5 — Verify Auto Trigger

```
Jenkins → telecom-app-pipeline

You will see:
→ New build started automatically
→ Triggered by GitHub push
→ Console Output shows "Started by GitHub push" okay!
```

---