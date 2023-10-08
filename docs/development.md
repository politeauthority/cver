# Development

## Testing
- Install the requirements (/tests/requirements.txt)[/tests/requirements.txt]
- Set the env var `CVER_TEST_DIR` to be where the `/tests` path of the repostiroy is stored at.

## Helpful Commands
Drop All tables
```sql
drop table api_keys;
drop table cluster_images;
drop table clusters;
drop table entity_metas;
drop table image_builds;
drop table image_build_waitings;
drop table images;
drop table migrations;
drop table options;
drop table organizations;
drop table perms;
drop table role_perms;
drop table roles;
drop table scans;
drop table scan_raws;
drop table scanners;
drop table softwares;
drop table users;
```

## New Model
Create the following files for a new model.

### Generate files
```bash
MODEL="image_cluster"
MODEL_PLURAL="image_clusters"

# Shared
cp src/cver/shared/models/image.py src/cver/shared/models/${MODEL}_new.py

## -- API -- ##
# Api Model
cp src/cver/api/models/image.py src/cver/api/models/${MODEL}_new.py
# Api Collection
cp src/cver/api/collects/images.py src/cver/api/collects/${MODEL_PLURAL}_new.py
# Api Model Controller
cp src/cver/api/controllers/ctrl_models/ctrl_image.py src/cver/api/controllers/ctrl_models/ctrl_${MODEL}_new.py
# Api Collection Controller
cp src/cver/api/controllers/ctrl_collections/ctrl_images.py src/cver/api/controllers/ctrl_collections/ctrl_${MODEL_PLURAL}_new.py


# Client
cp src/cver/cver_client/models/image.py src/cver/cver_client/models/${MODEL}_new.py
cp src/cver/cver_client/collections/images.py src/cver/cver_client/collections/${MODEL_PLURAL}_new.py

# Tests - Api
cp tests/unit/api/models/test_api_model_image.py tests/unit/api/models/test_api_model_${MODEL}_new.py
# cp tests/unit/api/collections/test_api_model_image.py tests/unit/api/models/test_api_model_${MODEL}.py

# Tests - Shared
cp tests/unit/shared/models/test_shared_model_image.py tests/unit/shared/models/test_shared_model_${MODEL}_new.py

# Tests - Client
cp tests/unit/cver_client/models/test_client_model_image.py tests/unit/api/models/test_client_model_${MODEL}_new.py

```

### Update Files
Add controller routes to `src/cver/api/app.py`
Add rbac info to `src/cver/api/utils/rbac.py`
