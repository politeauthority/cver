--- Migration 3 SQL
--- Alter image_builds to have unique constraints
---
ALTER TABLE image_builds
    ADD CONSTRAINT UNIQUE sha (sha),
    ADD CONSTRAINT UNIQUE sha_imported (sha_imported);