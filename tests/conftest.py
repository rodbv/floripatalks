"""
Pytest configuration and shared fixtures for FloripaTalks tests.
"""

# Configure Django settings for pytest
pytest_plugins = ["pytest_django"]

# Fixtures will be added as needed in Phase 2 and beyond
# Example:
# @pytest.fixture
# def user():
#     from accounts.models import User
#     return User.objects.create_user(...)
