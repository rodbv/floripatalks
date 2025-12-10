# HTMX View Contracts: Event Topics Platform

**Date**: 2025-12-09  
**Feature**: Event Topics Platform  
**Note**: This system uses HTMX hypermedia pattern (no REST API). All interactions return HTML (full pages or partial fragments).

## View Contracts

### Event Views

#### GET `/events/<slug>/`

**Purpose**: Display event page with topics list

**Request**:
- Method: GET
- Path: `/events/<slug>/` (e.g., `/events/python-floripa/`)
- Headers: Standard browser request

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Full HTML page with topics list
- Template: `events/event_detail.html`

**HTMX Behavior**: None (full page load)

**Data Flow**:
1. View calls use case: `GetEventTopicsUseCase(event_slug)`
2. Use case returns list of TopicDTOs
3. View converts to context, renders template
4. Template receives DTOs (not QuerySets)

---

#### GET `/events/<slug>/topics/load-more/` (HTMX)

**Purpose**: Load more topics for infinite scroll

**Request**:
- Method: GET
- Path: `/events/<slug>/topics/load-more/`
- Headers: `HX-Request: true`
- Query params: `offset=<number>` (number of topics already loaded)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Partial HTML fragment with next batch of topics
- Template: `events/partials/topic_list_fragment.html`

**HTMX Behavior**:
- `hx-get="/events/<slug>/topics/load-more/?offset=20"`
- `hx-trigger="revealed"` (on last topic item)
- `hx-swap="afterend"` (append after last item)

**Data Flow**:
1. View calls use case: `GetEventTopicsUseCase(event_slug, offset=offset)`
2. Use case returns list of TopicDTOs (next batch)
3. View converts to context, renders partial template
4. Returns HTML fragment

---

### Topic Views

#### GET `/topics/<slug>/`

**Purpose**: Display topic detail page

**Request**:
- Method: GET
- Path: `/topics/<slug>/` (e.g., `/topics/advanced-django-orm/`)
- Headers: Standard browser request

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Full HTML page with topic details, comments, presenter suggestions
- Template: `events/topic_detail.html`

**HTMX Behavior**: None (full page load)

**Data Flow**:
1. View calls use case: `GetTopicDetailUseCase(topic_slug)`
2. Use case returns TopicDetailDTO (includes comments, suggestions)
3. View converts to context, renders template

---

#### GET `/topics/create/`

**Purpose**: Display topic creation form

**Request**:
- Method: GET
- Path: `/topics/create/`
- Query params: `event=<slug>` (optional, pre-fill event)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Full HTML page with topic creation form
- Template: `events/topic_form.html`

**Authentication**: Required (redirect to login if not authenticated)

---

#### POST `/topics/create/`

**Purpose**: Create new topic

**Request**:
- Method: POST
- Path: `/topics/create/`
- Headers: `HX-Request: true` (if HTMX), CSRF token
- Body: Form data (`title`, `description`, `event`)

**Response** (HTMX):
- Status: 200 OK (success) or 400 Bad Request (validation error)
- Content-Type: `text/html`
- Body: Partial HTML fragment with new topic item OR error message
- Template: `events/partials/topic_item.html` (success) or `events/partials/error_message.html` (error)

**HTMX Behavior**:
- `hx-post="/topics/create/"`
- `hx-swap="afterbegin"` (prepend to topics list)
- `hx-target="#topics-list"`
- On success: Insert new topic at top of list
- On error: Display error message

**Data Flow**:
1. View calls use case: `CreateTopicUseCase(user, title, description, event_slug)`
2. Use case validates, creates topic, returns TopicDTO
3. View converts to context, renders partial template
4. Returns HTML fragment

---

#### GET `/topics/<slug>/edit/`

**Purpose**: Display topic edit form

**Request**:
- Method: GET
- Path: `/topics/<slug>/edit/`

**Response**:
- Status: 200 OK (if owner) or 403 Forbidden (if not owner)
- Content-Type: `text/html`
- Body: Full HTML page with topic edit form
- Template: `events/topic_edit.html`

**Authentication**: Required
**Authorization**: Must be topic creator

**HTMX Behavior**: None (dedicated page per spec requirement)

---

#### POST `/topics/<slug>/edit/`

**Purpose**: Update topic

**Request**:
- Method: POST
- Path: `/topics/<slug>/edit/`
- Headers: CSRF token
- Body: Form data (`title`, `description`)

