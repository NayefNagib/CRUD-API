CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO tasks (title, done)
SELECT 'Learn FastAPI', FALSE
WHERE NOT EXISTS (
    SELECT 1 FROM tasks
);

INSERT INTO tasks (title, done)
SELECT 'Build CRUD API', FALSE
WHERE NOT EXISTS (
    SELECT 1 FROM tasks
    WHERE title = 'Build CRUD API'
);

INSERT INTO tasks (title, done)
SELECT 'Publish project to GitHub', FALSE
WHERE NOT EXISTS (
    SELECT 1 FROM tasks
    WHERE title = 'Publish project to GitHub'
);