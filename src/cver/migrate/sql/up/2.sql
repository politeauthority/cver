--- Migration 2 SQL
--- Create RBAC tables
---
--- Create roles
---
CREATE TABLE IF NOT EXISTS roles (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200));

---
--- Create role_perms
---
CREATE TABLE IF NOT EXISTS perms (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `name` VARCHAR(200),
    `slug_name` VARCHAR(200));

---
--- Create role_perm
---
CREATE TABLE IF NOT EXISTS role_perms (
    `id` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `created_ts` DATETIME,
    `updated_ts` DATETIME,
    `role_id` INTEGER,
    `perm_id` INTEGER,
    `enabled` TINYINT(1) DEFAULT True);

--- End File: cver/src/migrate/sql/up/2.sql

