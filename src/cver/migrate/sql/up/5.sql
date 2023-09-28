--- Migration 5 SQL
--- Alter image_build_waitings to have unique contstaints
---
ALTER TABLE image_build_waitings
    ADD CONSTRAINT UNIQUE image_id_build_tag (image_id, image_build_id, tag);

--- End File: cver/src/migrate/sql/up/5.sql
