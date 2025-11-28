# 🎯 Dashboard Completion Plan

## Current Status

### ✅ Analytics Page - 95% Complete
- [x] Frontend component exists
- [x] Backend endpoints exist
- [x] Database functions exist
- [x] Database table exists
- [ ] **Needs**: Minor testing and verification

### ⚠️ Call Logs Page - 40% Complete
- [x] Frontend component exists (with mock data)
- [ ] **Missing**: Backend `/api/calls` endpoint
- [ ] **Missing**: Database integration
- [ ] **Missing**: Real filters functionality
- [ ] **Missing**: Export functionality
- [ ] **Missing**: Play/Transcript functionality

---

## 📋 Step-by-Step Plan

### Phase 1: Analytics Page - Final Testing ✅
**Goal**: Verify everything works

- [ ] 1.1: Start backend server
- [ ] 1.2: Open Analytics page in browser
- [ ] 1.3: Verify metrics load correctly
- [ ] 1.4: Verify chart displays
- [ ] 1.5: Verify top agents display
- [ ] 1.6: Test date range toggle (30d vs 7d)
- [ ] 1.7: Test chart period toggle (Daily/Weekly/Monthly)
- [ ] 1.8: Fix `get_top_agents_analytics` warning (varchar → text)

---

### Phase 2: Call Logs Backend - Create API ⚡
**Goal**: Create `/api/calls` endpoint

- [ ] 2.1: Add `GET /api/calls` endpoint to `main.py`
  - Query `call_logs` table
  - Support filters: agent_id, date_from, date_to, status, search
  - Support pagination: limit, offset
  - Return formatted data

- [ ] 2.2: Add `GET /api/calls/{call_id}` for individual call details

- [ ] 2.3: Test endpoints with Postman/curl

**Expected endpoint**:
```python
@app.get("/api/calls")
async def get_calls(
    agent_id: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    authorization: Optional[str] = Header(None)
):
    # Query call_logs table with filters
    # Return paginated results
```

---

### Phase 3: Call Logs Frontend - Connect Real Data 🔌
**Goal**: Replace mock data with real API calls

- [ ] 3.1: Update `api.js` - ensure `getCallLogs()` is correctly implemented
- [ ] 3.2: Update `CallLogsView.vue`:
  - Replace mock `callLogs.value` with API call
  - Load data on mount
  - Apply filters to API call
  - Update pagination to use API

- [ ] 3.3: Map database fields to UI:
  - `room_name` → `callerId`
  - `agent_id` → lookup agent name
  - `start_time` → `startTime`
  - `duration_seconds` → convert to `MM:SS`
  - `status` → `outcome`

---

### Phase 4: Call Logs Features - Export & Actions 🎬
**Goal**: Implement missing features

- [ ] 4.1: **Export functionality**
  - Add backend endpoint: `GET /api/calls/export` (returns CSV)
  - Update frontend to download CSV

- [ ] 4.2: **Play Recording** (if recordings exist)
  - Check if recordings are saved
  - If yes: Add audio player
  - If no: Hide button or show "Not available"

- [ ] 4.3: **View Transcript** (if available)
  - Check if transcripts are saved in DB
  - If yes: Show in modal/page
  - If no: Hide button

- [ ] 4.4: **Filters - Make functional**
  - Agent filter: Load agents from `/api/agents`
  - Department: Add department to agents table or call_logs
  - Date Range: Implement date picker
  - Outcome: Map to `status` field
  - Duration: Calculate from `duration_seconds`
  - Search: Search in `room_name` or caller info

---

### Phase 5: Final Polish & Testing ✨
**Goal**: Everything works perfectly

- [ ] 5.1: Test Analytics page thoroughly
- [ ] 5.2: Test Call Logs page thoroughly
- [ ] 5.3: Test all filters
- [ ] 5.4: Test pagination
- [ ] 5.5: Test export
- [ ] 5.6: Test dark mode compatibility
- [ ] 5.7: Test mobile responsive design
- [ ] 5.8: Add loading states
- [ ] 5.9: Add empty states (when no data)
- [ ] 5.10: Add error handling

---

## 🚀 Quick Start

### Option A: Analytics Only (Quick Win - 15 min)
```bash
# 1. Restart backend
3-STOP.bat
2-START.bat

# 2. Open browser to Analytics page
http://localhost:5173/analytics

# 3. Make a test call
# 4. Refresh Analytics page
# 5. See data appear!
```

### Option B: Full Implementation (2-3 hours)
Follow all phases above sequentially.

---

## 📝 Notes

- **Recordings**: Check if LiveKit is configured to record calls. If not, we can't play recordings.
- **Transcripts**: Check if STT transcripts are being saved to database. Need to verify this.
- **Department**: Currently `call_logs` table doesn't have department. Need to decide:
  - Add to `call_logs` table? OR
  - Get from `agents` table via `agent_id`?

---

## ❓ Questions to Resolve

1. **Are call recordings being saved?** Where?
2. **Are transcripts being saved to database?**
3. **Should we add `department` field to `call_logs`?**
4. **What additional fields do we need in `call_logs`?**
   - caller_phone_number?
   - customer_id?
   - call_notes?
   - tags?

---

**Priority**: Start with Phase 1 & 2, then decide if recordings/transcripts are needed.
