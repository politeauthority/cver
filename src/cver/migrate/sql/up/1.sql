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
--- Create clusters
---
CREATE TABLE IF NOT EXISTS clusters (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `org_id` INTEGER NOT NULL,
    `name` VARCHAR(200),
    `maintained` TINYINT(1) DEFAULT True
);

---
--- Create cluster_images
---
CREATE TABLE IF NOT EXISTS cluster_images (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `image_id` INTEGER NOT NULL,
    `cluster_id` INTEGER NOT NULL,
    `first_seen` DATETIME,
    `last_seen` DATETIME,
    UNIQUE KEY `ux_cluster_image` (`image_id`, `cluster_id`)
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
    `name` VARCHAR(200) NOT NULL,
    `registry` VARCHAR(200) NOT NULL,
    `maintained` TINYINT(1) DEFAULT True,
    UNIQUE KEY `ux_registry_image` (`name`, `registry`)
);

--- 
--- Create image_builds
---
CREATE TABLE IF NOT EXISTS image_builds (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `sha` VARCHAR(200) UNIQUE,
    `sha_imported` VARCHAR(200) UNIQUE,
    `image_id` INTEGER NOT NULL,
    `registry` VARCHAR(200) NOT NULL,
    `registry_imported` VARCHAR(200),
    `tags` TEXT,
    `size` INTEGER,
    `os_family` VARCHAR(200),
    `os_name` VARCHAR(200),
    `maintained` TINYINT(1) DEFAULT True,
    `sync_flag` TINYINT(1),
    `sync_enabled` TINYINT(1) DEFAULT True,
    `sync_last_ts` DATETIME,
    `scan_flag` TINYINT(1),
    `scan_enabled` TINYINT(1) DEFAULT True,
    `scan_last_ts` DATETIME
);

--- 
--- Create image_builds_waiting
---
CREATE TABLE IF NOT EXISTS image_build_waitings (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `image_id` INTEGER NOT NULL,
    `image_build_id` INTEGER,
    `sha` VARCHAR(200) UNIQUE,
    `tag` TEXT,
    `waiting` TINYINT(1) DEFAULT True,
    `waiting_for` VARCHAR(200),
    `status` TINYINT(1),
    `status_ts` DATETIME,
    `status_reason` VARCHAR(200),
    `fail_count` INTEGER DEFAULT 0,
     UNIQUE image_id_build_tag (image_id, image_build_id)
);

--- 
--- Create options
---
CREATE TABLE IF NOT EXISTS options (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `type` VARCHAR(200),
    `name` VARCHAR(200) UNIQUE,
    `value` VARCHAR(200),
    `acl_write` TEXT,
    `acl_read` TEXT,
    `hide_value` TINYINT(1)
);

---
--- Create organizations
---
CREATE TABLE IF NOT EXISTS organizations (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200) UNIQUE,
    `email` VARCHAR(200) UNIQUE,
    `last_access` DATETIME
);

---
--- Create roles
---
CREATE TABLE IF NOT EXISTS roles (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200)
);

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
    `name` VARCHAR(200),
    `email` VARCHAR(200),
    `role_id` INTEGER,
    `org_id` INTEGER,
    `last_access` DATETIME
);

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


--- End File: cver/src/migrate/sql/up/1.sql