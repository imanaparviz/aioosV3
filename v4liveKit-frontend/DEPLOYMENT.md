# 🚀 Deployment Guide - Voice AI Platform

In guide baraye deploy kardane project ru **Vercel** ba **Supabase** database.

---

## 📋 Checklist...

Age tamoom in kara ro anjam dadi, amadeyi baraye deploy:

- [ ] Git repo setup shode (GitHub/GitLab)
- [ ] Supabase account + project sakhtei
- [ ] Supabase keys dari (URL + anon key)
- [ ] `.env.local` ba keys fill shode (local test)
- [ ] Code push shode be Git
- [ ] Vercel account sakhtei

---

## Part 1️⃣: Supabase Setup (Database)

### Step 1: Create Supabase Account

1. Boro **https://supabase.com**
2. Click **"Start your project"**
3. **Sign in** ba GitHub account

### Step 2: Create New Project

1. Click **"New Project"**
2. Fill konid:
   ```
   Organization: Personal (ya team e khodo entekhab konid)
   Project Name: voice-ai-platform
   Database Password: [YE PASSWORD E GHAVI - YADET BASHE!]
   Region: West US (North California) - ya nazdiktarino
   ```
3. Click **"Create new project"**
4. **Wait 2-3 minutes** - project dare amade mishe

### Step 3: Get API Keys

Vaghti project amade shod:

1. Sidebar samte chap: **Settings** ⚙️
2. Click **"API"**
3. Copy konid (har do!):
   ```
   Project URL: https://xxxxxxxxxxxxx.supabase.co
   anon public key: eyJhbGc...kheyli_boland_hast
   ```

### Step 4: Email Confirmation Setup (OPTIONAL amma khobe)

Default, Supabase email confirmation mikhad. Baraye testing:

1. **Settings** > **Authentication**
2. **Email Auth** section:
   - Toggle **OFF**: "Enable email confirmations"
   - Toggle **ON**: "Enable email signups"
3. Save konid

Alan users bedoone email confirmation signup mishan! (baraye testing khobe)

---

## Part 2️⃣: Local Development Test

Age hanuz local test nakardi, check kon:

### Step 1: Environment Variables

1. To root e project, check `.env.local` vojood dare
2. Age nadari, copy `.env.example`:

   ```bash
   cp .env.example .env.local
   ```
3. Baz kon `.env.local` va fill kon:

   ```env
   VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGc...
   ```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Run Dev Server

```bash
npm run dev
```

Baz kon: **http://localhost:5173**

### Step 4: Test Signup/Login

1. Click **"Get Started"**
2. Fill signup form
3. Submit kon
4. Check Supabase dashboard:
   - **Authentication** > **Users**
   - Bayad user e jadid bebini! ✅

Age in kar kard, amadeyi baraye Vercel! 🎉

---

## Part 3️⃣: Vercel Deployment

### Step 1: Push Code to GitHub

Age hanuz push nakardi:

```bash
git add .
git commit -m "Add Supabase integration"
git push origin main
```

### Step 2: Create Vercel Account

1. Boro **https://vercel.com**
2. Click **"Sign Up"**
3. **Continue with GitHub**
4. Authorize Vercel

### Step 3: Import Project

1. Vercel dashboard: Click **"Add New..."** > **"Project"**
2. **Import Git Repository**:
   - List e repos ro mibi
   - Repo ro peyda kon: `voice-ai-platform`
   - Click **"Import"**

### Step 4: Configure Build Settings

Vercel automatice detect mikone Vite ro. Check konid:

```
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

Age درست nist, manual set kon.

### Step 5: Add Environment Variables (KHEILI MOHEM!)

In section e **Environment Variables**:

1. Click **"Add"**
2. Add konid:

   ```
   Name: VITE_SUPABASE_URL
   Value: https://xxxxxxxxxxxxx.supabase.co
   ```
3. Click **"Add"** dobare:

   ```
   Name: VITE_SUPABASE_ANON_KEY
   Value: eyJhbGc...
   ```
4. **Environment**: "Production" (check she)

### Step 6: Deploy!

1. Click **"Deploy"** button
2. Wait 2-3 minutes
3. Vercel build mikone va deploy mikone
4. Success meshe! 🎉

Ye URL midi mesle: `https://voice-ai-platform-xyz123.vercel.app`

