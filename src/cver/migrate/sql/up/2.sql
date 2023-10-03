--- Migration 2 SQL
--- Create organization table
---
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

--- End File: cver/src/migrate/sql/up/2.sql
