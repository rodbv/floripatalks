# Tasks: Event Topics Platform

**Input**: Design documents from `/specs/001-event-topics-platform/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD is required per constitution - all tests must be written before implementation code.

**User Story Design (Principle XVI)**: All user stories are designed as standalone, independently testable deliveries that deliver value by themselves. Each user story phase includes:
- **Standalone Delivery**: Independently completable without depending on other stories
- **Independent Test**: Clear test criteria verifiable by Product Owner (included in each phase)
- **Visual Verification**: Verifiable through frontend or Django Admin
- **Value Delivery**: Each story delivers tangible value
- **Output-First Approach**: Viewing/interaction features prioritized before content creation

**MVP Scope Limitations** (per clarifications):
- Admin access: Django superuser only (no custom role system)
- User profile editing: Not in MVP (users use SSO-provided info only)
- Content reporting/flagging: Not in MVP (admins monitor manually via Django admin)
- Analytics/tracking: Not in MVP (focus on core functionality)

**GitHub Issues**: Create a GitHub issue ONLY for the task currently being worked on (not in advance for entire phases). Branch names MUST follow pattern: `{issue-id}-{description-in-slug-format}` (e.g., `029-custom-user-model`). This prevents issues from becoming outdated when tasks are reordered or changed.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Django web application structure per plan.md
- Apps: `events/`, `accounts/`, `core/`
- Tests: `tests/unit/`, `tests/integration/`
- Static: `static/js/`, `static/css/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

### Initial Project Setup

- [x] T001 Initialize Python project with `uv`: create `pyproject.toml` with Python 3.13+ requirement
- [x] T002 [P] Add Django to project using `uv add django` (adds to `pyproject.toml` and installs)
- [x] T003 [P] Add django-allauth using `uv add django-allauth` for SSO authentication
- [x] T004 [P] Add django-cotton using `uv add django-cotton` for component-based UI
- [x] T005 [P] Add django-htmx using `uv add django-htmx` for Django HTMX integration helpers
- [x] T006 [P] Add pytest and pytest-django using `uv add pytest pytest-django` for testing
- [x] T007 [P] Run `uv sync` to install all dependencies and generate `uv.lock` file
- [x] T008 Create Django project structure: run `django-admin startproject floripatalks` to create project root with `manage.py`

### Django Apps and Structure

- [x] T009 [P] Create Django app `events`: run `python manage.py startapp events` in project root
- [x] T010 [P] Create Django app `accounts`: run `python manage.py startapp accounts` in project root
- [x] T011 [P] Create Django app `core`: run `python manage.py startapp core` in project root
- [x] T012 [P] Setup Django settings structure: create `floripatalks/settings/` directory with `__init__.py`, `base.py`, `development.py`, `production.py`
- [x] T013 [P] Configure `floripatalks/urls.py` with app routing: include `events.urls`, `accounts.urls`
- [x] T014 [P] Create `tests/` directory structure: `tests/unit/`, `tests/integration/`, `tests/conftest.py` with `__init__.py` files

### Static Files and Assets

