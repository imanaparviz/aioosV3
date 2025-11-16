# Voice AI Agents Platform

Ye platform e Vue.js baraye modiriyate Voice AI Agents ba authentication e vaghei (Supabase), login, signup, va dashboard.

## Features

✅ **Real Authentication** ba Supabase
✅ **Login/Signup** system ba database
✅ **Dashboard** baraye modiriyate agents
✅ **Responsive Design** ba Tailwind CSS
✅ **Dark Mode** support
✅ **Protected Routes** ba authentication guards
✅ **Modern UI** ba Material Icons
✅ **Vercel Ready** baraye deployment

## Tech Stack

- Vue 3 (Composition API)
- Vue Router
- Pinia (State Management)
- Supabase (Database + Authentication)
- Tailwind CSS
- Vite
- Vercel (Deployment)

---

## 🚀 Setup Guide (Local Development)

### Step 1: Clone Project

```bash
git clone <your-repo-url>
cd voice-ai-platform
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Supabase Setup

#### 3.1 Create Supabase Account
1. Boro `https://supabase.com`
2. Sign up ba GitHub
3. Create New Project:
   - Name: `voice-ai-platform`
   - Database Password: Ye password e ghavi (save kon!)
   - Region: Nazdiktarino entekhab kon
   - Wait 2-3 minutes ta amade she

#### 3.2 Get API Keys
1. To Supabase Dashboard beres
2. **Settings** > **API**
3. Copy konid:
   - `Project URL`
   - `anon public` key

#### 3.3 Configure Environment Variables

1. Copy `.env.example` be `.env.local`:
   ```bash
   cp .env.example .env.local
   ```

2. `.env.local` ro baz kon va keys ro ezafe kon:
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=your-anon-key-here
   ```

### Step 4: Run Local Development Server

```bash
npm run dev
```

Baz kon: `http://localhost:5173`

---

## 🌐 Vercel Deployment (Production)

### ⚡ Auto-Deploy (Recommended)
Age Vercel ro ba GitHub connect kardi, har dafe ke `git push` koni, automatic deploy mishe! 🎉

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Vercel

1. Boro `https://vercel.com`
2. **Sign up** ba GitHub account
3. Click **"Add New Project"**
4. **Import** GitHub repository ro entekhab kon
5. **Configure Project:**
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`

6. **Environment Variables** ezafe kon (kheili mohem!):
   - `VITE_SUPABASE_URL` = `https://your-project.supabase.co`
   - `VITE_SUPABASE_ANON_KEY` = `your-anon-key`

7. Click **"Deploy"**

Vercel 2-3 daghighe tool mikeshe. Bad az deploy, ye URL midi mesle: `https://your-app.vercel.app`

### Step 3: Test Production

1. Baz kon URL e Vercel
2. Sign up kon ba ye email
3. Login kon
4. Dashboard ro test kon

---

## 👥 Multi-Developer Setup

Baraye 3-4 nafar developer ke mikhan ru project kar konan:

### Har developer bayad:

1. **Clone repo:**
   ```bash
   git clone <repo-url>
   cd voice-ai-platform
   npm install
   ```

2. **Get Supabase keys** (az lead developer):
   - Project URL
   - Anon key

3. **Create `.env.local`** file:
   ```env
   VITE_SUPABASE_URL=https://shared-project.supabase.co
   VITE_SUPABASE_ANON_KEY=shared-anon-key
   ```

4. **Run locally:**
   ```bash
   npm run dev
   ```

### Hame ru ye Supabase project

Hame developers ru **yek Supabase project** kar mikonan. In yani:
- ✅ Yek database baraye hame
- ✅ Har ki signup kone, to database sabt mishe
- ✅ Hame baham login/logout test mikonan
- ✅ Live test ru Vercel URL

---

## 📁 Project Structure

```
voice-ai-platform/
├── src/
│   ├── assets/          # CSS files
│   ├── components/      # Vue components
│   │   ├── SidebarNav.vue
│   │   ├── DashboardHeader.vue
│   │   └── AgentCard.vue
│   ├── views/          # Page components
│   │   ├── LandingView.vue
│   │   ├── LoginView.vue
│   │   ├── SignupView.vue
│   │   └── DashboardView.vue
│   ├── router/         # Vue Router
│   ├── stores/         # Pinia stores (auth)
│   ├── lib/            # Supabase client
│   ├── App.vue
│   └── main.js
├── .env.local          # Environment variables (LOCAL ONLY - git ignore)
├── .env.example        # Template baraye env vars
├── vercel.json         # Vercel config
├── package.json
└── README.md
```

---

## 🔐 Authentication Flow

### Signup:
1. User email, password, name mide
2. Request mire Supabase
3. User to `auth.users` table sabt mishe
4. Automatically login mishe
5. Redirect be `/dashboard`

### Login:
1. User email/password mide
2. Supabase check mikone
3. Session create mishe
4. Redirect be `/dashboard`

### Protected Routes:
- Age login nakoni, nemitoni `/dashboard` ro bebini
- Redirect mishe be `/login`

---

## 🛠️ Commands

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build production
npm run build

# Preview production build
npm run preview
```

---

## 🐛 Troubleshooting

### Error: "Supabase credentials mojood nist"
- Check `.env.local` file vojood dare
- Keys ro check kon درست copy shode باشه

### Error: "Invalid login credentials"
- Password bayad 6+ characters bashe
- Email bayad valid bashe
- Check Supabase dashboard > Authentication > Users

### Vercel build error
- Check environment variables to Vercel add shode باشه
- Build command: `npm run build`
- Output directory: `dist`

---

## 📞 Support

Agar moshkeli vojood dasht:
1. Check Supabase logs: Dashboard > Logs
2. Check browser console baraye errors
3. Check Vercel deployment logs

---

## 🎯 Next Steps

- [x] Agent creation functionality ✅
- [x] Database schema for agents ✅
- [ ] Real-time updates
- [ ] Analytics dashboard
- [ ] User profile management
- [ ] Team collaboration features

---

## 📖 Additional Documentation

- **[Agent Creation & Customization Guide](./AGENT_CREATION_GUIDE.md)** - Complete guide for creating and customizing voice AI agents, including system prompt customization, voice selection, and best practices

---

**Happy Coding!** 🚀
