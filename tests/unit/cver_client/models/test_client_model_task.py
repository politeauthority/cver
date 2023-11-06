"""
    Cver Client Unit Test
    Client Model: Task
    Source: cver/src/cver/cver_client/model/task.py

"""
import random

from cver.client.models.task import Task


class TestClientModelTask:

    def test____init__(self):
        """Test the Task Model's initialization.
        :method: Task().__init__
        """
        task = Task()
        assert task
        assert hasattr(task, "id")
        assert hasattr(task, "created_ts")
        assert hasattr(task, "updated_ts")
        assert hasattr(task, "user_id")
        assert hasattr(task, "name")
        assert hasattr(task, "image_id")
        assert hasattr(task, "image_build_id")
        assert hasattr(task, "image_build_waiting_id")
        assert hasattr(task, "status")
        assert hasattr(task, "status_reason")
        assert hasattr(task, "start_ts")
        assert hasattr(task, "end_ts")

    def test____repr__(self):
        """Test the model's representation.
        :method: Task().__repr__
        """
        model = Task()
        assert str(model) == "<Task>"

        model.id = 1
        assert str(model) == "<Task: 1>"

    def test____get_model_fields(self):
        model = Task()
        model.name = "engine-download"
        model.image_id = random.randint(1000, 1000)
        model.image_build_id = random.randint(1000, 1000)
        model.image_build_waiting_id = random.randint(1000, 1000)
        model.status = False
        model.status_reason = "hello-world"
        data = model._get_model_fields()
        assert "id" not in data
        assert model.status == data["status"]
        model


# End File: cver/tests/cver_client/models/test_client_model_task.py
