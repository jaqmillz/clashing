# Firebase Migration Plan - Clash Royale Stats Tracker

## Overview
Migrate the Clash Royale Stats Tracker from local Flask app to Firebase (free tier) with:
- **Firebase Hosting** - Static frontend hosting
- **Cloud Functions** - Backend API endpoints (Python)
- **Cloud Firestore** - NoSQL database for historical stats
- **Firebase Authentication** - User login (optional for now)
- Custom domain support

---

## Architecture Changes

### Current Architecture
- **Backend**: Flask (Python) running on local server (port 3000)
- **Data Storage**: Parquet files in `data/` directory
- **Frontend**: Jinja2 templates rendered server-side
- **API**: REST endpoints served by Flask

### New Firebase Architecture
- **Backend**: Cloud Functions (2nd gen, Python 3.11+)
- **Data Storage**: Cloud Firestore (NoSQL database)
- **Frontend**: Static HTML/CSS/JS hosted on Firebase Hosting
- **API**: Cloud Functions HTTP endpoints
- **Authentication**: Firebase Auth (for future user-specific features)

---

## Firebase Free Tier Limits & Our Usage

### Cloud Firestore
- **Free Tier**: 1 GB storage, 50k reads/day, 20k writes/day, 20k deletes/day
- **Our Usage**:
  - Each player stat record ~2 KB
  - 20k writes/day = ~500 player lookups/day (if saving every lookup)
  - 50k reads/day = plenty for displaying stats and trends
  - **Strategy**: Cache frequently accessed data, batch writes

### Cloud Functions
- **Free Tier**: 2M invocations/month, 400k GB-seconds compute, 200k CPU-seconds
- **Our Usage**:
  - ~10-20 API calls per user session
  - 2M/month = ~66k invocations/day (plenty for small-medium traffic)
  - **Strategy**: Use Cloud Functions 2nd gen for better performance

### Firebase Hosting
- **Free Tier**: 10 GB bandwidth/month, 1 GB storage
- **Our Usage**:
  - Frontend files ~5 MB total
  - 10 GB = ~2,000 full page loads/month (with assets)
  - **Strategy**: Enable CDN caching, compress assets

### Firebase Authentication
- **Free Tier**: 50k MAU (monthly active users)
- **Our Usage**: Not required initially, but available for future

---

## Step-by-Step Migration Plan

## PART 1: WHAT YOU NEED TO DO (Web Console Setup)

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or "Create a project"
3. Enter project name: `clashing-stats` (or your preferred name)
4. **Disable Google Analytics** (optional, but recommended to keep it simple)
5. Click "Create project"
6. Wait for project to be created (~30 seconds)

### Step 2: Enable Firestore Database
1. In Firebase Console, click "Firestore Database" in left sidebar
2. Click "Create database"
3. **Select**: "Start in production mode" (we'll add security rules later)
4. **Location**: Choose closest to you (e.g., `us-central1` for US)
   - ⚠️ **Important**: Cannot change location later!
5. Click "Enable"

### Step 3: Enable Firebase Authentication (Optional but Recommended)
1. Click "Authentication" in left sidebar
2. Click "Get started"
3. Click on "Sign-in method" tab
4. Enable "Anonymous" authentication (for future features)
5. Click "Save"

### Step 4: Get Firebase Configuration
1. Click the gear icon ⚙️ next to "Project Overview"
2. Click "Project settings"
3. Scroll down to "Your apps" section
4. Click the Web icon `</>`
5. Register app:
   - App nickname: `clashing-web`
   - **Check** "Also set up Firebase Hosting"
   - Click "Register app"
6. **Copy the firebaseConfig object** - You'll need to provide this to me
   - It looks like this:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIza...",
     authDomain: "clashing-stats.firebaseapp.com",
     projectId: "clashing-stats",
     storageBucket: "clashing-stats.appspot.com",
     messagingSenderId: "123...",
     appId: "1:123..."
   };
   ```
7. Click "Continue to console"

### Step 5: Get Clash Royale API Key Configuration
- **Provide me with your current Clash Royale API key** from your `.env` file
- We'll store this securely in Firebase Secret Manager

### Step 6: Set Up Custom Domain (Do This Last)
1. After we deploy successfully, go to Firebase Console
2. Click "Hosting" in left sidebar
3. Click "Add custom domain"
4. Enter your domain: `yourdomain.com`
5. Follow DNS verification steps:
   - Add TXT record to your domain DNS
   - Add A record pointing to Firebase IPs
6. Firebase will auto-provision SSL certificate (takes ~24 hours)

---

## PART 2: WHAT I NEED FROM YOU

Please provide the following:

1. **Firebase Config Object** (from Step 4 above)
   ```javascript
   {
     apiKey: "...",
     authDomain: "...",
     projectId: "...",
     // etc.
   }
   ```

2. **Your Clash Royale API Key** (from `.env` file)
   - We'll store this as a Cloud Functions secret

3. **Your Custom Domain** (if you want to set it up)
   - Domain name: `_____________________`
   - Domain registrar: (e.g., Namecheap, GoDaddy, Cloudflare)

4. **Default Player Tag** (from `.env` file)
   - Current default: `#2PP`

---

## PART 3: WHAT I WILL DO (Code Changes)

### Step 1: Install Firebase CLI & Dependencies
```bash
# Install Firebase CLI globally
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase project
firebase init
```

