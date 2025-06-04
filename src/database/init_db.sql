CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    currency CHAR(3) NOT NULL,
    balance DECIMAL(15, 2) NOT NULL,
    UNIQUE(user_id, currency)
);

CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    sender_account_id INTEGER REFERENCES accounts(id),
    receiver_account_id INTEGER REFERENCES accounts(id),
    amount DECIMAL(15, 2) NOT NULL,
    currency CHAR(3) NOT NULL,
    exchange_rate DECIMAL(15, 6),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos iniciales
INSERT INTO users (name) VALUES ('X'), ('Y')
ON CONFLICT (name) DO NOTHING;

-- Cuentas para usuario X (ID 1)
INSERT INTO accounts (user_id, currency, balance) 
VALUES 
    (1, 'PEN', 100.00),
    (1, 'USD', 200.00)
ON CONFLICT (user_id, currency) DO UPDATE SET balance = EXCLUDED.balance;

-- Cuentas para usuario Y (ID 2)
INSERT INTO accounts (user_id, currency, balance) 
VALUES 
    (2, 'PEN', 50.00),
    (2, 'USD', 100.00)
ON CONFLICT (user_id, currency) DO UPDATE SET balance = EXCLUDED.balance;