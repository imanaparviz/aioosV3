# 🔧 Fix: Call Logs RLS & Transcript Feature

## 🔴 Masale chi bood?

Vaghti agent call ro answer mikard:
- ❌ Call log save nemishod
- ❌ Transcript save nemishod
- ❌ Analytics khali bood

**Dalil**: Agent az **ANON key** estefade mikard, na **SERVICE_ROLE key**!

---

## ✅ Chi fix shod?

### 1. Database RLS Policies ✅
- Service_role policies ezafe shod
- Alan agent mitone INSERT va UPDATE kone

### 2. Agent Worker Code ✅
- Code update shod ke az `SUPABASE_SERVICE_ROLE_KEY` estefade kone
- Transcript save code ezafe shod

### 3. Database Schema ✅
- `transcript` column ezafe shod
- `transcript_json` column ezafe shod
- `summary` column ezafe shod (bara Phase 2)
- `summary_json` column ezafe shod (bara Phase 2)

---

## 🎯 Chi bayad bokoni ALAN?

### Step 1: Get SERVICE_ROLE Key 🔑

1. Bro Supabase Dashboard: https://supabase.com/dashboard/project/wwwnfrfbynrktysnydyi
2. Bro **Settings** → **API**
3. Scroll down ta **Project API keys**
4. Copy **`service_role`** key (starts with `eyJ...`)
5. ⚠️ **IMPORTANT**: In key ro NEVER tu frontend estefade nakon!

### Step 2: Update .env File 📝

Open: `v4liveKit/backend/.env`

Peyda kon in line:
```
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY_HERE
```

Replace `YOUR_SERVICE_ROLE_KEY_HERE` ba service_role key-e ke copy kardi.

Bayad beshe mesle in:
```
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M...
```

### Step 3: Restart Backend 🔄

```bash
cd v4liveKit/backend
3-STOP.bat
2-START.bat
```

### Step 4: Test! 🧪

1. Yek call bezan ba agent
2. Ba agent harf bezan
3. Call ro tamoom kon
4. Bro Analytics page
5. **Bayad data bebin!** ✅

---

## 🎉 Chi alan kar mikone?

Bad az in fix:
- ✅ Call logs save mishe
- ✅ Transcript save mishe (text + JSON)
- ✅ Analytics data neshoon mide
- ✅ Top Agents list por mishe
- ✅ Charts data dare
- ✅ Call Logs page data dare

---

## 📊 Chizi k bayad bebini tu Analytics:

### Metrics Cards:
- **Total Calls**: Tedad e call ha
- **Average Duration**: Miyangin e tool e call ha
- **Success Rate**: Darsad e call haye movafagh
- **Total Cost**: Hazine e kol

### Chart:
- Call volume over time (daily/weekly/monthly)

### Top Agents:
- List e agent ha ba call count

---

## 🐛 Age hanuz kar nakard?

### Check 1: SERVICE_ROLE key dorost-e?
```bash
cat v4liveKit/backend/.env | grep SUPABASE_SERVICE_ROLE_KEY
```
Bayad yek JWT token e boland bebin (na `YOUR_SERVICE_ROLE_KEY_HERE`)

### Check 2: Backend restart kardi?
Backend bayad restart beshe ta .env e jadid ro bekhone.

### Check 3: Check database
```sql
SELECT * FROM call_logs ORDER BY created_at DESC LIMIT 1;
```
Age call zadи bayad yek row bebin.

### Check 4: Check logs
Bebin tu backend logs chi mige. Bayad bebini:
```
✅ Call log created: <UUID>
✅ Transcript saved: X messages
✅ Call log updated: <UUID>
```

---

## 🚀 Baadi: Phase 2 & 3

Alan Phase 1 tamoom shod:
- ✅ Transcripts save mishe
- ✅ Call logs kar mikone
- ✅ Analytics data dare

Baadi:
- ⏳ Phase 2: AI Summarization (GPT-4o-mini)
- ⏳ Phase 3: UI bara Summary/Transcript tabs

Mikhay shoro konim Phase 2 ro?
