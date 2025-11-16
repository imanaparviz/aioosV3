# 🤖 Agent Creation & Customization Guide

Complete guide for creating and customizing voice AI agents in the AIOOS platform.

---

## 📋 Table of Contents

1. [Creating a New Agent](#creating-a-new-agent)
2. [Agent Configuration Options](#agent-configuration-options)
3. [System Prompt Customization](#system-prompt-customization)
4. [Advanced Settings](#advanced-settings)
5. [Testing Your Agent](#testing-your-agent)
6. [Best Practices](#best-practices)

---

## 🚀 Creating a New Agent

### Step 1: Navigate to Agent Creation

1. Log in to your admin dashboard at `http://localhost:5173` (or your deployed URL)
2. Click on **"Create Agent"** button
3. You'll see 6 pre-configured templates:
   - **Call Router** - Routes calls to departments
   - **Receptionist** - General inquiries and call forwarding
   - **Booker** - Appointment scheduling ⭐ (Has calendar tools!)
   - **Order Management** - Order status and processing
   - **Customer Service** - Support queries and FAQs
   - **Lead Caller** - Lead qualification

### Step 2: Select a Template

Click on any template card to start configuration. Each template comes with pre-configured:
- System instructions
- Common phrases
- Relevant tools (e.g., Booker has calendar tools)

---

## ⚙️ Agent Configuration Options

### Basic Information

| Field | Description | Example |
|-------|-------------|---------|
| **Agent Name** | Unique identifier for your agent | "Deutscher Kundenservice" |
| **Description** | Optional description of agent's purpose | "German customer service agent for appointment booking" |

### Language & Region

Currently supported languages:
- 🇺🇸 English (United States) - `en-US`
- 🇪🇸 Spanish (Spain) - `es-ES`
- 🇫🇷 French (France) - `fr-FR`
- 🇩🇪 **German (Germany)** - `de-DE` ⭐ (add via database)

**Note:** To add more languages, update the `ConfigureAgentView.vue` file.

### Conversation Messages

#### Welcome Message
The first thing callers hear when connecting.

**Example (English):**
```
Thank you for calling. Please tell me how I can help you today.
```

**Example (German):**
```
Guten Tag! Wie kann ich Ihnen helfen?
```

**⚠️ Keep it short!** Long welcome messages frustrate callers.

#### Transfer Message
What the agent says when transferring to a department.

**Variables you can use:**
- `{{department.name}}` - Department name
- `{{department.phone}}` - Department phone number

**Example:**
```
One moment while I connect you to {{department.name}}.
```

---

## 📝 System Prompt Customization

### How System Instructions Work

Your agent's behavior is controlled by **system instructions** (also called "system prompt"). This tells the AI:
- What role it should play
- How to respond
- What tools it has access to
- Tone and style guidelines

### Current Implementation

**⚠️ Important:** Currently, the UI automatically builds system instructions from your:
1. Welcome Message
2. Transfer Message
3. Department List

**Automatically generated prompt looks like:**
```
You are a Booker voice agent.

Welcome Message: Thank you for calling. Please tell me how I can help you today.

Transfer Message: One moment while I connect you to {{department.name}}.

Available Departments:
- Sales: For new inquiries and purchases. (+1-202-555-0182)
- Support: Technical support. (+1-202-555-0199)
```

### Advanced: Custom System Prompts

If you need full control over your agent's behavior, you can directly edit system instructions in the **database**.

#### Via Supabase Dashboard:

1. Go to Supabase Dashboard → Table Editor
2. Open `agents` table
3. Find your agent row
4. Edit the `system_instructions` column
5. Save changes
6. Restart your agent worker

#### Example Professional System Prompt (German Agent):

```sql
UPDATE agents
SET system_instructions = 'WICHTIGE ANWEISUNGEN - BEFOLGEN SIE DIESE STRENG:

1. KURZE ANTWORTEN: Halten Sie Ihre Antworten kurz und präzise. Maximum 2-3 Sätze.

2. DIREKT ZUM PUNKT: Keine langen Erklärungen. Beantworten Sie die Frage direkt.

3. NATÜRLICH UND FREUNDLICH: Bleiben Sie höflich aber knapp.

4. TERMIN-TOOLS: Sie haben Zugriff auf einen Kalender. Sie können:
   - Termine anzeigen (get_my_appointments)
   - Termine buchen
   - Verfügbarkeit prüfen
   - Termine stornieren

5. BEI TERMINFRAGEN:
   - Nutzen Sie Ihre Tools
   - Bestätigen Sie kurz
   - Keine langen Erklärungen

BEISPIELE FÜR GUTE ANTWORTEN:

❌ SCHLECHT (zu lang):
"Guten Tag! Ich freue mich sehr, dass Sie sich an mich wenden..."

✅ GUT (kurz):
"Hallo! Wie kann ich helfen?"

IHRE HAUPTAUFGABE:
- Professioneller deutscher Kundenservice
- Kurze, klare Antworten (maximal 2-3 Sätze!)
- Termine effizient verwalten
- Kein Small Talk

WICHTIG: Antworten Sie IMMER in maximal 2-3 Sätzen!'
WHERE id = 'your-agent-id';
```

#### Via Backend Script:

We've provided a Python script to update agent instructions:

```bash
cd v4liveKit/backend
python update_agent_instructions.py
```

Edit the script to customize your agent's instructions.

---

## 🔧 Advanced Settings

### Available in Database (Manual Configuration)

| Setting | Column Name | Options | Description |
|---------|-------------|---------|-------------|
| **LLM Model** | `llm_model` | `gpt-4o-mini`, `gpt-4`, `gemini-2.0-flash-exp` | Language model to use |
| **Temperature** | `llm_temperature` | `0.0` - `1.0` | Creativity level (0.3-0.5 recommended for professional agents) |
| **TTS Provider** | `tts_provider` | `azure`, `openai` | Text-to-Speech provider |
| **TTS Voice** | `tts_voice` | `en-US-JennyNeural`, `de-DE-KatjaNeural`, etc. | Voice to use |
| **STT Provider** | `stt_provider` | `azure`, `deepgram` | Speech-to-Text provider |
| **STT Language** | `stt_language` | `en-US`, `de-DE`, etc. | Language for transcription |
| **Status** | `status` | `active`, `inactive` | Agent availability |

### Example Update Query:

```sql
UPDATE agents
SET
  llm_model = 'gemini-2.0-flash-exp',
  llm_temperature = 0.3,
  tts_provider = 'azure',
  tts_voice = 'de-DE-KatjaNeural',
  stt_language = 'de-DE',
  greeting_message = 'Hallo! Ich bin Ihr Terminassistent. Wie kann ich helfen?'
WHERE id = 'your-agent-id';
```

---

## 🎤 Available TTS Voices

### German (Deutsch) Voices 🇩🇪

**Female:**
- `de-DE-KatjaNeural` - Friendly, warm ⭐ RECOMMENDED
- `de-DE-AmalaNeural` - Young, energetic
- `de-AT-IngridNeural` - Austrian, natural
- `de-CH-LeniNeural` - Swiss, clear

**Male:**
- `de-DE-ConradNeural` - Professional, clear
- `de-DE-KillianNeural` - Calm, mature
- `de-AT-JonasNeural` - Austrian, professional
- `de-CH-JanNeural` - Swiss, friendly

### English Voices 🇺🇸

**Female:**
- `en-US-JennyNeural` - Friendly, warm ⭐ RECOMMENDED
- `en-US-AriaNeural` - Natural, conversational
- `en-US-JaneNeural` - Energetic, young
- `en-GB-SoniaNeural` - British, elegant

**Male:**
- `en-US-GuyNeural` - Professional, clear
- `en-US-DavisNeural` - Calm, mature
- `en-GB-RyanNeural` - British, professional

**Full list:** [Azure Speech Service - Language Support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support)

---

## 🧪 Testing Your Agent

### Option 1: Test via Dashboard

1. Click on your agent in the dashboard
2. Click **"Test Agent"** button
3. Allow microphone access
4. Start speaking to test:
   - **General questions:** "Hello, how are you?"
   - **Appointment booking (Booker agent):** "I need to book an appointment"
   - **Calendar check:** "What appointments do I have?"

### Option 2: Test via Direct Link

Your agent will be available at:
```
http://localhost:5173/agents/test/{agent-id}
```

### What to Test:

✅ **Response Quality:**
- Are answers concise?
- Is the tone appropriate?
- Does it understand the language correctly?

✅ **Tool Usage (for Booker agents):**
- Can it check available appointments?
- Can it book new appointments?
- Can it handle conflicts (double-booking)?

✅ **Error Handling:**
- What happens if you ask something it can't do?
- Does it gracefully decline or ask for clarification?

---

## 💡 Best Practices

### 1. Keep System Prompts Concise

❌ **Bad (Too Long):**
```
You are an extremely helpful, friendly, and professional AI voice assistant
created to help customers with all their needs. You should always strive to
provide the most comprehensive and detailed answers possible, making sure to
explain every single aspect thoroughly and completely...
```

✅ **Good (Concise):**
```
You are a professional voice assistant. Keep answers short (2-3 sentences max).
Be helpful and friendly. Use available tools when needed.
```

### 2. Set Appropriate Temperature

- **0.0 - 0.3:** Very predictable, consistent (good for factual responses)
- **0.3 - 0.5:** Balanced, professional ⭐ **RECOMMENDED**
- **0.6 - 0.8:** More creative, conversational
- **0.9 - 1.0:** Very creative, unpredictable (not recommended for business)

### 3. Test in Target Language

Always test your agent in the actual language it will be used in:
- German agent? Test in German!
- Check for:
  - Proper pronunciation
  - Cultural appropriateness
  - Local expressions

### 4. Monitor Agent Performance

Check regularly:
- Average call duration (should be < 3 minutes for most cases)
- Success rate (completed tasks / total calls)
- User feedback

### 5. Iterate Based on Real Usage

After deploying:
1. Listen to call recordings (if enabled)
2. Identify common issues
3. Update system instructions
4. Test again
5. Repeat

---

## 🚨 Common Issues & Solutions

### Issue: Agent talks too much

**Solution:** Add to system instructions:
```
IMPORTANT: Keep ALL responses under 2-3 sentences. Be direct and concise.
```

Also consider lowering temperature to 0.3.

### Issue: Agent doesn't use tools

**Solution:**
1. Check that tools are enabled for your agent (check `agent_worker.py`)
2. Add explicit instructions:
```
You have access to calendar tools. Use them when users ask about appointments.
```

### Issue: Wrong language/accent

**Solution:** Update both:
- `stt_language` - for understanding
- `tts_voice` - for speaking

Example for German:
```sql
UPDATE agents SET
  stt_language = 'de-DE',
  tts_voice = 'de-DE-KatjaNeural'
WHERE id = 'your-agent-id';
```

### Issue: Agent crashes or doesn't speak

**Solution:**
1. Check backend logs: `v4liveKit/backend/`
2. Check agent worker is running
3. Restart the platform: `3-STOP.bat` then `2-START.bat`

---

## 📚 Additional Resources

- **LiveKit Agents Documentation:** [https://docs.livekit.io/agents](https://docs.livekit.io/agents)
- **Azure TTS Voices:** [https://learn.microsoft.com/azure/ai-services/speech-service/language-support](https://learn.microsoft.com/azure/ai-services/speech-service/language-support)
- **OpenAI Function Calling:** [https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
- **Gemini API:** [https://ai.google.dev/gemini-api/docs](https://ai.google.dev/gemini-api/docs)

---

## 🎯 Roadmap: Future Features

We're planning to add direct UI support for:

- [ ] **Advanced Settings Tab** in agent configuration
  - Direct system prompt editor (textarea)
  - LLM model selector
  - Temperature slider
  - Voice selection dropdown
- [ ] **Tool Management** - Enable/disable specific tools per agent
- [ ] **A/B Testing** - Test multiple system prompts
- [ ] **Analytics Dashboard** - Performance metrics per agent
- [ ] **Version Control** - Save and rollback system prompts

---

## 💬 Questions?

If you have questions about agent customization:
1. Check this guide first
2. Check backend logs for errors
3. Review the `agent_worker.py` file for technical details

**Happy Agent Building!** 🚀
