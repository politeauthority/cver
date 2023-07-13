--- Migration 1 SQL
--- Create initial tables
---
--- Create api_keys
---
CREATE TABLE IF NOT EXISTS api_keys (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `user_id` INTEGER,
    `client_id` VARCHAR(200) UNIQUE,
    `key` VARCHAR(200),
    `last_access` DATETIME,
    `last_ip` VARCHAR(200),
    `expiration_date` DATETIME,
    `enabled` TINYINT(1) DEFAULT True
);

---
--- Create entity_metas
---
CREATE TABLE IF NOT EXISTS entity_metas (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `entity_type` VARCHAR(200),
    `entity_id` INTEGER,
    `name` VARCHAR(200),
    `type` VARCHAR(200),
    `value` VARCHAR(200)
);

--- 
--- Create images
---
CREATE TABLE IF NOT EXISTS images (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200) UNIQUE,
    `repository` VARCHAR(200) NOT NULL,
    `maintained` TINYINT(1) DEFAULT True
);

--- 
--- Create image_builds
---
CREATE TABLE IF NOT EXISTS image_builds (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `sha` VARCHAR(200),
    `sha_imported` VARCHAR(200),
    `image_id` INTEGER NOT NULL,
    `repository` VARCHAR(200) NOT NULL,
    `repository_imported` VARCHAR(200),
    `tags` TEXT,
    `os_family` VARCHAR(200),
    `os_name` VARCHAR(200),
    `maintained` TINYINT(1) DEFAULT True,
    `sync_flag` TINYINT(1),
    `sync_enabled` TINYINT(1) DEFAULT True,
    `sync_last_ts` DATETIME,
    `scan_flag` TINYINT(1),
    `scan_enabled` TINYINT(1) DEFAULT True,
    `scan_last_ts` DATETIME,
    `pending_operation` VARCHAR(200),
);

--- 
--- Create image_builds_waiting
---
CREATE TABLE IF NOT EXISTS image_build_waitings (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `image_id` INTEGER NOT NULL,
    `tag` VARCHAR(200),
    `waiting` TINYINT(1) DEFAULT True
);

--- 
--- Create options
---
CREATE TABLE IF NOT EXISTS options (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `number` VARCHAR(200) UNIQUE,
    `value` VARCHAR(200))
;

---
--- Create roles
---
CREATE TABLE IF NOT EXISTS roles (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200))
;

---
--- Create role_perms
---
CREATE TABLE IF NOT EXISTS perms (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200))
;

---
--- Create role_perm
---
CREATE TABLE IF NOT EXISTS role_perms (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `role_id` INTEGER,
    `perm_id` INTEGER,
    `enabled` TINYINT(1) DEFAULT True
);

--- 
--- Create scans
---
CREATE TABLE IF NOT EXISTS scans (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `user_id` INTEGER,
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
    `cve_unknown_nums` TEXT,
    `pending_parse` TINYINT(1) DEFAULT True
);

---
--- Create scan_raws
---
CREATE TABLE IF NOT EXISTS scan_raws(
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `user_id` INTEGER,
    `image_id` INTEGER,
    `image_build_id` INTEGER,
    `scanner_id` INTEGER,
    `scan_id` INTEGER,
    `raw` JSON
);

--- 
--- Create scanners
---
CREATE TABLE IF NOT EXISTS scanners (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200)
);

--- 
--- Create softwares
---
CREATE TABLE IF NOT EXISTS softwares (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200),
    `software_id` INTEGER,
    `url_git` VARCHAR(200) UNIQUE,
    `url_marketing` VARCHAR(200)
);

--- 
--- Create users
---
CREATE TABLE IF NOT EXISTS users (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200) UNIQUE,
    `email` VARCHAR(200) UNIQUE,
    `role_id` INTEGER,
    `last_access` DATETIME
);

--- End File: cver/src/migrate/sql/up/1.sql