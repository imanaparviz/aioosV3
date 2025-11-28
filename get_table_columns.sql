-- Get column information for call_logs table
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM
    information_schema.columns
WHERE
    table_name = 'call_logs'
    AND table_schema = 'public'
ORDER BY
    ordinal_position;