**Response**:
- Status: 200 OK (success) or 400 Bad Request (validation error)
- Content-Type: `text/html`
- Body: Full HTML page (redirect to topic detail or event page)
- Template: Redirect after successful update

**HTMX Behavior**: None (dedicated page, browser back button works)

**Data Flow**:
1. View calls use case: `EditTopicUseCase(user, topic_slug, title, description)`
2. Use case validates ownership, updates topic, returns TopicDTO
3. View redirects to topic detail or event page

---

#### POST `/topics/<slug>/delete/`

**Purpose**: Soft delete topic

**Request**:
- Method: POST
- Path: `/topics/<slug>/delete/`
- Headers: CSRF token
- Body: Confirmation (if required)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Partial HTML fragment (remove topic from list) OR redirect
- Template: HTMX removes element, or redirect on full page

**HTMX Behavior**:
- `hx-delete="/topics/<slug>/delete/"`
- `hx-swap="outerHTML"` (remove element)
- `hx-confirm="Are you sure you want to delete this topic?"`

**Data Flow**:
1. View calls use case: `DeleteTopicUseCase(user, topic_slug)`
2. Use case validates ownership, soft deletes topic
3. View returns success response, HTMX removes element

---

#### POST `/topics/<slug>/vote/` (HTMX)

**Purpose**: Vote or un-vote on topic

**Request**:
- Method: POST
- Path: `/topics/<slug>/vote/`
- Headers: `HX-Request: true`, CSRF token

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Partial HTML fragment with updated vote button and count
- Template: `events/partials/vote_button.html`

**HTMX Behavior**:
- `hx-post="/topics/<slug>/vote/"`
- `hx-swap="outerHTML"` (replace vote button)
- `hx-target="#vote-button-<slug>"`

**Data Flow**:
1. View calls use case: `vote_topic(user, topic_slug)` or `unvote_topic(user, topic_slug)`
2. Use case creates or hard-deletes Vote record, returns VoteStatusDTO with updated vote count (calculated from Vote records)
3. View converts to context, renders partial template
4. Returns updated vote button HTML

**Authentication**: Required (returns sign-in popup HTML if not authenticated)

---

### Comment Views

#### POST `/topics/<slug>/comments/create/` (HTMX)

**Purpose**: Add comment to topic

**Request**:
- Method: POST
- Path: `/topics/<slug>/comments/create/`
- Headers: `HX-Request: true`, CSRF token
- Body: Form data (`content`)

**Response**:
- Status: 200 OK (success) or 400 Bad Request (validation error)
- Content-Type: `text/html`
- Body: Partial HTML fragment with new comment OR error message
- Template: `events/partials/comment_item.html` (success)

**HTMX Behavior**:
- `hx-post="/topics/<slug>/comments/create/"`
- `hx-swap="afterbegin"` (prepend to comments list)
- `hx-target="#comments-list"`

**Data Flow**:
1. View calls use case: `AddCommentUseCase(user, topic_slug, content)`
2. Use case validates, creates comment, returns CommentDTO
3. View converts to context, renders partial template

**Authentication**: Required

---

#### GET `/comments/<id>/edit/`

**Purpose**: Display comment edit form

**Request**:
- Method: GET
- Path: `/comments/<id>/edit/`

**Response**:
- Status: 200 OK (if owner) or 403 Forbidden
- Content-Type: `text/html`
- Body: Full HTML page with comment edit form
- Template: `events/comment_edit.html`

**HTMX Behavior**: None (dedicated page)

---

#### POST `/comments/<id>/edit/`

**Purpose**: Update comment

**Request**:
- Method: POST
- Path: `/comments/<id>/edit/`
- Headers: CSRF token
- Body: Form data (`content`)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Redirect to topic detail page

**HTMX Behavior**: None (dedicated page)

---

#### POST `/comments/<id>/delete/` (HTMX)

**Purpose**: Soft delete comment

**Request**:
- Method: POST
- Path: `/comments/<id>/delete/`
- Headers: `HX-Request: true`, CSRF token

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: HTMX removes element

**HTMX Behavior**:
- `hx-delete="/comments/<id>/delete/"`
- `hx-swap="outerHTML"` (remove element)

---

### Presenter Suggestion Views

#### POST `/topics/<slug>/presenters/suggest/` (HTMX)