---

## Part 4️⃣: Test Production

### Test 1: Landing Page

1. Baz kon Vercel URL
2. Bayad landing page ro bebini ba logo va buttons

### Test 2: Signup

1. Click **"Get Started"**
2. Fill form:
   ```
   Name: Test User
   Email: test@example.com
   Password: test123456
   ```
3. Submit
4. Bayad redirect she be **Dashboard** ✅

### Test 3: Check Supabase

1. Boro Supabase dashboard
2. **Authentication** > **Users**
3. Bayad `test@example.com` ro bebini! ✅

### Test 4: Logout/Login

1. To dashboard, bezane **Logout**
2. Miri landing page
3. Click **"Sign In"**
4. Login kon ba همون email/password
5. Bayad dashboard ro bebini dobare! ✅

---

## 👥 Part 5️⃣: Share with Team (3-4 Developers)

### Baraye Lead Developer (to!):

1. **Share Vercel URL** ba team:

   ```
   Production: https://your-app.vercel.app
   ```
2. **Share Supabase Keys** ba team (SAFELY!):

   ```
   VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGc...
   ```

   Befreste via:

   - Slack/Discord private message
   - Encrypted file
   - Password manager (1Password, etc)
3. **Invite team to Git repo:**

   - GitHub repo > Settings > Collaborators
   - Add email haye developers

### Baraye Developers (other team members):

1. **Clone repo:**

   ```bash
   git clone https://github.com/your-username/voice-ai-platform.git
   cd voice-ai-platform
   npm install
   ```
2. **Create `.env.local`:**

   ```bash
   cp .env.example .env.local
   ```
3. **Fill `.env.local`** ba keys ke lead dad:

   ```env
   VITE_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGc...
   ```
4. **Run:**

   ```bash
   npm run dev
   ```
5. **Test signup/login** locally
6. **Test production URL** online!

---

## 🔄 Update Workflow (After Deploy)

Har vaght change midi:

### Local:

```bash
# Make changes
git add .
git commit -m "Description e change"
git push origin main
```

### Vercel:

- Automatice detect mikone push ro
- Build mikone dobare
- Deploy mikone
- 2-3 daghighe tool mikeshe

Check: https://vercel.com/dashboard > Deployments

---

## 🐛 Troubleshooting

### Problem 1: "Supabase credentials mojood nist"

**Error to console:**

```
❌ Supabase credentials mojood nist! Check .env.local file ro.
```

**Fix:**

- Check `.env.local` vojood dare
- Check keys copy shode dorost
- Restart dev server: `npm run dev`

---

### Problem 2: Vercel Build Fails

**Error:** Build command failed

**Fix:**

1. Vercel dashboard > Project > Settings > Environment Variables
2. Check in 2 ta add shode:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
3. Redeploy: Deployments > Latest > "Redeploy"

---

### Problem 3: Login nemikone ru production

**Symptoms:** Local kar mikone, production na

**Fix:**

1. Browser console ro baz kon (F12)
2. Bebin error chi mige
3. Mostly environment variables nist
4. Check Vercel env vars dobare

---

### Problem 4: Email confirmation email nemiad

**Fix:**

1. Supabase dashboard > Settings > Authentication
2. **Disable** "Enable email confirmations" (baraye testing)
3. Ya check spam folder

---

## 📊 Monitor App

### Supabase Monitoring:

- **Users**: Authentication > Users
- **Logs**: Logs & Events
- **Database**: Table Editor

### Vercel Monitoring:

- **Deployments**: Vercel dashboard > Deployments
- **Logs**: Click on deployment > "View Function Logs"
- **Analytics**: Analytics tab

---

## 🎯 Summary Checklist

After deployment, check konid:

- [ ] ✅ Vercel URL kar mikone
- [ ] ✅ Landing page load mishe
- [ ] ✅ Signup form kar mikone
- [ ] ✅ User to Supabase save mishe
- [ ] ✅ Login kar mikone
- [ ] ✅ Dashboard namayesh dade mishe
- [ ] ✅ Logout kar mikone
- [ ] ✅ Team members access daran
- [ ] ✅ Local development kar mikone

---

**Moafagh bashi!** 🚀

Age problem vojood dasht, check kon:

1. Browser console (F12)
2. Supabase logs
3. Vercel deployment logs
