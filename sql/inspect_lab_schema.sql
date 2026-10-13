\echo === Columns of lab.orders ===
SELECT column_name, data_type, character_maximum_length, numeric_precision, numeric_scale, is_nullable
FROM information_schema.columns
WHERE table_schema = 'lab' AND table_name = 'orders'
ORDER BY ordinal_position;

\echo === Constraints of lab.orders ===
SELECT conname, pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'lab.orders'::regclass
ORDER BY conname;