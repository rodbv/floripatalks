# Data Model: Event Topics Platform

**Date**: 2025-12-09  
**Feature**: Event Topics Platform

## Entities

### Event

Represents a recurring event series (e.g., Python Floripa).

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `name`: CharField(max_length=200) - Event name (e.g., "Python Floripa")
- `slug`: SlugField(unique=True, max_length=100) - URL slug (e.g., "python-floripa")
- `description`: TextField(blank=True, null=True) - Optional event description
- `created_at`: DateTimeField(auto_now_add=True)
- `updated_at`: DateTimeField(auto_now=True)

**Relationships**:
- One-to-many with Topic (one event has many topics)

**Validation**:
- `slug` must be unique
- `name` is required

**Manager**: Default Django manager (no soft delete needed for events)

### Topic

Represents a suggested talk topic for an event.

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `event`: ForeignKey(Event, on_delete=CASCADE, related_name='topics')
- `slug`: SlugField(unique=True, max_length=200) - URL slug for topic
- `title`: CharField(max_length=200) - Topic title
- `description`: TextField(max_length=2000, blank=True, null=True) - Optional description
- `creator`: ForeignKey(User, on_delete=CASCADE, related_name='created_topics')
- `vote_count`: IntegerField(default=0) - Denormalized count for performance
- `is_deleted`: BooleanField(default=False, db_index=True) - Soft delete flag
- `created_at`: DateTimeField(auto_now_add=True)
- `updated_at`: DateTimeField(auto_now=True)

**Relationships**:
- Many-to-one with Event (many topics belong to one event)
- Many-to-one with User (creator)
- One-to-many with Vote (one topic has many votes)
- One-to-many with Comment (one topic has many comments)
- One-to-many with PresenterSuggestion (one topic has many presenter suggestions)

**Validation**:
- `title` is required, max 200 characters
- `description` max 2000 characters if provided
- `vote_count` must be non-negative

**Manager**: Custom SoftDeleteManager that filters `is_deleted=False` by default

**Indexes**:
- `is_deleted` (for soft delete filtering)
- `(event, is_deleted, vote_count, created_at)` - Composite index for list queries

### Vote

Represents a user's vote on a topic.

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `topic`: ForeignKey(Topic, on_delete=CASCADE, related_name='votes')
- `user`: ForeignKey(User, on_delete=CASCADE, related_name='votes')
- `created_at`: DateTimeField(auto_now_add=True)

**Relationships**:
- Many-to-one with Topic (many votes belong to one topic)
- Many-to-one with User (many votes belong to one user)

**Validation**:
- Unique constraint on `(topic, user)` - one vote per user per topic

**Manager**: Default Django manager (no soft delete for votes - deletion removes the vote record)

**Indexes**:
- `(topic, user)` - Unique constraint for one vote per user per topic
- `topic` - For vote count queries

### Comment

Represents a user's comment on a topic.

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `topic`: ForeignKey(Topic, on_delete=CASCADE, related_name='comments')
- `author`: ForeignKey(User, on_delete=CASCADE, related_name='comments')
- `content`: TextField(max_length=1000) - Comment text
- `is_deleted`: BooleanField(default=False, db_index=True) - Soft delete flag
- `created_at`: DateTimeField(auto_now_add=True)
- `updated_at`: DateTimeField(auto_now=True)

**Relationships**:
- Many-to-one with Topic (many comments belong to one topic)
- Many-to-one with User (author)

**Validation**:
- `content` is required, max 1000 characters

**Manager**: Custom SoftDeleteManager that filters `is_deleted=False` by default

**Indexes**:
- `is_deleted` (for soft delete filtering)
- `(topic, is_deleted, created_at)` - For chronological comment listing

### PresenterSuggestion

Represents a suggested presenter for a topic.

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `topic`: ForeignKey(Topic, on_delete=CASCADE, related_name='presenter_suggestions')
- `suggester`: ForeignKey(User, on_delete=CASCADE, related_name='presenter_suggestions')
- `email`: EmailField(blank=True, null=True) - Optional email address
- `url`: URLField(blank=True, null=True) - Optional URL (e.g., LinkedIn)
- `full_name`: CharField(max_length=200, blank=True, null=True) - Optional full name
- `is_deleted`: BooleanField(default=False, db_index=True) - Soft delete flag
- `created_at`: DateTimeField(auto_now_add=True)
- `updated_at`: DateTimeField(auto_now=True)

