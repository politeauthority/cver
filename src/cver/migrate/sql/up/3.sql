--- Migration 3 SQL
--- Create Scan Raw
---
--- Create scan_raw
---
CREATE TABLE IF NOT EXISTS scan_raws (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `image_id` INTEGER,
    `image_build_id` INTEGER,
    `scanner_id` INTEGER,
    `cve_critical_int` INTEGER,
    `cve_critical_nums` TEXT,
    `cve_high_int` INTEGER,
    `cve_high_nums` TEXT,
    `cve_medium_int` INTEGER,
    `cve_medium_nums` TEXT,
    `cve_low_int` INTEGER,
    `cve_low_nums` TEXT,
    `cve_unknown_int` INTEGER,
    `cve_unknown_nums` TEXT);

--- End File: cver/src/migrate/sql/up/3.sql