**Purpose**: Suggest presenter for topic

**Request**:
- Method: POST
- Path: `/topics/<slug>/presenters/suggest/`
- Headers: `HX-Request: true`, CSRF token
- Body: Form data (`email`, `url`, `full_name` - at least one required)

**Response**:
- Status: 200 OK (success) or 400 Bad Request (validation/limit error)
- Content-Type: `text/html`
- Body: Partial HTML fragment with new suggestion OR error message
- Template: `events/partials/presenter_suggestion_item.html`

**HTMX Behavior**:
- `hx-post="/topics/<slug>/presenters/suggest/"`
- `hx-swap="afterbegin"` (prepend to suggestions list)

**Data Flow**:
1. View calls use case: `SuggestPresenterUseCase(user, topic_slug, email, url, full_name)`
2. Use case validates limits (3 per user, 10 per topic), creates suggestion, returns PresenterSuggestionDTO
3. View converts to context, renders partial template

---

#### GET `/presenters/<id>/edit/`

**Purpose**: Display presenter suggestion edit form

**Request**:
- Method: GET
- Path: `/presenters/<id>/edit/`

**Response**:
- Status: 200 OK (if owner) or 403 Forbidden
- Content-Type: `text/html`
- Body: Full HTML page with edit form
- Template: `events/presenter_edit.html`

---

#### POST `/presenters/<id>/edit/`

**Purpose**: Update presenter suggestion

**Request**:
- Method: POST
- Path: `/presenters/<id>/edit/`
- Headers: CSRF token
- Body: Form data (`email`, `url`, `full_name`)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Redirect to topic detail page

---

#### POST `/presenters/<id>/delete/` (HTMX)

**Purpose**: Soft delete presenter suggestion

**Request**:
- Method: POST
- Path: `/presenters/<id>/delete/`
- Headers: `HX-Request: true`, CSRF token

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: HTMX removes element

---

### Authentication Views

#### GET `/accounts/login/`

**Purpose**: Display login page or sign-in popup

**Request**:
- Method: GET
- Path: `/accounts/login/`
- Query params: `next=<url>` (redirect after login)

**Response**:
- Status: 200 OK
- Content-Type: `text/html`
- Body: Login page with Google/LinkedIn SSO buttons OR popup HTML fragment
- Template: `accounts/login.html` or `accounts/login_popup.html` (if HTMX request)

**HTMX Behavior** (for popup):
- Non-authenticated user clicks interactive element
- `hx-get="/accounts/login/?next=<current-url>"`
- `hx-target="#popup-container"`
- `hx-swap="innerHTML"`
- Returns popup HTML fragment

---

#### GET `/accounts/google/login/`

**Purpose**: Initiate Google SSO authentication

**Request**:
- Method: GET
- Path: `/accounts/google/login/`
- Query params: `next=<url>` (redirect after login)

**Response**:
- Status: 302 Redirect
- Location: Google OAuth2 authorization URL

**Managed by**: django-allauth

---

#### GET `/accounts/linkedin/login/`

**Purpose**: Initiate LinkedIn SSO authentication

**Request**:
- Method: GET
- Path: `/accounts/linkedin/login/`
- Query params: `next=<url>` (redirect after login)

**Response**:
- Status: 302 Redirect
- Location: LinkedIn OAuth2 authorization URL

**Managed by**: django-allauth

---

## Error Responses

All views return HTML error responses (not JSON):

- **400 Bad Request**: Validation errors, rate limit exceeded
  - Template: `events/partials/error_message.html` (HTMX) or full error page
  - Contains user-friendly error message

- **403 Forbidden**: Unauthorized action (not owner, etc.)
  - Template: Error page with explanation

- **404 Not Found**: Resource doesn't exist
  - Template: 404 error page

- **500 Internal Server Error**: Server errors
  - Template: 500 error page

## HTMX Response Patterns

### Full Page Responses
- Initial page loads
- Edit pages (dedicated pages per spec)
- Navigation between events

### Partial Fragment Responses
- Infinite scroll loading
- Vote/un-vote actions
- Comment creation
- Topic creation (prepend to list)
- Delete actions (remove element)
- Sign-in popup

## Rate Limiting

Rate limiting applied at view level:
- Topic creation: 10 per hour per user
- Comment creation: 20 per hour per user
- Returns 429 Too Many Requests with HTML error message showing retry time
