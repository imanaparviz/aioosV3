-- Create call_logs table
CREATE TABLE IF NOT EXISTS call_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    agent_id UUID REFERENCES agents(id),
    room_name TEXT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER,
    status TEXT DEFAULT 'ongoing', -- ongoing, completed, failed
    cost NUMERIC(10, 4) DEFAULT 0,
    user_id UUID DEFAULT auth.uid() -- For RLS
);

-- Enable RLS
ALTER TABLE call_logs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to see their own call logs
CREATE POLICY "Users can view their own call logs"
    ON call_logs FOR SELECT
    USING (auth.uid() = user_id);

-- Create policy to allow agents (service role) to insert call logs
-- Note: Service role bypasses RLS, but if we use authenticated client we need this
CREATE POLICY "Users can insert their own call logs"
    ON call_logs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Create policy to allow users to update their own call logs
CREATE POLICY "Users can update their own call logs"
    ON call_logs FOR UPDATE
    USING (auth.uid() = user_id);

-- Function to get analytics summary
CREATE OR REPLACE FUNCTION get_analytics_summary(
    p_user_id UUID DEFAULT auth.uid(),
    p_start_date TIMESTAMP WITH TIME ZONE DEFAULT (now() - INTERVAL '30 days'),
    p_end_date TIMESTAMP WITH TIME ZONE DEFAULT now()
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_total_calls INTEGER;
    v_total_duration INTEGER;
    v_avg_duration NUMERIC;
    v_success_rate NUMERIC;
    v_total_cost NUMERIC;
    v_prev_start_date TIMESTAMP WITH TIME ZONE;
    v_prev_total_calls INTEGER;
    v_call_trend NUMERIC;
BEGIN
    -- Calculate previous period for trend
    v_prev_start_date := p_start_date - (p_end_date - p_start_date);

    -- Current period stats
    SELECT 
        COUNT(*),
        COALESCE(SUM(duration_seconds), 0),
        COALESCE(AVG(duration_seconds), 0),
        COALESCE(SUM(cost), 0)
    INTO 
        v_total_calls,
        v_total_duration,
        v_avg_duration,
        v_total_cost
    FROM call_logs
    WHERE user_id = p_user_id
    AND start_time BETWEEN p_start_date AND p_end_date;

    -- Success rate (completed calls / total calls)
    IF v_total_calls > 0 THEN
        SELECT (COUNT(*) * 100.0 / v_total_calls)
        INTO v_success_rate
        FROM call_logs
        WHERE user_id = p_user_id
        AND start_time BETWEEN p_start_date AND p_end_date
        AND status = 'completed';
    ELSE
        v_success_rate := 0;
    END IF;

    -- Previous period stats (for trend)
    SELECT COUNT(*)
    INTO v_prev_total_calls
    FROM call_logs
    WHERE user_id = p_user_id
    AND start_time BETWEEN v_prev_start_date AND p_start_date;

    -- Calculate trend percentage
    IF v_prev_total_calls > 0 THEN
        v_call_trend := ((v_total_calls - v_prev_total_calls)::NUMERIC / v_prev_total_calls) * 100;
    ELSE
        v_call_trend := 100; -- If 0 before and >0 now, 100% increase (simplified)
    END IF;

    RETURN json_build_object(
        'total_calls', v_total_calls,
        'total_duration_seconds', v_total_duration,
        'avg_duration_seconds', ROUND(v_avg_duration, 1),
        'success_rate', ROUND(v_success_rate, 1),
        'total_cost', ROUND(v_total_cost, 2),
        'call_trend', ROUND(v_call_trend, 1)
    );
END;
$$;

-- Function to get daily call volume
CREATE OR REPLACE FUNCTION get_daily_call_volume(
    p_user_id UUID DEFAULT auth.uid(),
    p_days INTEGER DEFAULT 30
)
RETURNS TABLE (
    day DATE,
    count BIGINT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        start_time::DATE as day,
        COUNT(*) as count
    FROM call_logs
    WHERE user_id = p_user_id
    AND start_time >= (now() - (p_days || ' days')::INTERVAL)
    GROUP BY day
    ORDER BY day ASC;
END;
$$;

-- Function to get top agents
CREATE OR REPLACE FUNCTION get_top_agents_analytics(
    p_user_id UUID DEFAULT auth.uid(),
    p_limit INTEGER DEFAULT 5
)
RETURNS TABLE (
    agent_name TEXT,
    call_count BIGINT
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.name as agent_name,
        COUNT(cl.id) as call_count
    FROM call_logs cl
    JOIN agents a ON cl.agent_id = a.id
    WHERE cl.user_id = p_user_id
    GROUP BY a.name
    ORDER BY call_count DESC
    LIMIT p_limit;
END;
$$;