- [x] T015 [P] Setup static files configuration in `floripatalks/settings/base.py`: `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`
- [x] T016 [P] Create static files directories: `static/js/`, `static/css/pure-css/`
- [x] T017 [P] Download HTMX latest version to `static/js/htmx.min.js` (from https://htmx.org/)
- [x] T018 [P] Download AlpineJS latest version to `static/js/alpine.min.js` (from https://alpinejs.dev/)
- [x] T019 [P] Download Pure CSS latest version to `static/css/pure-css/pure-min.css` (from https://purecss.io/)

### Development Tools

- [x] T020 [P] Create `justfile` with common tasks: `just test` (run pytest), `just dev` (runserver), `just migrate`, `just lint`, `just format`
- [x] T021 [P] Create `.gitignore` for Python/Django project (include `.venv/`, `.uv/`, `uv.lock`, `db.sqlite3`, `__pycache__/`, etc.)

### Pre-commit Hooks

- [x] T022 [P] Install pre-commit: `uv add --dev pre-commit ruff`
- [x] T023 [P] Create `.pre-commit-config.yaml` with hooks: ruff (formatting/linting, line length 100), Django checks, auto-fix enabled
- [x] T024 [P] Initialize pre-commit: run `pre-commit install` to setup git hooks

### GitHub Actions CI/CD

- [x] T025 [P] Create `.github/workflows/ci.yml` with workflow to:
  - Run on push and pull requests
  - Setup Python 3.13+ with uv
  - Install dependencies with `uv sync`
  - Run tests with `pytest` via `just test`
  - Run linting/formatting checks
  - Fail build if any check fails

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Note**: Create GitHub issues only for the task currently being worked on, not in advance for entire phases. This prevents issues from becoming outdated when tasks are reordered or changed.

- [x] T026 Create custom User model in `accounts/models.py` inheriting from `AbstractUser` with UUID v6 primary key
- [x] T027 [P] Create User migration: `accounts/migrations/0001_initial.py` (MUST be first migration)
- [x] T028 [P] Configure django-allauth for Google SSO in `floripatalks/settings/base.py` (LinkedIn SSO planned for future release)
- [x] T029 [P] Setup database configuration: SQLite for all environments (development and production) in `floripatalks/settings/base.py`
- [x] T030 [P] Configure django-htmx in `floripatalks/settings/base.py`: add `django_htmx` to `INSTALLED_APPS`
- [x] T031 [P] Configure django-cotton in `floripatalks/settings/base.py`: add `django_cotton` to `INSTALLED_APPS`
- [x] T032 [P] Create base templates directory: `templates/base.html` with HTMX includes (AlpineJS optional/commented)
- [x] T033 [P] Create base model classes in `core/models.py`: `BaseModel` (UUID v6, created_at, updated_at) and `SoftDeleteModel` (extends BaseModel with is_deleted and SoftDeleteManager)
- [x] T034 [P] Setup i18n configuration: Portuguese (pt-BR) as primary language, timezone America/Sao_Paulo in `floripatalks/settings/base.py`
- [x] T035 [P] Create `core/utils.py` for shared utilities
- [x] T036 [P] Configure Django admin in `accounts/admin.py` for User model (file exists but empty)
- [x] T037 [P] Create base Django-Cotton component structure: `events/cotton/`, `accounts/cotton/` directories
- [x] T038 [P] Setup pytest configuration: `pytest.ini` or `pyproject.toml` pytest section with Django settings
- [x] T039 [P] Create test fixtures in `tests/conftest.py`: user fixtures, event fixtures (partial: user fixtures exist, event fixtures cannot exist yet)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Browse Topics (Priority: P1) 🎯 MVP - Output-First

**Goal**: Users (logged in or not) can view a list of topics for an event, see vote counts and comment counts, browse with infinite scroll. Non-authenticated users are redirected to login when clicking interactive elements.

**Independent Test**: A user (logged in or not) can navigate to `/events/python-floripa/` and see a list of topics with vote counts and comment counts displayed. Topics load in batches of 20 via infinite scroll. Non-authenticated users see interactive buttons but receive sign-in prompts when clicking them.

**Output-First Rationale**: This is the foundation - users must be able to see existing content before they can interact with it or create new content.

### Tests for User Story 1 (TDD - Write First)

- [x] T040 [P] [US1] Unit test for Event model in `tests/unit/events/test_models.py`
- [x] T041 [P] [US1] Unit test for Topic model in `tests/unit/events/test_models.py`
- [x] T042 [P] [US1] Unit test for TopicDTO with `assertNumQueries` from `pytest_django.asserts` in `tests/unit/events/test_dto/test_topic_dto.py`
- [x] T043 [P] [US1] Unit test for get_topics_for_event function in `tests/unit/events/test_services/test_topic_service.py`
- [x] T044 [P] [US1] Unit test for get_event_topics function in `tests/unit/events/test_use_cases/test_get_event_topics.py`
- [x] T045 [P] [US1] Integration test for event detail view in `tests/integration/events/test_event_detail_view.py`

### Implementation for User Story 1

- [x] T046 [P] [US1] Create Event model in `events/models.py` inheriting from `BaseModel` with slug, name, description
- [x] T047 [P] [US1] Create Topic model in `events/models.py` inheriting from `SoftDeleteModel` with slug (auto-generated), title, description, event FK, creator FK (no vote_count field - votes are counted at runtime)
- [x] T049 [US1] Create migrations for Event and Topic models: `events/migrations/0001_initial.py`
- [x] T050 [P] [US1] Create TopicDTO dataclass in `events/dto/topic_dto.py`
- [x] T051 [P] [US1] Create get_topics_for_event function in `events/services/topic_service.py` (use Count('votes') annotation for vote_count, prefetch, select_related, convert to DTOs)
- [x] T052 [US1] Create get_event_topics function in `events/use_cases/get_event_topics.py` (calls get_topics_for_event service function, returns DTOs)
- [x] T053 [US1] Create event detail view in `events/views.py` for GET `/events/<slug>/` (calls use case, passes DTOs to template)
- [x] T054 [US1] Create HTMX view for infinite scroll in `events/views.py` for GET `/events/<slug>/topics/load-more/` (returns partial fragment)
- [x] T055 [US1] Create URL patterns in `events/urls.py` for event detail and load-more endpoints
- [x] T056 [US1] Create base template `templates/base.html` with HTMX, Pure CSS includes (AlpineJS optional/commented)
- [x] T057 [US1] Create event detail template `events/templates/events/event_detail.html` with topics list
- [x] T058 [US1] Create topic list partial template `events/templates/events/partials/topic_list_fragment.html` for HTMX infinite scroll
- [x] T059 [US1] Create Django-Cotton topic card component `events/cotton/topic/card.html`
- [x] T060 [US1] ~~Create HTMX sign-in popup component~~ (REMOVED: Replaced with redirect approach using `HttpResponseClientRedirect`)
- [x] T061 [US1] ~~Integrate sign-in popup in event detail template~~ (REMOVED: Replaced with `@require_authentication` decorator)
- [x] T062 [US1] Configure comprehensive admin for Event and Topic models in `events/admin.py` with inlines for Topic (manage topics from Event page), list_display, list_filter, search_fields, fieldsets, and readonly_fields. Topic admin should show event relationship and support filtering by event.
- [x] T063 [US1] Create initial Event (Python Floripa) via Django admin or data migration

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can view topics list with infinite scroll.

---

## Phase 4: User Story 3 - Vote and Un-vote on Topics (Priority: P1) 🎯 Output-First

**Goal**: Logged-in users can vote on topics they want to see as talks. Each user can vote once per topic and can later un-vote (remove their vote). The vote count is displayed and updates in real-time when users vote or un-vote.

**Independent Test**: A logged-in user can click vote button, see count increment, then un-vote and see count decrement. Vote button state reflects user's vote status.

**Output-First Rationale**: Voting allows users to immediately engage with existing content. This is prioritized over creating new content (output-first approach).

### Tests for User Story 3 (TDD - Write First)

- [ ] T064 [P] [US3] Unit test for Vote model in `tests/unit/events/test_models.py`
- [ ] T065 [P] [US3] Unit test for vote_topic service function in `tests/unit/events/test_services/test_vote_service.py`
- [ ] T066 [P] [US3] Unit test for unvote_topic service function in `tests/unit/events/test_services/test_vote_service.py`
- [ ] T067 [P] [US3] Unit test for vote_topic function in `tests/unit/events/test_use_cases/test_vote_topic.py`
- [ ] T068 [P] [US3] Unit test for unvote_topic function in `tests/unit/events/test_use_cases/test_unvote_topic.py`
- [ ] T069 [P] [US3] Integration test for vote/unvote flow in `tests/integration/events/test_vote_flow.py`

### Implementation for User Story 3

- [ ] T070 [US3] Create Vote model in `events/models.py` inheriting from `BaseModel` with topic FK, user FK, unique constraint (topic, user)
- [ ] T071 [US3] Create migration for Vote model: `events/migrations/0002_vote.py`
- [ ] T072 [US3] Create vote service functions in `events/services/vote_service.py`: vote_topic, unvote_topic, get_user_vote_status
- [ ] T073 [US3] Create vote_topic function in `events/use_cases/vote_topic.py` (validates, creates Vote record, returns status DTO)
- [ ] T074 [US3] Create unvote_topic function in `events/use_cases/unvote_topic.py` (validates, hard-deletes Vote record, returns status DTO)
- [ ] T075 [US3] Create vote/unvote HTMX view in `events/views.py` for POST `/topics/<slug>/vote/` (toggles vote/unvote)
- [ ] T076 [US3] Add URL pattern in `events/urls.py` for vote endpoint
- [ ] T077 [US3] Create vote button partial template `events/templates/events/partials/vote_button.html` with HTMX attributes
- [ ] T078 [US3] Create Django-Cotton vote button component `events/cotton/topic/vote_button.html`
- [x] T079 [US3] Integrate vote button in topic card component (redirects to login for non-authenticated users via `@require_authentication` decorator)
- [ ] T080 [US3] Update get_topics_for_event function to include user vote status in TopicDTO
- [ ] T081 [US3] Update get_event_topics function to pass user context for vote status

**Checkpoint**: At this point, User Stories 1 AND 3 should work independently. Users can view topics and vote on them (output-first approach).

---

## Phase 5: User Story 6 - Readonly Experience for Non-Authenticated Users (Priority: P2)

**Goal**: Non-authenticated users can view all content in readonly mode. Interactive buttons redirect to login page (HTMX redirect for HTMX requests, standard redirect for regular requests).

**Independent Test**: A non-authenticated user can view topics, comments, and presenter suggestions. Clicking vote/comment/add buttons redirects to login page.

### Tests for User Story 6 (TDD - Write First)

- [x] T082 [P] [US6] Integration test for non-authenticated user viewing topics in `tests/integration/events/test_readonly_experience.py`
- [x] T083 [P] [US6] Integration test for authentication redirects in `tests/integration/accounts/test_signin_popup.py` (renamed from test_signin_popup)

### Implementation for User Story 6

- [x] T084 [US6] ~~Enhance sign-in popup component~~ (REMOVED: Replaced with redirect approach)
- [x] T085 [US6] ~~Create SSO authentication views~~ (Already implemented via django-allauth)
- [x] T086 [US6] ~~Add URL patterns for SSO~~ (Already implemented via django-allauth)
- [x] T087 [US6] Create `@require_authentication` decorator in `core/decorators.py` that handles both HTMX and regular redirects
- [x] T088 [US6] Apply `@require_authentication` decorator to vote endpoint and update other interactive elements as they are implemented
- [x] T089 [US6] ~~Handle SSO authentication failures~~ (Already handled by django-allauth with error messages)

**Checkpoint**: At this point, non-authenticated users have full readonly experience with sign-in prompts.

---

## Phase 6: User Story 2 - Add, Edit, and Delete Topics (Priority: P2)

**Goal**: Logged-in users can create, edit, and delete their own topics. Editing occurs on dedicated pages (not modals) with seamless back button navigation.

**Independent Test**: A logged-in user can create a topic via form, see it appear in the list, edit it on a dedicated page, and delete it with confirmation modal.

**Output-First Rationale**: Following output-first approach, content creation is prioritized after viewing and voting functionality is available.

### Tests for User Story 2 (TDD - Write First)

- [ ] T090 [P] [US2] Unit test for create_topic function in `tests/unit/events/test_use_cases/test_create_topic.py`
- [ ] T091 [P] [US2] Unit test for edit_topic function in `tests/unit/events/test_use_cases/test_edit_topic.py`
- [ ] T092 [P] [US2] Unit test for delete_topic function in `tests/unit/events/test_use_cases/test_delete_topic.py`
- [ ] T093 [P] [US2] Unit test for create_topic service function in `tests/unit/events/test_services/test_topic_service.py`
- [ ] T094 [P] [US2] Unit test for slug generation uniqueness in `tests/unit/events/test_services/test_topic_service.py`
- [ ] T095 [P] [US2] Integration test for topic creation flow in `tests/integration/events/test_topic_creation.py`
- [ ] T096 [P] [US2] Integration test for topic edit flow in `tests/integration/events/test_topic_edit.py`
- [ ] T097 [P] [US2] Integration test for topic delete flow in `tests/integration/events/test_topic_delete.py`
- [ ] T097a [P] [US2] Integration test for browser back button navigation in edit pages (FR-032) in `tests/integration/events/test_browser_navigation.py`

### Implementation for User Story 2

- [ ] T098 [US2] Create TopicForm in `events/forms.py` for topic creation/editing with validation
- [ ] T099 [US2] Create create_topic function in `events/use_cases/create_topic.py` (validates, generates slug, creates topic, returns DTO)
- [ ] T100 [US2] Create edit_topic function in `events/use_cases/edit_topic.py` (validates ownership, updates topic, keeps slug immutable, returns DTO)
- [ ] T101 [US2] Create delete_topic function in `events/use_cases/delete_topic.py` (validates ownership, soft deletes topic)
- [ ] T102 [US2] Add create_topic function to `events/services/topic_service.py` (slug generation with uniqueness)
- [ ] T103 [US2] Add update_topic function to `events/services/topic_service.py`
- [ ] T104 [US2] Add soft_delete_topic function to `events/services/topic_service.py`
- [ ] T105 [US2] Create topic creation view in `events/views.py` for GET/POST `/topics/create/`
- [ ] T106 [US2] Create topic edit view in `events/views.py` for GET/POST `/topics/<slug>/edit/`
- [ ] T107 [US2] Create topic delete view in `events/views.py` for POST `/topics/<slug>/delete/` (HTMX, returns success response)
- [ ] T108 [US2] Add URL patterns in `events/urls.py` for create, edit, delete endpoints
- [ ] T109 [US2] Create topic form template `events/templates/events/topic_form.html` with HTML5 native validation and/or vanilla JS for character count (AlpineJS only if explicitly requested)
- [ ] T110 [US2] Create topic edit template `events/templates/events/topic_edit.html` with HTMX form submission
- [ ] T111 [US2] Create HTMX confirmation modal component for delete in `events/templates/events/partials/delete_confirm_modal.html` (HTMX-first: load dialog fragment from server, AlpineJS only if explicitly requested)
- [ ] T112 [US2] Integrate delete confirmation modal in topic detail/card (HTMX to load dialog fragment, AlpineJS only if explicitly requested)
- [ ] T113 [US2] Add "Add Topic" button/link in event detail template (redirects to login for non-authenticated users)
- [ ] T114 [US2] Add edit/delete buttons in topic card (only visible to topic creator)
- [ ] T115 [US2] Implement rate limiting for topic creation: 10 topics/hour per user in `core/middleware.py`

**Checkpoint**: At this point, User Stories 1, 3, 6, AND 2 should work independently. Users can view, vote on, and create topics.

---

## Phase 7: User Story 4 - Comment, Edit, and Delete Comments (Priority: P2)

**Goal**: Logged-in users can add, edit, and delete comments on topics. Comments display chronologically (oldest first). Editing on dedicated pages.

**Independent Test**: A logged-in user can add a comment, see it appear, edit it on a dedicated page, and delete it with confirmation.

### Tests for User Story 4 (TDD - Write First)

- [ ] T116 [P] [US4] Unit test for Comment model in `tests/unit/events/test_models.py`
- [ ] T117 [P] [US4] Unit test for CommentDTO with `assertNumQueries` from `pytest_django.asserts` in `tests/unit/events/test_dto/test_comment_dto.py`
- [ ] T118 [P] [US4] Unit test for add_comment service function in `tests/unit/events/test_services/test_comment_service.py`
- [ ] T119 [P] [US4] Unit test for add_comment function in `tests/unit/events/test_use_cases/test_add_comment.py`
- [ ] T120 [P] [US4] Unit test for edit_comment function in `tests/unit/events/test_use_cases/test_edit_comment.py`
- [ ] T121 [P] [US4] Unit test for delete_comment function in `tests/unit/events/test_use_cases/test_delete_comment.py`
- [ ] T122 [P] [US4] Integration test for comment flow in `tests/integration/events/test_comment_flow.py`
- [ ] T122a [P] [US4] Integration test for browser back button navigation in comment edit pages (FR-032) in `tests/integration/events/test_browser_navigation.py`

### Implementation for User Story 4

- [ ] T123 [US4] Create Comment model in `events/models.py` inheriting from `SoftDeleteModel` with topic FK, author FK, content
- [ ] T124 [US4] Create migration for Comment model: `events/migrations/0003_comment.py`
- [ ] T125 [US4] Create CommentDTO dataclass in `events/dto/comment_dto.py`
- [ ] T126 [US4] Create comment service functions in `events/services/comment_service.py`: add_comment, update_comment, soft_delete_comment
- [ ] T127 [US4] Create add_comment function in `events/use_cases/add_comment.py` (validates, creates comment, returns DTO)
- [ ] T128 [US4] Create edit_comment function in `events/use_cases/edit_comment.py` (validates ownership, updates comment, returns DTO)
- [ ] T129 [US4] Create delete_comment function in `events/use_cases/delete_comment.py` (validates ownership, soft deletes comment)
- [ ] T130 [US4] Create add comment HTMX view in `events/views.py` for POST `/topics/<slug>/comments/create/` (returns comment partial)
- [ ] T131 [US4] Create comment edit view in `events/views.py` for GET/POST `/topics/<slug>/comments/<id>/edit/`
- [ ] T132 [US4] Create comment delete view in `events/views.py` for POST `/topics/<slug>/comments/<id>/delete/` (HTMX)
- [ ] T133 [US4] Add URL patterns in `events/urls.py` for comment endpoints
- [ ] T134 [US4] Create comment item partial template `events/templates/events/partials/comment_item.html` for HTMX insertion
- [ ] T135 [US4] Create Django-Cotton comment item component `events/cotton/comment/item.html`
- [ ] T136 [US4] Create comment form template `events/templates/events/comment_form.html` with HTML5 native validation and/or vanilla JS for character count (AlpineJS only if explicitly requested)
- [ ] T137 [US4] Create comment edit template `events/templates/events/comment_edit.html` with HTMX form submission
- [ ] T138 [US4] Integrate comment form in topic detail template (redirects to login for non-authenticated users)
- [ ] T139 [US4] Update get_topic_detail function to include comments (ordered chronologically, oldest first)
- [ ] T140 [US4] Update TopicDetailDTO to include list of CommentDTOs
- [ ] T141 [US4] Implement rate limiting for comments: 20 comments/hour per user in `core/middleware.py`

**Checkpoint**: At this point, User Stories 1-4 should work independently. Users can view, manage, vote on, and comment on topics.

---

## Phase 8: User Story 7 - Switch Between Events (Priority: P2)

**Goal**: Users can switch between events using an event selector. Each event has slug-based URL. HTMX loads event content.

**Independent Test**: A user can access `/events/python-floripa/` and `/events/other-event/` and see topics specific to each event. Event selector allows switching.

### Tests for User Story 7 (TDD - Write First)

- [ ] T142 [P] [US7] Unit test for event selector use case in `tests/unit/events/test_use_cases/test_get_events.py`
- [ ] T143 [P] [US7] Integration test for event switching in `tests/integration/events/test_event_switching.py`

### Implementation for User Story 7

- [ ] T144 [US7] Create get_events function in `events/use_cases/get_events.py` (returns list of EventDTOs)
- [ ] T145 [US7] Create EventDTO dataclass in `events/dto/event_dto.py`
- [ ] T146 [US7] Create event selector view in `events/views.py` for GET `/events/` (returns event list)
- [ ] T147 [US7] Add URL pattern in `events/urls.py` for events list
- [ ] T148 [US7] Create HTMX event selector component in base template or navigation (HTMX-first: native HTML select with hx-get/hx-trigger, AlpineJS only if explicitly requested)
- [ ] T149 [US7] Create HTMX handler for event selection (loads event content without full page refresh)
- [ ] T150 [US7] Update navigation to include event selector (HTMX-first: native HTML select with hx-get/hx-trigger for content loading, AlpineJS only if explicitly requested)
- [ ] T151 [US7] Implement unsaved changes warning for event switching: detect unsaved form input (comment forms, topic forms) and show confirmation dialog before switching events (HTMX-first: load confirmation dialog fragment, AlpineJS only if explicitly requested)

**Checkpoint**: At this point, users can switch between events seamlessly.

---

## Phase 9: User Story 5 - Suggest, Edit, and Delete Presenters (Priority: P3)

**Goal**: Logged-in users can suggest presenters for topics (email, URL, or full name). Limited to 3 per user per topic, 10 total per topic. Users can edit and delete their own suggestions.

**Independent Test**: A logged-in user can suggest a presenter, see it displayed, edit it on a dedicated page, and delete it with confirmation. Limits are enforced.

### Tests for User Story 5 (TDD - Write First)

- [ ] T152 [P] [US5] Unit test for PresenterSuggestion model in `tests/unit/events/test_models.py`
- [ ] T153 [P] [US5] Unit test for PresenterDTO with `assertNumQueries` from `pytest_django.asserts` in `tests/unit/events/test_dto/test_presenter_dto.py`
- [ ] T154 [P] [US5] Unit test for suggest_presenter service function with limits in `tests/unit/events/test_services/test_presenter_service.py`
- [ ] T155 [P] [US5] Unit test for suggest_presenter function in `tests/unit/events/test_use_cases/test_suggest_presenter.py`
- [ ] T156 [P] [US5] Unit test for edit_presenter_suggestion function in `tests/unit/events/test_use_cases/test_edit_presenter_suggestion.py`
- [ ] T157 [P] [US5] Unit test for delete_presenter_suggestion function in `tests/unit/events/test_use_cases/test_delete_presenter_suggestion.py`
- [ ] T158 [P] [US5] Integration test for presenter suggestion flow in `tests/integration/events/test_presenter_suggestion_flow.py`
- [ ] T158a [P] [US5] Integration test for browser back button navigation in presenter suggestion edit pages (FR-032) in `tests/integration/events/test_browser_navigation.py`

### Implementation for User Story 5

- [ ] T159 [US5] Create PresenterSuggestion model in `events/models.py` inheriting from `SoftDeleteModel` with topic FK, suggested_by FK, presenter_contact CharField (can be email, name, LinkedIn URL, WhatsApp contact, etc.)
- [ ] T160 [US5] Create migration for PresenterSuggestion model: `events/migrations/0004_presenter_suggestion.py`
- [ ] T161 [US5] Create PresenterDTO dataclass in `events/dto/presenter_dto.py`
- [ ] T162 [US5] Create presenter service functions in `events/services/presenter_service.py`: suggest_presenter, update_suggestion, soft_delete_suggestion, check_limits
- [ ] T163 [US5] Create suggest_presenter function in `events/use_cases/suggest_presenter.py` (signature: `suggest_presenter(suggested_by, topic_slug, presenter_contact)`, validates limits: 3 per user, 10 per topic, creates suggestion, returns DTO)
- [ ] T164 [US5] Create edit_presenter_suggestion function in `events/use_cases/edit_presenter_suggestion.py` (validates ownership, updates suggestion, returns DTO)
- [ ] T165 [US5] Create delete_presenter_suggestion function in `events/use_cases/delete_presenter_suggestion.py` (validates ownership, soft deletes suggestion)
- [ ] T166 [US5] Create suggest presenter HTMX view in `events/views.py` for POST `/topics/<slug>/presenters/suggest/` (returns suggestion partial)
- [ ] T167 [US5] Create presenter suggestion edit view in `events/views.py` for GET/POST `/topics/<slug>/presenters/<id>/edit/`
- [ ] T168 [US5] Create presenter suggestion delete view in `events/views.py` for POST `/topics/<slug>/presenters/<id>/delete/` (HTMX)
- [ ] T169 [US5] Add URL patterns in `events/urls.py` for presenter suggestion endpoints
- [ ] T170 [US5] Create presenter suggestion partial template `events/templates/events/partials/presenter_suggestion_item.html`
- [ ] T171 [US5] Create Django-Cotton presenter suggestion component `events/cotton/presenter/suggestion.html`
- [ ] T172 [US5] Create presenter suggestion form template with HTML5 native validation (single `presenter_contact` field with UI guidance indicating it can be email, name, LinkedIn URL, WhatsApp contact, etc., AlpineJS only if explicitly requested)
- [ ] T173 [US5] Create presenter suggestion edit template `events/templates/events/presenter_suggestion_edit.html`
- [ ] T174 [US5] Integrate presenter suggestions in topic detail template (redirects to login for non-authenticated users)
- [ ] T175 [US5] Update get_topic_detail function to include presenter suggestions (ordered chronologically, oldest first)
- [ ] T176 [US5] Update TopicDetailDTO to include list of PresenterDTOs

**Checkpoint**: At this point, all user stories should be independently functional. Users can suggest presenters with proper limits.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T177 [P] Configure comprehensive Django admin for all models: Event, Topic, Vote, Comment, PresenterSuggestion in `events/admin.py`. Use inlines for 1:N relationships (TopicInline in EventAdmin, CommentInline and PresenterSuggestionInline in TopicAdmin). Configure list_display, list_filter, search_fields, fieldsets, readonly_fields, and prepopulated_fields for all models. Ensure complete system management through admin interface.
- [ ] T178 [P] Add comprehensive admin actions: bulk soft delete recovery, export functionality. Configure all_objects manager for soft-deleted models in admin to access deleted records.
- [ ] T179 [P] Implement proper error handling and user-friendly error messages across all views
- [ ] T180 [P] Add loading indicators using HTMX hx-indicator for all HTMX requests
- [ ] T181 [P] Optimize database queries: add composite indexes per data-model.md specifications
- [ ] T182 [P] Add comprehensive logging for all use cases and services
- [ ] T183 [P] Implement proper CSRF protection for all forms
- [ ] T184 [P] Add mobile-first responsive design improvements using Pure CSS
- [ ] T185 [P] Ensure WCAG 2.1 Level AA accessibility compliance across all templates
- [ ] T186 [P] Add proper meta tags and SEO optimization
- [ ] T187 [P] Create empty state templates for events with no topics
- [ ] T188 [P] Add proper timezone handling for all datetime displays (America/Sao_Paulo)
- [ ] T189 [P] Implement proper i18n strings for all user-facing text (Portuguese pt-BR)
- [ ] T190 [P] Add comprehensive integration tests for complete user journeys
- [ ] T191 [P] Run quickstart.md validation scenarios
- [ ] T192 [P] Performance testing: verify 1000+ topics per event without degradation
- [ ] T193 [P] Security audit: verify UUID v6 prevents ID enumeration, verify rate limiting works
- [ ] T194 [P] Documentation: Update README with setup instructions
- [ ] T195 [P] Documentation: Add API documentation for HTMX endpoints (contracts)

### Cross-Cutting Requirements (FR-037, FR-040-FR-044)

- [ ] T196 [P] Create rate limiting middleware in `core/middleware.py` for FR-037: implement 10 topics/hour and 20 comments/hour per user
- [ ] T197 [P] Create error message utility in `core/utils.py` for FR-040: function to generate inline error messages using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR)
- [ ] T198 [P] Update all form templates to use error message utility (FR-040): replace generic error displays with inline semantic HTML messages
- [ ] T199 [P] Add concurrent edit handling to edit_topic function in `events/use_cases/edit_topic.py` for FR-041: implement last-write-wins approach with optional warning if content changed
- [ ] T200 [P] Add concurrent edit handling to edit_comment function in `events/use_cases/edit_comment.py` for FR-041: implement last-write-wins approach
- [ ] T201 [P] Add concurrent edit handling to edit_presenter_suggestion function in `events/use_cases/edit_presenter_suggestion.py` for FR-041: implement last-write-wins approach
- [ ] T202 [P] Create HTMX error handling middleware in `core/middleware.py` for FR-042: catch network failures and return inline error messages with retry button using semantic HTML
- [ ] T203 [P] Update all HTMX views to handle network failures (FR-042): ensure error responses use inline semantic HTML messages with retry functionality
- [ ] T204 [P] Create session expiration handler in `accounts/middleware.py` for FR-043: redirect to login and preserve action context for automatic execution after authentication
- [ ] T205 [P] Update authentication views to support action preservation (FR-043): store intended action and execute after successful login
- [ ] T206 [P] Create number formatting utility in `core/utils.py` for FR-044: function to format numbers in Portuguese (pt-BR) conventions (e.g., "1.234 votos") without abbreviations
- [ ] T207 [P] Update TopicDTO and CommentDTO to use number formatting utility (FR-044): format vote counts (calculated from Vote records) and comment counts in pt-BR format

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies (Output-First Approach)

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 (needs Topic model) - **Output-first: voting prioritized over creation**
- **User Story 6 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 and US3 (needs viewing and voting functionality)
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs Event and Topic models) - **Content creation after viewing/voting**
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs Topic model)
- **User Story 7 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (needs Event model)
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (needs Topic model)

