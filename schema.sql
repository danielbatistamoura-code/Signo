-- Estrutura da tabela SQLite utilizada pelo Oráculo Zodíaco Profissional
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_code TEXT NOT NULL,
    name TEXT NOT NULL,
    dob TEXT NOT NULL,
    tob TEXT,
    age INTEGER NOT NULL,
    sign_name TEXT NOT NULL,
    ascendant TEXT NOT NULL,
    moon TEXT NOT NULL,
    entry_time TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Ativa',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
