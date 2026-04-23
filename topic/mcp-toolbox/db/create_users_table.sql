-- sqlite3 database initialization script for users table
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO users (name, email) VALUES
  ('王小明', 'xiaoming.wang@example.com'),
  ('李小華', 'xiaohua.li@example.com'),
  ('陳怡君', 'yijun.chen@example.com'),
  ('林志豪', 'zhihao.lin@example.com'),
  ('張雅婷', 'yating.zhang@example.com');

-- postgres database initialization script for users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
  ('王小明', 'xiaoming.wang@example.com'),
  ('李小華', 'xiaohua.li@example.com'),
  ('陳怡君', 'yijun.chen@example.com'),
  ('林志豪', 'zhihao.lin@example.com'),
  ('張雅婷', 'yating.zhang@example.com');
  