--- Migration 2 SQL
--- Create task tables
---
--- Create tasks
---
CREATE TABLE IF NOT EXISTS tasks (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `user_id` INTEGER,
    `name` VARCHAR(200),
    `image_id` INTEGER,
    `image_build_id` INTEGER,
    `image_build_waiting_id` INTEGER,
    `status` TINYINT(1),
    `status_reason` VARCHAR(200),
    `start_ts` DATETIME,
    `end_ts` DATETIME
);
