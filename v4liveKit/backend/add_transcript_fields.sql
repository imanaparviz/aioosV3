-- Migration: Add Transcript and Summary Fields to call_logs
-- Date: 2025-11-24
-- Purpose: Enable conversation transcript storage and AI summarization

-- Add transcript fields
ALTER TABLE call_logs ADD COLUMN IF NOT EXISTS transcript TEXT;
ALTER TABLE call_logs ADD COLUMN IF NOT EXISTS transcript_json JSONB;

-- Add summary fields (for Phase 2 - AI summarization)
ALTER TABLE call_logs ADD COLUMN IF NOT EXISTS summary TEXT;
ALTER TABLE call_logs ADD COLUMN IF NOT EXISTS summary_json JSONB;

-- Add index for faster transcript searches
CREATE INDEX IF NOT EXISTS idx_call_logs_transcript ON call_logs USING gin(to_tsvector('english', transcript));

-- Add comments for documentation
COMMENT ON COLUMN call_logs.transcript IS 'Full conversation transcript as formatted text (USER: hello\nAGENT: hi there)';
COMMENT ON COLUMN call_logs.transcript_json IS 'Detailed conversation transcript with timestamps and metadata';
COMMENT ON COLUMN call_logs.summary IS 'AI-generated summary of the conversation (brief overview)';
COMMENT ON COLUMN call_logs.summary_json IS 'Structured AI summary with key points, sentiment, action items, and tags';