### Step 2: Migrate Data Storage (Parquet → Firestore)
- Convert `data_store.py` to use Firestore SDK
- Collection structure:
  ```
  players/
    {player_tag}/
      stats/
        {timestamp} → { trophies, wins, losses, ... }

  cards/
    {card_name} → { kisses, name, rarity, icon_url }
  ```

### Step 3: Convert Flask App to Cloud Functions
- Split Flask routes into individual Cloud Functions:
  - `get_player_stats(player_tag)` → Cloud Function
  - `get_player_history(player_tag)` → Cloud Function
  - `get_all_cards()` → Cloud Function
  - `kiss_card()` → Cloud Function
  - etc.

### Step 4: Convert Frontend to Static HTML/JS
- Convert Jinja2 templates to static HTML
- Use vanilla JavaScript to call Cloud Functions APIs
- Keep existing CSS/images

### Step 5: Add Firestore Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow public read access to player stats and cards
    match /players/{playerId}/{document=**} {
      allow read: if true;
      allow write: if false; // Only Cloud Functions can write
    }

    match /cards/{cardId} {
      allow read: if true;
      allow write: if false; // Only Cloud Functions can write
    }
  }
}
```

### Step 6: Configure Firebase Hosting
- Create `firebase.json` with hosting rules
- Set up redirects for API calls to Cloud Functions
- Configure caching headers

### Step 7: Deploy Everything
```bash
# Deploy Firestore rules, Functions, and Hosting in one command
firebase deploy
```

### Step 8: Migrate Existing Data (Optional)
- Script to read existing Parquet files
- Upload historical data to Firestore
- Preserve all timestamps and player history

---

## Files I Will Create/Modify

### New Files
- `firebase.json` - Firebase project configuration
- `.firebaserc` - Firebase project aliases
- `firestore.rules` - Database security rules
- `firestore.indexes.json` - Database indexes for queries
- `functions/` directory:
  - `functions/main.py` - Cloud Functions entry point
  - `functions/requirements.txt` - Python dependencies
  - `functions/cr_api.py` - Clash Royale API client (adapted)
  - `functions/firestore_store.py` - Firestore data layer
  - `functions/roaster.py` - Roasting logic (same)
- `public/` directory:
  - `public/index.html` - Static home page
  - `public/cards.html` - Static cards page
  - `public/js/app.js` - Frontend JavaScript
  - `public/css/style.css` - Styles
  - `public/static/` - Images
- `scripts/migrate_data.py` - One-time data migration script

### Modified Files
- `.gitignore` - Add Firebase cache/debug files
- `README.md` - Update with Firebase deployment instructions
- `justfile` - Add Firebase deployment commands

### Files We Keep (for reference)
- Original Flask app in `legacy/` folder (backup)

---

## Estimated Costs

### Free Tier Coverage
With Firebase free tier, you can handle:
- **~500 player lookups per day** (with historical tracking)
- **~2,000 website visits per month**
- **~50 concurrent users**

### If You Need More
- Upgrade to Blaze (pay-as-you-go) plan
- Typical costs for small app: **$1-5/month**
- Only pay for what you use beyond free tier

---

## Timeline

Once you provide the Firebase config:
1. **Setup & Configuration** (30 mins)
   - Initialize Firebase project locally
   - Configure secrets and environment

2. **Code Migration** (2-3 hours)
   - Convert Flask → Cloud Functions
   - Migrate Parquet → Firestore
   - Convert templates → static HTML/JS

3. **Testing** (1 hour)
   - Test locally with Firebase emulators
   - Verify all features work

4. **Deployment** (30 mins)
   - Deploy to Firebase
   - Smoke test production

5. **Custom Domain Setup** (your side, ~24 hours)
   - DNS configuration
   - SSL certificate provisioning

**Total Time**: ~4-5 hours of work, ready to deploy same day

---

## Benefits After Migration

✅ **No Server Maintenance** - Firebase handles everything
✅ **Auto-Scaling** - Handles traffic spikes automatically
✅ **Global CDN** - Fast loading worldwide
✅ **Free SSL** - HTTPS by default
✅ **99.95% Uptime** - Google's infrastructure
✅ **Built-in DDoS Protection** - Automatic
✅ **Zero Downtime Deploys** - Update without disruption
✅ **Custom Domain** - Professional appearance

---

## Next Steps

1. **You**: Follow "PART 1: WHAT YOU NEED TO DO" above
2. **You**: Provide me the information from "PART 2: WHAT I NEED FROM YOU"
3. **Me**: Execute "PART 3: WHAT I WILL DO" to migrate the code
4. **We**: Test together on Firebase Hosting temporary URL
5. **You**: Configure custom domain (optional)
6. **Done**: App live on Firebase! 🚀

---

## Questions & Considerations

### Do we need user authentication?
- **Now**: Not required (public app)
- **Future**: Could add login to track "favorite players" per user
- **Recommendation**: Skip for v1, easy to add later

### What about the Clash Royale API rate limits?
- Keep the same API client
- Add caching in Firestore to reduce API calls
- Cloud Functions can cache responses in memory

### Can we still use the local dev environment?
- Yes! I'll keep the Flask app in a `legacy/` folder
- Firebase Emulators let you test locally before deploying

### What if we exceed free tier limits?
- Firebase sends email warnings at 80% usage
- Upgrade to Blaze plan (pay-as-you-go)
- Set billing alerts to prevent surprises

---

## Ready to Start?

Let me know when you have:
1. ✅ Firebase project created
2. ✅ Firestore enabled
3. ✅ Firebase config object (from web console)
4. ✅ Clash Royale API key to share

Then I'll start the migration! 🔥
