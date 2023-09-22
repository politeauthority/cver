--- Migration 4 SQL
--- Alter images to have unique contstaints
---
ALTER TABLE images
    ADD CONSTRAINT UNIQUE image_repo (name, repository);

--- End File: cver/src/migrate/sql/up/4.sql