**Relationships**:
- Many-to-one with Topic (many suggestions belong to one topic)
- Many-to-one with User (suggester)

**Validation**:
- At least one of `email`, `url`, or `full_name` must be provided
- Max 3 suggestions per user per topic (enforced in use case layer)
- Max 10 total suggestions per topic (enforced in use case layer)

**Manager**: Custom SoftDeleteManager that filters `is_deleted=False` by default

**Indexes**:
- `is_deleted` (for soft delete filtering)
- `(topic, suggester, is_deleted)` - For per-user per-topic queries

### User

Represents an authenticated user (custom model inheriting from AbstractUser, not Django's default User model).

**Fields**:
- `id`: UUIDField(primary_key=True, default=uuid.uuid7, editable=False) - UUID v7 primary key
- `email`: EmailField(unique=True)
- `username`: CharField(unique=True, max_length=150)
- `display_name`: CharField(max_length=150) - Name to display in UI
- `created_at`: DateTimeField(auto_now_add=True)
- SSO provider fields (managed by django-allauth)
- Standard AbstractUser fields (password, is_active, is_staff, is_superuser, etc.)

**Relationships**:
- One-to-many with Topic (creator)
- One-to-many with Vote (user's votes)
- One-to-many with Comment (author)
- One-to-many with PresenterSuggestion (suggester)

**Note**: Custom user model MUST be defined before first migration. Inherits from `AbstractUser` following Django best practices. django-allauth will work with custom user model.

## State Transitions

### Topic Lifecycle

1. **Created**: User creates topic → `is_deleted=False`, appears in list
2. **Soft Deleted**: User deletes topic → `is_deleted=True`, hidden from regular users, visible to admins
3. **Recovered**: Admin recovers topic → `is_deleted=False`, appears in list again

### Comment Lifecycle

1. **Created**: User creates comment → `is_deleted=False`, appears in comments list
2. **Edited**: User edits comment → `updated_at` updated, content changed
3. **Soft Deleted**: User deletes comment → `is_deleted=True`, hidden from regular users, visible to admins
4. **Recovered**: Admin recovers comment → `is_deleted=False`, appears in comments list again

### Vote Lifecycle

1. **Created**: User votes on topic → Vote record created, topic `vote_count` incremented
2. **Removed**: User un-votes → Vote record deleted, topic `vote_count` decremented
3. **Re-voted**: User votes again after un-voting → New vote record created, `vote_count` incremented

**Note**: Votes are hard-deleted (no soft delete) since un-voting is an explicit user action.

### PresenterSuggestion Lifecycle

1. **Created**: User suggests presenter → `is_deleted=False`, appears with topic
2. **Edited**: User edits suggestion → `updated_at` updated, fields changed
3. **Soft Deleted**: User deletes suggestion → `is_deleted=True`, hidden from regular users, visible to admins
4. **Recovered**: Admin recovers suggestion → `is_deleted=False`, appears with topic again

## Data Volume Assumptions

- **Events**: Small number (10-50 events)
- **Topics per event**: Up to 1000 topics
- **Votes per topic**: Up to 1000 votes
- **Comments per topic**: Up to 100 comments
- **Presenter suggestions per topic**: Up to 10 suggestions
- **Users**: Unlimited (SSO authentication)

## Query Optimization Strategy

To prevent N+1 queries when loading topics list:

1. **Prefetch related**: `prefetch_related('comments', 'presenter_suggestions')`
2. **Select related**: `select_related('event', 'creator')`
3. **Aggregate vote counts**: Use `vote_count` denormalized field (updated on vote/un-vote)
4. **Count comments**: Use `Count('comments', filter=Q(comments__is_deleted=False))` or denormalize
5. **Convert to DTOs**: After optimization, convert QuerySet to dataclass DTOs before passing to templates

## Soft Delete Implementation

All models with soft delete (Topic, Comment, PresenterSuggestion) use:

```python
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Topic(models.Model):
    objects = SoftDeleteManager()
    all_objects = models.Manager()  # For admin access to deleted items
    # ... fields ...
```

Admin interface uses `all_objects` to access deleted items for recovery.
