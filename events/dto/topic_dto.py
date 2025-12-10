"""
Topic DTO for transferring topic data to templates.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TopicDTO:
    """
    Data Transfer Object for Topic model.

    Used to transfer topic data from services/use cases to templates,
    preventing N+1 queries by ensuring all related data is loaded upfront.
    """

    id: UUID
    slug: str
    title: str
    description: str | None
    vote_count: int
    creator_username: str
    event_slug: str
    event_name: str
    created_at: datetime
