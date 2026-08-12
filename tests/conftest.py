import copy
import importlib

import pytest
from fastapi.testclient import TestClient

app_module = importlib.import_module("src.app")


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    app_module.activities = copy.deepcopy(original)
    yield
    app_module.activities = copy.deepcopy(original)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
