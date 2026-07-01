PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS financial_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,

    monthly_income REAL,
    monthly_expenses REAL,

    dependants INTEGER DEFAULT 0,

    employment_type TEXT CHECK (
        employment_type IN ('student', 'salaried', 'self-employed')
    ),

    risk_profile TEXT CHECK (
        risk_profile IN ('low', 'medium', 'high')
    ),

    currency TEXT DEFAULT 'INR',

    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    role TEXT CHECK (
        role IN ('user', 'assistant')
    ),

    message TEXT NOT NULL,

    intent TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id)
);