# Users Schema

## Table: `users`

| Column | Type | Nullable | Default | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| `id` | `INTEGER` | No | - | `PRIMARY KEY`, `AUTOINCREMENT` | 使用者唯一識別碼 |
| `name` | `TEXT` | No | - | - | 使用者名稱 |
| `email` | `TEXT` | No | - | `UNIQUE` | 使用者 Email（不可重複） |
| `created_at` | `DATETIME` | No | `CURRENT_TIMESTAMP` | - | 建立時間 |
| `updated_at` | `DATETIME` | No | `CURRENT_TIMESTAMP` | - | 更新時間 |

## DDL

```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```
