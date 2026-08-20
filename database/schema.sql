
CREATE TABLE IF NOT EXISTS users (
    user_id         SERIAL          PRIMARY KEY,
    full_name       VARCHAR(100)    NOT NULL,
    department      VARCHAR(50)     NOT NULL
                    CHECK (department IN (
                        'Engineering', 'Marketing', 'Finance',
                        'Human Resources', 'Operations', 'Sales', 'Design'
                    )),
    designation     VARCHAR(80)     NOT NULL,
    experience_level VARCHAR(20)   NOT NULL
                    CHECK (experience_level IN ('Junior', 'Mid', 'Senior', 'Lead'))
);
CREATE TABLE IF NOT EXISTS ai_models (
    model_id        SERIAL          PRIMARY KEY,
    model_name      VARCHAR(60)     NOT NULL UNIQUE,
    provider        VARCHAR(60)     NOT NULL
);
CREATE TABLE IF NOT EXISTS prompt_categories (
    category_id     SERIAL          PRIMARY KEY,
    category_name   VARCHAR(60)     NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS prompt_history (
    prompt_id           SERIAL          PRIMARY KEY,
    user_id             INT             NOT NULL
                        REFERENCES users(user_id) ON DELETE CASCADE,
    model_id            INT             NOT NULL
                        REFERENCES ai_models(model_id) ON DELETE RESTRICT,
    category_id         INT             NOT NULL
                        REFERENCES prompt_categories(category_id) ON DELETE RESTRICT,
    prompt_length       INT             NOT NULL CHECK (prompt_length > 0),
    token_count         INT             NOT NULL CHECK (token_count BETWEEN 50 AND 4000),
    response_time_ms    INT             NOT NULL CHECK (response_time_ms BETWEEN 500 AND 12000),
    estimated_cost      NUMERIC(8, 6)   NOT NULL CHECK (estimated_cost >= 0),
    satisfaction_rating SMALLINT        NOT NULL CHECK (satisfaction_rating BETWEEN 1 AND 5),
    created_at          TIMESTAMP       NOT NULL DEFAULT NOW(),
    prompt_complexity   VARCHAR(10)     NOT NULL
                        CHECK (prompt_complexity IN ('Simple', 'Medium', 'Complex')),
    task_completed      BOOLEAN         NOT NULL DEFAULT TRUE,
    response_quality    VARCHAR(10)     NOT NULL
                        CHECK (response_quality IN ('Poor', 'Fair', 'Good', 'Excellent'))
);
CREATE INDEX IF NOT EXISTS idx_prompt_history_created_at
    ON prompt_history(created_at);
CREATE INDEX IF NOT EXISTS idx_prompt_history_user_id
    ON prompt_history(user_id);
CREATE INDEX IF NOT EXISTS idx_prompt_history_model_id
    ON prompt_history(model_id);
CREATE INDEX IF NOT EXISTS idx_prompt_history_category_id
    ON prompt_history(category_id);
CREATE INDEX IF NOT EXISTS idx_prompt_history_model_created
    ON prompt_history(model_id, created_at);
INSERT INTO ai_models (model_name, provider) VALUES
    ('GPT-4o',          'OpenAI'),
    ('Claude Sonnet',   'Anthropic'),
    ('Gemini 2.5',      'Google'),
    ('GitHub Copilot',  'Microsoft'),
    ('DeepSeek',        'DeepSeek AI')
ON CONFLICT (model_name) DO NOTHING;
INSERT INTO prompt_categories (category_name) VALUES
    ('Coding'),
    ('Debugging'),
    ('Research'),
    ('Writing'),
    ('Translation'),
    ('Data Analysis'),
    ('Learning'),
    ('Planning'),
    ('Brainstorming')
ON CONFLICT (category_name) DO NOTHING;
