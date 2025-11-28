-- Create calendar_events table for voice agent appointment booking
-- This matches the backend API expectations

CREATE TABLE IF NOT EXISTS public.calendar_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL,

    -- Event details
    title TEXT NOT NULL,
    description TEXT,
    event_type TEXT NOT NULL DEFAULT 'appointment' CHECK (event_type IN ('appointment', 'meeting', 'call', 'consultation')),

    -- Timing
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30 CHECK (duration_minutes > 0 AND duration_minutes <= 480),

    -- Participant information
    participant_name TEXT,
    participant_email TEXT,
    participant_phone TEXT,

    -- Status tracking
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed')),
    notes TEXT,

    -- Metadata
    created_via TEXT DEFAULT 'voice',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Foreign key to agents table
    CONSTRAINT fk_agent
      FOREIGN KEY(agent_id)
      REFERENCES public.agents(id)
      ON DELETE CASCADE
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_calendar_events_agent_id ON public.calendar_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_calendar_events_date ON public.calendar_events(event_date);
CREATE INDEX IF NOT EXISTS idx_calendar_events_status ON public.calendar_events(status);
CREATE INDEX IF NOT EXISTS idx_calendar_events_agent_date ON public.calendar_events(agent_id, event_date);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_calendar_events_updated_at
BEFORE UPDATE ON public.calendar_events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comment
COMMENT ON TABLE public.calendar_events IS 'Calendar events and appointments booked via voice agents';

-- Insert some test data for agent "Deutscher Kundenservice" (47addfec-f4cd-41e2-b6ec-6a5e949fe754)
INSERT INTO public.calendar_events (agent_id, title, event_type, event_date, event_time, duration_minutes, participant_name, participant_email, participant_phone, status)
VALUES
  ('47addfec-f4cd-41e2-b6ec-6a5e949fe754', 'Beratungstermin mit Hans Müller', 'consultation', '2025-11-14', '10:00:00', 45, 'Hans Müller', 'hans.mueller@example.de', '+49 30 12345678', 'confirmed'),
  ('47addfec-f4cd-41e2-b6ec-6a5e949fe754', 'Termin mit Frau Schmidt', 'appointment', '2025-11-15', '14:30:00', 30, 'Anna Schmidt', 'anna.schmidt@example.de', '+49 40 98765432', 'pending'),
  ('47addfec-f4cd-41e2-b6ec-6a5e949fe754', 'Telefongespräch mit Herr Weber', 'call', '2025-11-18', '11:00:00', 30, 'Thomas Weber', 'thomas.weber@example.de', '+49 89 55512345', 'confirmed')
ON CONFLICT DO NOTHING;
