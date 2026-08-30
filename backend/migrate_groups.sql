BEGIN;

ALTER TABLE students ADD COLUMN IF NOT EXISTS group_id INTEGER;

INSERT INTO groups (name)
SELECT DISTINCT "group"
FROM students
WHERE "group" IS NOT NULL
ON CONFLICT (name) DO NOTHING;

UPDATE students
SET group_id = groups.id
FROM groups
WHERE students."group" = groups.name
  AND students.group_id IS NULL;

ALTER TABLE students ALTER COLUMN group_id SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'students_group_id_fkey'
    ) THEN
        ALTER TABLE students
            ADD CONSTRAINT students_group_id_fkey
            FOREIGN KEY (group_id) REFERENCES groups(id);
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS ix_students_group_id ON students (group_id);

COMMIT;