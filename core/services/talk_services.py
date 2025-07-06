from django.db import transaction

from core.choices import VoteChoices
from core.models import AppUser, Talk, TalkVote


def create_talk(
    title: str, created_by: AppUser, description: str | None = None
) -> Talk:
    return Talk.objects.create(
        title=title, created_by=created_by, description=description
    )


@transaction.atomic
def upvote_talk(talk: Talk, user: AppUser) -> bool:
    _, created = TalkVote.objects.update_or_create(
        talk=talk, user=user, defaults={"vote": VoteChoices.UP}
    )
    return created


def downvote_talk(talk: Talk, user: AppUser) -> bool:
    _, created = TalkVote.objects.update_or_create(
        talk=talk, user=user, defaults={"vote": VoteChoices.DOWN}
    )
    return created
