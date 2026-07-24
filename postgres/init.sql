CREATE TABLE IF NOT EXISTS urls (
    url_id BIGINT PRIMARY KEY,
    long_url TEXT NOT NULL,
    short_code VARCHAR(15) NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS isx_urls_short_code ON urls(short_code);

COMMENT ON TABLE urls IS 'URL адреса и их сокращения';
COMMENT ON COLUMN urls.url_id IS 'Twitter Snowflake ID URL адреса';
COMMENT ON COLUMN urls.long_url IS 'Исходный "длинный" URL адрес';
COMMENT ON COLUMN urls.short_code IS 'Сокращенный код URL адресв';

