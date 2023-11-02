"""
    Cver Test Regression
    CverClient - Model - Tests
    Source: src/cver/cver_client/models/tasks.py

"""
import random

from cver.shared.utils import date_utils
from cver.cver_client.models.task import Task


class TestCverClientModelTask:

    # def test__get(self):
    #     """Test that we can login to the Cver Api and that we store the token locally in a temp
    #     file.
    #     """
    #     ibws = ImageBuildWaitings().get()
    #     assert isinstance(ibws, list)

    def test__save(self):
        """Test that we can login to the Cver Api and that we store the token locally in a temp
        file.
        """
        task = Task()
        task.name = "engine-download"
        task.image_id = random.randint(1000, 1000)
        task.image_build_id = random.randint(1000, 10000)
        task.image_build_waiting_id = random.randint(1000, 10000)
        task.start_ts = date_utils.now()
        task.status = False
        task.status_reason = "this is a test"
        assert task.save()

        saved_task = Task()
        saved_task.get_by_id(task.id)
        assert saved_task.name == task.name
        assert saved_task.image_id == task.image_id
        assert saved_task.image_build_id == task.image_build_id
        assert saved_task.image_build_waiting_id == task.image_build_waiting_id
        assert saved_task.start_ts == task.start_ts.datetime
        assert saved_task.status == task.status
        assert saved_task.status_reason == task.status_reason

# End File: cver/tests/regression/cver_client/models/test_task.py
