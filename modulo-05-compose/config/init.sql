-- Criar extensoes necessarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar tabela de usuarios
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar tabela de tarefas
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar indices para performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);

-- Inserir usuario padrao (senha: admin123)
INSERT INTO users (username, email, password_hash) 
VALUES ('admin', 'admin@taskmanager.local', 'pbkdf2:sha256:260000$salt$hash')
ON CONFLICT (username) DO NOTHING;

-- Inserir tarefas de exemplo
INSERT INTO tasks (user_id, title, description, completed) 
VALUES 
    (1, 'Configurar Docker Compose', 'Aprender orquestracao multi-container', false),
    (1, 'Adicionar PostgreSQL', 'Migrar dados para banco relacional', true),
    (1, 'Implementar Redis', 'Adicionar cache para performance', false),
    (1, 'Configurar Nginx', 'Setup de proxy reverso', false)
ON CONFLICT DO NOTHING;

-- Log de inicializacao
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
END $$;