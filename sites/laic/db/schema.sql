CREATE TABLE IF NOT EXISTS contact_submissions (
    id SERIAL PRIMARY KEY,
    organization_name VARCHAR(200) NOT NULL,
    contact_name VARCHAR(200) NOT NULL,
    email VARCHAR(200) NOT NULL,
    organization_type VARCHAR(120) NOT NULL,
    problem_to_solve TEXT NOT NULL,
    privacy_sensitive BOOLEAN NOT NULL DEFAULT FALSE,
    submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_laic_contact_submissions_submitted_at
    ON contact_submissions (submitted_at DESC);