### Within Each User Story

- Tests (TDD) MUST be written and FAIL before implementation
- Models before services
- Services before use cases
- Use cases before views
- Views before templates
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (with coordination)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (with coordination for shared models)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: T025 - Unit test for Event model
Task: T026 - Unit test for Topic model
Task: T027 - Unit test for TopicDTO
Task: T028 - Unit test for get_topics_for_event function
Task: T029 - Unit test for get_event_topics function
Task: T030 - Integration test for event detail view

# Launch all models for User Story 1 together:
Task: T031 - Create Event model
Task: T032 - Create Topic model
Task: T033 - Create SoftDeleteManager

# Launch DTOs and services in parallel:
Task: T035 - Create TopicDTO
Task: T036 - Create get_topics_for_event function
```

---

## Implementation Strategy

### MVP First (Output-First: View and Vote)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (View and Browse Topics)
4. Complete Phase 4: User Story 3 (Vote and Un-vote) - **Output-first: users can engage with existing content**
5. **STOP and VALIDATE**: Test User Stories 1 and 3 independently
6. Deploy/demo if ready

### Incremental Delivery (Output-First Approach)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (View Topics) → Test independently → Deploy/Demo
3. Add User Story 3 (Vote) → Test independently → Deploy/Demo (MVP with engagement!)
4. Add User Story 6 (Readonly) → Test independently → Deploy/Demo
5. Add User Story 2 (Create Topics) → Test independently → Deploy/Demo (Content creation after viewing/voting)
6. Add User Story 4 (Comments) → Test independently → Deploy/Demo
7. Add User Story 7 (Switch Events) → Test independently → Deploy/Demo
8. Add User Story 5 (Presenters) → Test independently → Deploy/Demo
9. Polish phase → Final improvements
10. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP)
   - Developer B: User Story 2 (after US1 models ready)
   - Developer C: User Story 3 (after US1 models ready)
3. Stories complete and integrate independently

---

## Phase 8: Navigation Bar and Login Flow (US8)

**Purpose**: Add persistent top navigation bar and beautiful login/signup flow

**Independent Test**: A user can see a navigation bar at the top of all pages with FloripaTalks branding, Eventos link, and appropriate login/logout links. Admin users see an Admin link. The login/signup flow is beautiful with Google social login including logo.

- [ ] T208 [US8] Create navigation bar component in base template with FloripaTalks branding, Eventos link, and login/logout links: `templates/base.html` - add semantic `<nav>` with proper structure
- [ ] T209 [US8] Add admin link to navigation bar (only visible to users with admin rights): check `user.is_staff` or `user.is_superuser` in template
- [ ] T210 [US8] Make navigation bar SEO-friendly: use semantic HTML (`<nav>`, proper `<a>` links with href attributes), ensure all links are crawlable by search engines
- [ ] T211 [US8] Style navigation bar for mobile-first responsive design: ensure touch-friendly targets, proper spacing, hamburger menu if needed for mobile
- [ ] T212 [US8] Create beautiful login page template: `accounts/templates/accounts/login.html` - modern design with Google social login button including logo
- [ ] T213 [US8] Create beautiful signup page template: `accounts/templates/accounts/signup.html` - consistent with login page design
- [ ] T214 [US8] Style Google social login button with logo: use official Google branding guidelines, include Google logo, proper colors
- [ ] T215 [US8] Ensure login/logout flow is consistent with delightful UI design (Principle XVIII): friendly, approachable, visually appealing

---

## Summary

- **Total Tasks**: 215
- **Tasks per User Story** (Output-First Priority Order):
  - US1 (View Topics - P1): 24 tasks
  - US3 (Vote - P1): 12 tasks
  - US6 (Readonly - P2): 6 tasks
  - US2 (Manage Topics - P2): 26 tasks
  - US4 (Comments - P2): 26 tasks
  - US7 (Event Switch - P2): 10 tasks
  - US5 (Presenters - P3): 25 tasks
  - US8 (Navigation & Login - P1): 8 tasks
  - Setup: 25 tasks
  - Foundational: 14 tasks
  - Polish: 19 tasks
  - Cross-Cutting Requirements: 20 tasks (FR-037, FR-040-FR-048)

- **Parallel Opportunities**: Many tasks marked [P] can run in parallel
- **Independent Test Criteria**: Each user story has clear independent test criteria
- **Suggested MVP Scope (Output-First)**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US3) = 73 tasks
  - Users can view topics and vote on them (output-first approach)
  - Content creation (US2) comes after viewing/voting functionality
- **Format Validation**: ✅ All tasks follow checklist format with Task ID, [P] markers, [Story] labels, and file paths

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All templates receive DTOs (not QuerySets) to prevent N+1 queries
- All DTO tests must include `assertNumQueries` from `pytest_django.asserts` (pytest-django provides this without requiring TestCase inheritance)
- AlpineJS optional (only when explicitly requested), HTMX prioritized for all interactions
- Custom user model MUST be created before first migration
- **Create GitHub issue ONLY for the task currently being worked on** (not in advance for entire phases)
- **Branch names MUST follow pattern: `{issue-id}-{description-in-slug-format}`** (e.g., `029-custom-user-model`)
- This prevents issues from becoming outdated when tasks are reordered or changed
