-- ============================================================
-- Update German Agent to use Google Gemini 2.0 Flash
-- Run this in Supabase SQL Editor
-- ============================================================

-- Update your German agent (Deutscher Kundenservice) to use Gemini 2.5 Flash
UPDATE agents
SET
    llm_model = 'gemini-2.5-flash',  -- ⭐ Latest stable model, FREE for you!
    updated_at = NOW()
WHERE name = 'Deutscher Kundenservice';

-- Verify the update
SELECT
    id,
    name,
    llm_model,
    tts_voice,
    language,
    updated_at
FROM agents
WHERE name = 'Deutscher Kundenservice';

-- Alternative: If you want to update ALL agents to Gemini 2.5 Flash
-- (Uncomment if needed)
/*
UPDATE agents
SET
    llm_model = 'gemini-2.5-flash',
    updated_at = NOW()
WHERE llm_model LIKE 'gpt-%';  -- Only update OpenAI models
*/
