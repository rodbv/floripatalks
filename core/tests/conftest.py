import pytest


@pytest.fixture
def make_user():
    from model_bakery import baker

    def _make_user(**kwargs):
        return baker.make("core.AppUser", **kwargs)

    return _make_user
