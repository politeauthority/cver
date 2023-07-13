--- Migration 2 SQL
--- Add column to image_builds
---

ALTER TABLE image_builds
    ADD COLUMN `sha_imported` VARCHAR(200) AFTER sha;

--- End File: cver/src/migrate/sql/up/2.sql