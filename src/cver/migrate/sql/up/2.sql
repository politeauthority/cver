--- Migration 2 SQL
--- Add imported columns to image_builds
---

ALTER TABLE image_builds
    ADD COLUMN `sha_imported` VARCHAR(200) AFTER `sha`;
    ADD COLUMN `repository_imported` VARCHAR(200) AFTER `repository`;

--- End File: cver/src/migrate/sql/up/2.sql
