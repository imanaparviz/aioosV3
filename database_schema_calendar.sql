-- ============================================================
-- AIOOS Platform - Calendar & Appointment System
-- Database Schema for Supabase PostgreSQL
-- ============================================================

-- ==================== Table: calendar_events ====================
-- Stores all calendar events and appointments

CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,

    -- Event Details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    event_type VARCHAR(50) DEFAULT 'appointment', -- appointment, meeting, call, etc.

    -- Date & Time
    event_date DATE NOT NULL,
    event_time TIME NOT NULL,
    duration_minutes INTEGER NOT NULL DEFAULT 30,
    end_time TIME GENERATED ALWAYS AS (event_time + (duration_minutes || ' minutes')::INTERVAL) STORED,

    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, cancelled, completed

    -- Participant Info (who booked)
    participant_name VARCHAR(255),
    participant_email VARCHAR(255),
    participant_phone VARCHAR(50),

    -- Metadata
    created_by UUID, -- User ID who created this
    created_via VARCHAR(50) DEFAULT 'voice', -- voice, web, api
    notes TEXT,
    metadata JSONB DEFAULT '{}',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_duration CHECK (duration_minutes > 0 AND duration_minutes <= 480),
    CONSTRAINT valid_status CHECK (status IN ('pending', 'confirmed', 'cancelled', 'completed'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_calendar_events_agent_id ON calendar_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_calendar_events_date ON calendar_events(event_date);
CREATE INDEX IF NOT EXISTS idx_calendar_events_status ON calendar_events(status);
CREATE INDEX IF NOT EXISTS idx_calendar_events_agent_date ON calendar_events(agent_id, event_date);


-- ==================== Table: business_hours ====================
-- Stores agent availability configuration

CREATE TABLE IF NOT EXISTS business_hours (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL UNIQUE REFERENCES agents(id) ON DELETE CASCADE,

    -- Working Hours (JSONB format)
    -- Example: {"monday": [{"start": "09:00", "end": "17:00"}], ...}
    working_hours JSONB NOT NULL DEFAULT '{}',

    -- Break Times (JSONB format)
    -- Example: [{"name": "Lunch", "start": "12:00", "end": "13:00", "days": ["monday", "tuesday"]}]
    break_times JSONB DEFAULT '[]',

    -- Default appointment duration (minutes)
    default_appointment_duration INTEGER DEFAULT 45,

    -- Buffer time between appointments (minutes)
    buffer_time_minutes INTEGER DEFAULT 0,

    -- Advance booking settings
    min_advance_booking_hours INTEGER DEFAULT 2, -- Can't book within 2 hours
    max_advance_booking_days INTEGER DEFAULT 90, -- Can book up to 90 days ahead

    -- Timezone
    timezone VARCHAR(100) DEFAULT 'UTC',

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_duration CHECK (default_appointment_duration > 0 AND default_appointment_duration <= 480),
    CONSTRAINT valid_buffer CHECK (buffer_time_minutes >= 0 AND buffer_time_minutes <= 60)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_business_hours_agent_id ON business_hours(agent_id);


-- ==================== Table: availability_exceptions ====================
-- Stores special dates when agent is unavailable (holidays, vacations, etc.)

CREATE TABLE IF NOT EXISTS availability_exceptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID NOT NULL REFERENCES agents(id) ON DELETE CASCADE,

    -- Exception Details
    exception_type VARCHAR(50) DEFAULT 'unavailable', -- unavailable, custom_hours
    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Date Range
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,

    -- Custom hours (if exception_type = 'custom_hours')
    custom_start_time TIME,
    custom_end_time TIME,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Constraints
    CONSTRAINT valid_date_range CHECK (end_date >= start_date),
    CONSTRAINT valid_exception_type CHECK (exception_type IN ('unavailable', 'custom_hours'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_exceptions_agent_id ON availability_exceptions(agent_id);
CREATE INDEX IF NOT EXISTS idx_exceptions_dates ON availability_exceptions(start_date, end_date);


-- ==================== Functions ====================

-- Function: Check if a time slot is available
CREATE OR REPLACE FUNCTION check_time_slot_available(
    p_agent_id UUID,
    p_event_date DATE,
    p_start_time TIME,
    p_duration_minutes INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    v_end_time TIME;
    v_conflict_count INTEGER;
BEGIN
    -- Calculate end time
    v_end_time := p_start_time + (p_duration_minutes || ' minutes')::INTERVAL;

    -- Check for conflicting appointments
    SELECT COUNT(*)
    INTO v_conflict_count
    FROM calendar_events
    WHERE agent_id = p_agent_id
      AND event_date = p_event_date
      AND status IN ('pending', 'confirmed')
      AND (
          -- New appointment starts during existing appointment
          (p_start_time >= event_time AND p_start_time < end_time)
          OR
          -- New appointment ends during existing appointment
          (v_end_time > event_time AND v_end_time <= end_time)
          OR
          -- New appointment encompasses existing appointment
          (p_start_time <= event_time AND v_end_time >= end_time)
      );

    RETURN v_conflict_count = 0;
END;
$$ LANGUAGE plpgsql;


-- Function: Get available time slots for a specific date
CREATE OR REPLACE FUNCTION get_available_slots(
    p_agent_id UUID,
    p_date DATE,
    p_slot_duration INTEGER DEFAULT 30
)
RETURNS TABLE(
    start_time TIME,
    end_time TIME,
    is_available BOOLEAN
) AS $$
DECLARE
    v_business_hours JSONB;
    v_day_of_week TEXT;
    v_working_blocks JSONB;
    v_block JSONB;
    v_current_time TIME;
    v_block_end TIME;
BEGIN
    -- Get day of week (lowercase)
    v_day_of_week := LOWER(TO_CHAR(p_date, 'Day'));
    v_day_of_week := TRIM(v_day_of_week);

    -- Get business hours for this agent
    SELECT working_hours INTO v_business_hours
    FROM business_hours
    WHERE agent_id = p_agent_id;

    -- Get working blocks for this day
    v_working_blocks := v_business_hours -> v_day_of_week;

    -- If no working hours for this day, return empty
    IF v_working_blocks IS NULL THEN
        RETURN;
    END IF;

    -- Loop through each working block
    FOR v_block IN SELECT * FROM jsonb_array_elements(v_working_blocks)
    LOOP
        v_current_time := (v_block->>'start')::TIME;
        v_block_end := (v_block->>'end')::TIME;

        -- Generate time slots for this block
        WHILE v_current_time + (p_slot_duration || ' minutes')::INTERVAL <= v_block_end LOOP
            start_time := v_current_time;
            end_time := v_current_time + (p_slot_duration || ' minutes')::INTERVAL;
            is_available := check_time_slot_available(
                p_agent_id,
                p_date,
                v_current_time,
                p_slot_duration
            );

            RETURN NEXT;

            v_current_time := v_current_time + (p_slot_duration || ' minutes')::INTERVAL;
        END LOOP;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- ==================== Triggers ====================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_calendar_events_updated_at
    BEFORE UPDATE ON calendar_events
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_business_hours_updated_at
    BEFORE UPDATE ON business_hours
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_availability_exceptions_updated_at
    BEFORE UPDATE ON availability_exceptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


-- ==================== Row Level Security (RLS) ====================

-- Enable RLS on all tables
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE business_hours ENABLE ROW LEVEL SECURITY;
ALTER TABLE availability_exceptions ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can read calendar events (for public booking)
CREATE POLICY "Public can read calendar events" ON calendar_events
    FOR SELECT USING (true);

-- Policy: Authenticated users can insert calendar events
CREATE POLICY "Authenticated users can insert calendar events" ON calendar_events
    FOR INSERT WITH CHECK (true);

-- Policy: Everyone can read business hours
CREATE POLICY "Public can read business hours" ON business_hours
    FOR SELECT USING (true);

-- Policy: Authenticated users can manage business hours
CREATE POLICY "Authenticated users can manage business hours" ON business_hours
    FOR ALL USING (true);

-- Policy: Everyone can read availability exceptions
CREATE POLICY "Public can read availability exceptions" ON availability_exceptions
    FOR SELECT USING (true);


-- ==================== Sample Data ====================

-- Insert default business hours for existing agents
INSERT INTO business_hours (agent_id, working_hours, break_times, default_appointment_duration)
SELECT
    id,
    '{
        "monday": [{"start": "09:00", "end": "17:00"}],
        "tuesday": [{"start": "09:00", "end": "17:00"}],
        "wednesday": [{"start": "09:00", "end": "17:00"}],
        "thursday": [{"start": "09:00", "end": "17:00"}],
        "friday": [{"start": "09:00", "end": "17:00"}]
    }'::JSONB,
    '[{"name": "Lunch Break", "start": "12:30", "end": "13:30", "days": ["monday", "tuesday", "wednesday", "thursday", "friday"]}]'::JSONB,
    45
FROM agents
ON CONFLICT (agent_id) DO NOTHING;

-- ==================== Grants ====================

-- Grant permissions to authenticated and anon roles
GRANT SELECT, INSERT, UPDATE ON calendar_events TO authenticated, anon;
GRANT SELECT, INSERT, UPDATE ON business_hours TO authenticated, anon;
GRANT SELECT, INSERT ON availability_exceptions TO authenticated, anon;

-- ============================================================
-- End of Schema
-- ============================================================
