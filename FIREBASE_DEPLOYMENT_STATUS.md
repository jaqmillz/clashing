# Firebase Deployment Status

## ✅ What's Been Deployed

### 1. Firebase Hosting (FREE TIER) ✓
- **Status**: Successfully deployed
- **URL**: https://clashing-stats.web.app
- **Contents**: Static frontend (HTML, CSS, JS, images)
- **Includes**:
  - Home page ([index.html](public/index.html))
  - Cards page ([cards.html](public/cards.html))
  - Static assets in [public/static/](public/static/)

### 2. Cloud Firestore (FREE TIER) ✓
- **Status**: Successfully configured and deployed
- **Database**: Created and ready
- **Security Rules**: Deployed ([firestore.rules](firestore.rules))
- **Indexes**: Deployed ([firestore.indexes.json](firestore.indexes.json))
- **Location**: `nam5` (North America)

---

## ⚠️ What Requires Blaze Plan

### Cloud Functions (REQUIRES PAY-AS-YOU-GO)
- **Status**: Cannot deploy on FREE tier
- **Why**: Cloud Functions 2nd gen requires Blaze plan
- **Required APIs**:
  - `cloudfunctions.googleapis.com`
  - `cloudbuild.googleapis.com`
  - `artifactregistry.googleapis.com`

**Error Message**:
```
Your project clashing-stats must be on the Blaze (pay-as-you-go) plan to complete this command.
```

---

## 🔄 Two Options Moving Forward

### Option 1: Upgrade to Blaze Plan (Pay-as-you-go)

**Cost Estimate**:
- **Free tier included** on Blaze plan:
  - 2M function invocations/month
  - 400k GB-seconds compute
  - 200k CPU-seconds
  - 5 GB network egress/month

- **Expected monthly cost**: $0-5/month for small traffic
  - First 2M invocations = FREE
  - Typical usage for personal project = $0-2/month
  - Only pay for what you use beyond free tier

**Steps to Upgrade**:
1. Go to: https://console.firebase.google.com/project/clashing-stats/usage/details
2. Click "Modify plan"
3. Select "Blaze - Pay as you go"
4. Add billing account (credit card required)
5. Set budget alerts (recommended: $5/month)

**After upgrading**:
```bash
# Deploy everything
firebase deploy
```

**Pros**:
- Full serverless backend
- No server management
- Auto-scaling
- Works exactly as planned

**Cons**:
- Requires credit card
- Potential charges (though likely $0-5/month)

---

### Option 2: Use Alternative Free Backend

Since Cloud Functions requires Blaze, here are free alternatives:

#### A. Deploy Backend to Free Hosting Platform
Use a free tier service for the Python backend:

- **Railway.app** (500 hrs/month free)
- **Render.com** (750 hrs/month free)
- **Fly.io** (Free tier available)
- **PythonAnywhere** (Always-on free tier)

**Architecture**:
- Firebase Hosting → serves frontend only
- External service → runs Flask API
- Cloud Firestore → database (still free)
- Frontend calls external API directly

**Pros**:
- 100% free
- No credit card required
- Keep using Firebase for frontend + database

**Cons**:
- More complex deployment
- Two separate services to manage
- Not fully serverless

#### B. Client-Side Only (No Backend)
Rewrite app to call Clash Royale API directly from browser

**Pros**:
- Completely free
- Simple deployment

**Cons**:
- Exposes API key in browser (security risk)
- CORS issues with Clash Royale API
- No historical data storage (unless using Firestore directly from client)
- Not recommended

---

## 📊 Current Status

| Component | Status | Free Tier? | URL/Location |
|-----------|--------|------------|--------------|
| Firebase Hosting | ✅ Deployed | ✅ Yes | https://clashing-stats.web.app |
| Cloud Firestore | ✅ Configured | ✅ Yes | `nam5` |
| Firestore Rules | ✅ Deployed | ✅ Yes | - |
| Firestore Indexes | ✅ Deployed | ✅ Yes | - |
| Cloud Functions | ❌ Blocked | ❌ No (Blaze required) | - |

---

## 🎯 Recommendation

### For Best Experience: Upgrade to Blaze Plan

**Why**:
1. **Actual cost will be ~$0-2/month** for your traffic level
2. Firebase gives you $0.01/invocation after 2M free invocations
3. Your app will use maybe 1k-10k invocations/month = FREE
4. You only pay if you exceed free tier
5. You can set billing alerts to prevent surprises

**Safety Measures**:
- Set budget alert at $5/month
- Monitor usage in Firebase console
- Can downgrade back to Spark anytime

**This is the cleanest, simplest solution** and will cost you nothing unless your app gets popular (which is a good problem to have).

---

## 📝 What's Already Built

All the code is ready to deploy:
- ✅ [functions/main.py](functions/main.py) - Cloud Functions endpoints
- ✅ [functions/firestore_store.py](functions/firestore_store.py) - Firestore data layer
- ✅ [functions/requirements.txt](functions/requirements.txt) - Dependencies
- ✅ [firebase.json](firebase.json) - Configuration
- ✅ [.firebaserc](.firebaserc) - Project settings

**All you need to do**:
1. Upgrade to Blaze plan
2. Run: `firebase deploy`
3. Done!

---

## 🚀 Ready to Deploy?

Let me know if you want to:
1. **Upgrade to Blaze** (recommended - will cost ~$0/month)
2. **Use alternative free backend** (more complex)
3. **Just keep static hosting** (no dynamic features)

The infrastructure is all set up and ready to go! 🔥
