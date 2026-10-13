\echo === Tables outside the system schemas ===
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

\echo === Columns of support_tickets ===
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'support_tickets'
ORDER BY ordinal_position;

\echo === Keys of support_tickets ===
SELECT tc.constraint_type, tc.constraint_name, kcu.column_name
FROM information_schema.table_constraints AS tc
LEFT JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
 AND tc.table_name = kcu.table_name
WHERE tc.table_name = 'support_tickets'
  AND tc.constraint_type IN ('PRIMARY KEY', 'UNIQUE', 'FOREIGN KEY')
ORDER BY tc.constraint_type, tc.constraint_name;

\echo === Row count ===
SELECT COUNT(*) FROM support_tickets;

\echo === First five rows ===
SELECT * FROM support_tickets LIMIT 5;