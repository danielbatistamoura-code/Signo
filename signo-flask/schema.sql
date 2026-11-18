-- Schema SQLite — Qual é o seu signo? (Flask + SQL)
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthdate TEXT NOT NULL,
    sign_key TEXT NOT NULL,
    sign_name TEXT NOT NULL,
    element TEXT NOT NULL,
    modality TEXT NOT NULL,
    ruler TEXT NOT NULL,
    lucky_numbers TEXT NOT NULL,
    compatibility TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_submissions_sign_name ON submissions(sign_name);
