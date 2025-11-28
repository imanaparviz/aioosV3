-- ============================================================
-- Multi-Tenant Migration for AIOOS Platform
-- Converts platform to SaaS model (like ElevenLabs)
-- Each user has their own agents and calendars
-- ============================================================

-- ==================== STEP 1: Add user_id to agents ====================

-- Add user_id column (nullable first, so existing data doesn't break)
ALTER TABLE public.agents
ADD COLUMN IF NOT EXISTS user_id UUID;

-- Add foreign key constraint to auth.users
ALTER TABLE public.agents
ADD CONSTRAINT fk_agents_user_id
FOREIGN KEY (user_id)
REFERENCES auth.users(id)
ON DELETE CASCADE;

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_agents_user_id ON public.agents(user_id);

-- Add comment
COMMENT ON COLUMN public.agents.user_id IS 'The user who owns this agent (multi-tenant support)';


-- ==================== STEP 2: Add user_id to calendar_events ====================

-- Add user_id column to calendar_events
ALTER TABLE public.calendar_events
ADD COLUMN IF NOT EXISTS user_id UUID;

-- Add foreign key constraint
ALTER TABLE public.calendar_events
ADD CONSTRAINT fk_calendar_events_user_id
FOREIGN KEY (user_id)
REFERENCES auth.users(id)
ON DELETE CASCADE;

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_calendar_events_user_id ON public.calendar_events(user_id);

-- Add comment
COMMENT ON COLUMN public.calendar_events.user_id IS 'The user who owns this calendar event (multi-tenant support)';


-- ==================== STEP 3: Enable Row Level Security (RLS) ====================

-- Enable RLS on agents table
ALTER TABLE public.agents ENABLE ROW LEVEL SECURITY;

-- Enable RLS on calendar_events table
ALTER TABLE public.calendar_events ENABLE ROW LEVEL SECURITY;


-- ==================== STEP 4: Create RLS Policies for agents ====================

-- Policy: Users can only see their own agents
DROP POLICY IF EXISTS "Users can view their own agents" ON public.agents;
CREATE POLICY "Users can view their own agents"
ON public.agents
FOR SELECT
USING (auth.uid() = user_id);

-- Policy: Users can only insert their own agents
DROP POLICY IF EXISTS "Users can create their own agents" ON public.agents;
CREATE POLICY "Users can create their own agents"
ON public.agents
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only update their own agents
DROP POLICY IF EXISTS "Users can update their own agents" ON public.agents;
CREATE POLICY "Users can update their own agents"
ON public.agents
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only delete their own agents
DROP POLICY IF EXISTS "Users can delete their own agents" ON public.agents;
CREATE POLICY "Users can delete their own agents"
ON public.agents
FOR DELETE
USING (auth.uid() = user_id);


-- ==================== STEP 5: Create RLS Policies for calendar_events ====================

-- Policy: Users can only see their own calendar events
DROP POLICY IF EXISTS "Users can view their own calendar events" ON public.calendar_events;
CREATE POLICY "Users can view their own calendar events"
ON public.calendar_events
FOR SELECT
USING (auth.uid() = user_id);

-- Policy: Users can only insert their own calendar events
DROP POLICY IF EXISTS "Users can create their own calendar events" ON public.calendar_events;
CREATE POLICY "Users can create their own calendar events"
ON public.calendar_events
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only update their own calendar events
DROP POLICY IF EXISTS "Users can update their own calendar events" ON public.calendar_events;
CREATE POLICY "Users can update their own calendar events"
ON public.calendar_events
FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can only delete their own calendar events
DROP POLICY IF EXISTS "Users can delete their own calendar events" ON public.calendar_events;
CREATE POLICY "Users can delete their own calendar events"
ON public.calendar_events
FOR DELETE
USING (auth.uid() = user_id);


-- ==================== STEP 6: Create helper function ====================

-- Function to automatically set user_id when creating agents
CREATE OR REPLACE FUNCTION public.set_agent_user_id()
RETURNS TRIGGER AS $$
BEGIN
  -- Auto-set user_id from JWT if not provided
  IF NEW.user_id IS NULL THEN
    NEW.user_id = auth.uid();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to auto-set user_id on agent creation
DROP TRIGGER IF EXISTS set_agent_user_id_trigger ON public.agents;
CREATE TRIGGER set_agent_user_id_trigger
BEFORE INSERT ON public.agents
FOR EACH ROW
EXECUTE FUNCTION public.set_agent_user_id();


-- Function to automatically set user_id when creating calendar events
CREATE OR REPLACE FUNCTION public.set_calendar_event_user_id()
RETURNS TRIGGER AS $$
BEGIN
  -- Auto-set user_id from JWT if not provided
  IF NEW.user_id IS NULL THEN
    NEW.user_id = auth.uid();
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to auto-set user_id on calendar event creation
DROP TRIGGER IF EXISTS set_calendar_event_user_id_trigger ON public.calendar_events;
CREATE TRIGGER set_calendar_event_user_id_trigger
BEFORE INSERT ON public.calendar_events
FOR EACH ROW
EXECUTE FUNCTION public.set_calendar_event_user_id();


-- ==================== DONE! ====================

-- Summary:
-- ✅ Added user_id to agents table
-- ✅ Added user_id to calendar_events table
-- ✅ Created foreign keys to auth.users
-- ✅ Enabled Row Level Security (RLS)
-- ✅ Created RLS policies for data isolation
-- ✅ Created triggers to auto-set user_id from JWT

-- Now the platform is a proper multi-tenant SaaS!
-- Each user can only see and manage their own agents and calendars.
