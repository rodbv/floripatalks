import pytest

from core.choices import VoteChoices
from core.services.talk_services import create_talk, downvote_talk, upvote_talk


@pytest.mark.django_db
class TestTalks:
    def test_create_talk_when_given_valid_user_should_create_talk(self, make_user):
        user = make_user(username="testuser", email="testuser@example.com")
        talk = create_talk("Test Talk", user)

        assert talk.title == "Test Talk"
        assert talk.created_by == user
        assert talk.description is None

    def test_upvote_talk_when_user_upvotes_should_create_upvote(self, make_user):
        user = make_user(username="testuser", email="testuser@example.com")
        talk = create_talk("Test Talk", user)

        upvote_talk(talk, user)
        assert talk.votes.count() == 1
        assert talk.votes.first().vote == 1

    def test_upvote_talk_when_user_upvotes_twice_should_not_create_upvote(
        self, make_user
    ):
        user = make_user(username="testuser", email="testuser@example.com")
        talk = create_talk("Test Talk", user)

        upvote_talk(talk, user)
        upvote_talk(talk, user)

        vote = talk.votes.first()
        assert talk.votes.count() == 1
        assert vote.user == user
        assert vote.vote == VoteChoices.UP

    def test_when_upvote_and_downvote_should_store_last_vote(self, make_user):
        user = make_user(username="testuser", email="testuser@example.com")
        talk = create_talk("Test Talk", user)

        upvote_talk(talk, user)
        downvote_talk(talk, user)

        vote = talk.votes.first()
        assert talk.votes.count() == 1
        assert vote.user == user
        assert vote.vote == VoteChoices.DOWN
