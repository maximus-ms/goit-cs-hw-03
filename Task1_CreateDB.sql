-- Table Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table Status
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) unique
);

-- Insert statuses if they are not exist
INSERT INTO status (name)
SELECT 'new'
WHERE NOT EXISTS (SELECT 1 FROM status WHERE name = 'new');

INSERT INTO status (name)
SELECT 'in progress'
WHERE NOT EXISTS (SELECT 1 FROM status WHERE name = 'in progress');

INSERT INTO status (name)
SELECT 'completed'
WHERE NOT EXISTS (SELECT 1 FROM status WHERE name = 'completed');

-- Table Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
