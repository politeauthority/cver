--- Migration 1 SQL
--- Create initial tables
---
--- Add image_build_id to image_build_waiting
---
ALTER TABLE image_build_waitings
    ADD COLUMN image_build_id INTEGER AFTER image_id;
---
--- Add waiting_for to image_build_waiting
---
ALTER TABLE image_build_waitings
    ADD COLUMN `waiting_for` VARCHAR(200);
