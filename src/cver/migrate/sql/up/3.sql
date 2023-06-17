--- Migration 3 SQL
--- Create Scan Raw
---
--- Create scan_raws
---
CREATE TABLE IF NOT EXISTS scan_raws(
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `image_id` INTEGER,
    `image_build_id` INTEGER,
    `scanner_id` INTEGER,
    `scan_id` INTEGER,
    `raw` JSON);

--- End File: cver/src/migrate/sql/up/3.sql