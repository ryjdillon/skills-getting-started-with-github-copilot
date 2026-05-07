import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

# Store the original state of activities
original_activities = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities state before each test."""
    global activities
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app."""
    return TestClient(app)