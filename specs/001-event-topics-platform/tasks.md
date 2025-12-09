# Tasks: Event Topics Platform

**Input**: Design documents from `/specs/001-event-topics-platform/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: TDD is required per constitution - all tests must be written before implementation code.

**GitHub Issues**: All tasks MUST have corresponding GitHub issues before work begins. Branch names MUST follow pattern: `{issue-id}-{description-in-slug-format}` (e.g., `123-view-topics-list`).

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

- [x] T001 Initialize Python project with `uv`: create `pyproject.toml` with Python 3.12+ requirement
- [x] T002 [P] Add Django to project using `uv add django` (adds to `pyproject.toml` and installs)
- [x] T003 [P] Add django-allauth using `uv add django-allauth` for SSO authentication
- [x] T004 [P] Add django-cotton using `uv add django-cotton` for component-based UI
- [x] T005 [P] Add django-htmx using `uv add django-htmx` for Django HTMX integration helpers
- [x] T006 [P] Add pytest and pytest-django using `uv add pytest pytest-django` for testing
- [x] T007 [P] Run `uv sync` to install all dependencies and generate `uv.lock` file
- [ ] T008 Create Django project structure: run `django-admin startproject floripatalks` to create project root with `manage.py`

### Django Apps and Structure

- [ ] T009 [P] Create Django app `events`: run `python manage.py startapp events` in project root
- [ ] T010 [P] Create Django app `accounts`: run `python manage.py startapp accounts` in project root
- [ ] T011 [P] Create Django app `core`: run `python manage.py startapp core` in project root
- [ ] T012 [P] Setup Django settings structure: create `floripatalks/settings/` directory with `__init__.py`, `base.py`, `development.py`, `production.py`
- [ ] T013 [P] Configure `floripatalks/urls.py` with app routing: include `events.urls`, `accounts.urls`
- [ ] T014 [P] Create `tests/` directory structure: `tests/unit/`, `tests/integration/`, `tests/conftest.py` with `__init__.py` files

### Static Files and Assets

- [ ] T015 [P] Setup static files configuration in `floripatalks/settings/base.py`: `STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`
- [ ] T016 [P] Create static files directories: `static/js/`, `static/css/pure-css/`
- [ ] T017 [P] Download HTMX latest version to `static/js/htmx.min.js` (from https://htmx.org/)
- [ ] T018 [P] Download AlpineJS latest version to `static/js/alpine.min.js` (from https://alpinejs.dev/)
- [ ] T019 [P] Download Pure CSS latest version to `static/css/pure-css/pure-min.css` (from https://purecss.io/)

### Development Tools

- [ ] T020 [P] Create `justfile` with common tasks: `just test` (run pytest), `just dev` (runserver), `just migrate`, `just lint`, `just format`
- [ ] T021 [P] Create `.gitignore` for Python/Django project (include `.venv/`, `.uv/`, `uv.lock`, `db.sqlite3`, `__pycache__/`, etc.)

### Pre-commit Hooks

- [ ] T022 [P] Install prek or rustyhook: `cargo install prek` or `cargo install rustyhook` (Rust-based pre-commit runner)
- [ ] T023 [P] Create `.pre-commit-config.yaml` with hooks: ruff (formatting/linting), mypy (type checking), security scanning
- [ ] T024 [P] Initialize pre-commit: run `prek install` or `rustyhook install` to setup git hooks

### GitHub Actions CI/CD

- [ ] T025 [P] Create `.github/workflows/ci.yml` with workflow to:
  - Run on push and pull requests
  - Setup Python 3.12+ with uv
  - Install dependencies with `uv sync`
  - Run tests with `pytest` via `just test`
  - Run linting/formatting checks
  - Fail build if any check fails

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T026 Create custom User model in `accounts/models.py` inheriting from `AbstractUser` with UUID v7 primary key
- [ ] T027 [P] Create User migration: `accounts/migrations/0001_initial.py` (MUST be first migration)
- [ ] T028 [P] Configure django-allauth for Google and LinkedIn SSO in `floripatalks/settings/base.py`
- [ ] T029 [P] Setup database configuration: PostgreSQL (production), SQLite (development) in `floripatalks/settings/base.py`
- [ ] T030 [P] Configure django-htmx in `floripatalks/settings/base.py`: add `django_htmx` to `INSTALLED_APPS`
- [ ] T031 [P] Configure django-cotton in `floripatalks/settings/base.py`: add `cotton` to `INSTALLED_APPS`
- [ ] T032 [P] Create base templates directory: `templates/base.html` with HTMX and AlpineJS includes
- [ ] T033 [P] Create `core/middleware.py` for rate limiting middleware structure
- [ ] T034 [P] Setup i18n configuration: Portuguese (pt-BR) as primary language, timezone America/Sao_Paulo in `floripatalks/settings/base.py`
- [ ] T035 [P] Create `core/utils.py` for shared utilities
- [ ] T036 [P] Configure Django admin in `accounts/admin.py` for User model
- [ ] T037 [P] Create base Django-Cotton component structure: `events/cotton/`, `accounts/cotton/` directories
- [ ] T038 [P] Setup pytest configuration: `pytest.ini` or `pyproject.toml` pytest section with Django settings
- [ ] T039 [P] Create test fixtures in `tests/conftest.py`: user fixtures, event fixtures

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Browse Topics (Priority: P1) 🎯 MVP - Output-First

**Goal**: Users (logged in or not) can view a list of topics for an event, see vote counts and comment counts, browse with infinite scroll. Non-authenticated users see sign-in popups when clicking interactive elements.

**Independent Test**: A user (logged in or not) can navigate to `/events/python-floripa/` and see a list of topics with vote counts and comment counts displayed. Topics load in batches of 20 via infinite scroll. Non-authenticated users see interactive buttons but receive sign-in prompts when clicking them.

**Output-First Rationale**: This is the foundation - users must be able to see existing content before they can interact with it or create new content.

### Tests for User Story 1 (TDD - Write First)

- [ ] T040 [P] [US1] Unit test for Event model in `tests/unit/events/test_models.py`
- [ ] T041 [P] [US1] Unit test for Topic model in `tests/unit/events/test_models.py`
- [ ] T042 [P] [US1] Unit test for TopicDTO with `assertNumQueries` in `tests/unit/events/test_dto/test_topic_dto.py`
- [ ] T043 [P] [US1] Unit test for TopicService.get_topics_for_event in `tests/unit/events/test_services/test_topic_service.py`
- [ ] T044 [P] [US1] Unit test for GetEventTopicsUseCase in `tests/unit/events/test_use_cases/test_get_event_topics.py`
- [ ] T045 [P] [US1] Integration test for event detail view in `tests/integration/events/test_event_detail_view.py`

### Implementation for User Story 1

- [ ] T046 [P] [US1] Create Event model in `events/models.py` with UUID v7, slug, name, description
- [ ] T047 [P] [US1] Create Topic model in `events/models.py` with UUID v7, slug (auto-generated), title, description, vote_count, is_deleted, event FK, creator FK
- [ ] T048 [P] [US1] Create SoftDeleteManager in `events/managers.py` with is_deleted filtering
- [ ] T049 [US1] Create migrations for Event and Topic models: `events/migrations/0001_initial.py`
- [ ] T050 [P] [US1] Create TopicDTO dataclass in `events/dto/topic_dto.py`
- [ ] T051 [P] [US1] Create TopicService in `events/services/topic_service.py` with get_topics_for_event method (prefetch, select_related, convert to DTOs)
- [ ] T052 [US1] Create GetEventTopicsUseCase in `events/use_cases/get_event_topics.py` (calls TopicService, returns DTOs)
- [ ] T053 [US1] Create event detail view in `events/views.py` for GET `/events/<slug>/` (calls use case, passes DTOs to template)
- [ ] T054 [US1] Create HTMX view for infinite scroll in `events/views.py` for GET `/events/<slug>/topics/load-more/` (returns partial fragment)
- [ ] T055 [US1] Create URL patterns in `events/urls.py` for event detail and load-more endpoints
- [ ] T056 [US1] Create base template `templates/base.html` with HTMX, AlpineJS, Pure CSS includes
- [ ] T057 [US1] Create event detail template `events/templates/events/event_detail.html` with topics list
- [ ] T058 [US1] Create topic list partial template `events/templates/events/partials/topic_list_fragment.html` for HTMX infinite scroll
- [ ] T059 [US1] Create Django-Cotton topic card component `events/cotton/topic/card.html`
- [ ] T060 [US1] Create AlpineJS sign-in popup component `accounts/templates/accounts/login_popup.html` with x-show toggle
- [ ] T061 [US1] Integrate sign-in popup in event detail template (AlpineJS triggers on interactive button clicks)
- [ ] T062 [US1] Configure admin for Event and Topic models in `events/admin.py`
- [ ] T063 [US1] Create initial Event (Python Floripa) via Django admin or data migration

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can view topics list with infinite scroll.

---

## Phase 4: User Story 3 - Vote and Un-vote on Topics (Priority: P1) 🎯 Output-First

**Goal**: Logged-in users can vote on topics they want to see as talks. Each user can vote once per topic and can later un-vote (remove their vote). The vote count is displayed and updates in real-time when users vote or un-vote.

**Independent Test**: A logged-in user can click vote button, see count increment, then un-vote and see count decrement. Vote button state reflects user's vote status.

**Output-First Rationale**: Voting allows users to immediately engage with existing content. This is prioritized over creating new content (output-first approach).

### Tests for User Story 3 (TDD - Write First)

- [ ] T064 [P] [US3] Unit test for Vote model in `tests/unit/events/test_models.py`
- [ ] T065 [P] [US3] Unit test for VoteService.vote_topic in `tests/unit/events/test_services/test_vote_service.py`
- [ ] T066 [P] [US3] Unit test for VoteService.unvote_topic in `tests/unit/events/test_services/test_vote_service.py`
- [ ] T067 [P] [US3] Unit test for VoteTopicUseCase in `tests/unit/events/test_use_cases/test_vote_topic.py`
- [ ] T068 [P] [US3] Unit test for UnvoteTopicUseCase in `tests/unit/events/test_use_cases/test_unvote_topic.py`
- [ ] T069 [P] [US3] Integration test for vote/unvote flow in `tests/integration/events/test_vote_flow.py`

### Implementation for User Story 3

- [ ] T070 [US3] Create Vote model in `events/models.py` with UUID v7, topic FK, user FK, unique constraint (topic, user)
- [ ] T071 [US3] Create migration for Vote model: `events/migrations/0002_vote.py`
- [ ] T072 [US3] Create VoteService in `events/services/vote_service.py` with vote_topic, unvote_topic, get_user_vote_status methods
- [ ] T073 [US3] Create VoteTopicUseCase in `events/use_cases/vote_topic.py` (validates, creates vote, updates vote_count, returns status DTO)
- [ ] T074 [US3] Create UnvoteTopicUseCase in `events/use_cases/unvote_topic.py` (validates, removes vote, updates vote_count, returns status DTO)
- [ ] T075 [US3] Create vote/unvote HTMX view in `events/views.py` for POST `/topics/<slug>/vote/` (toggles vote/unvote)
- [ ] T076 [US3] Add URL pattern in `events/urls.py` for vote endpoint
- [ ] T077 [US3] Create vote button partial template `events/templates/events/partials/vote_button.html` with HTMX attributes
- [ ] T078 [US3] Create Django-Cotton vote button component `events/cotton/topic/vote_button.html`
- [ ] T079 [US3] Integrate vote button in topic card component (shows sign-in popup for non-authenticated users)
- [ ] T080 [US3] Update TopicService to include user vote status in TopicDTO
- [ ] T081 [US3] Update GetEventTopicsUseCase to pass user context for vote status

**Checkpoint**: At this point, User Stories 1 AND 3 should work independently. Users can view topics and vote on them (output-first approach).

---

## Phase 5: User Story 6 - Readonly Experience for Non-Authenticated Users (Priority: P2)

**Goal**: Non-authenticated users can view all content in readonly mode. Interactive buttons trigger AlpineJS sign-in popup.

**Independent Test**: A non-authenticated user can view topics, comments, and presenter suggestions. Clicking vote/comment/add buttons shows sign-in popup.

### Tests for User Story 6 (TDD - Write First)

- [ ] T082 [P] [US6] Integration test for non-authenticated user viewing topics in `tests/integration/events/test_readonly_experience.py`
- [ ] T083 [P] [US6] Integration test for sign-in popup triggers in `tests/integration/accounts/test_signin_popup.py`

### Implementation for User Story 6

- [ ] T084 [US6] Enhance sign-in popup component `accounts/templates/accounts/login_popup.html` with Google and LinkedIn SSO buttons
- [ ] T085 [US6] Create SSO authentication views in `accounts/views.py` for Google and LinkedIn OAuth flows
- [ ] T086 [US6] Add URL patterns in `accounts/urls.py` for SSO authentication endpoints
- [ ] T087 [US6] Integrate sign-in popup triggers in all interactive elements: vote buttons, comment forms, add topic buttons, suggest presenter buttons
- [ ] T088 [US6] Update templates to show interactive buttons for non-authenticated users (with AlpineJS click handlers)
- [ ] T089 [US6] Handle SSO authentication failures with user-friendly error messages and retry options

**Checkpoint**: At this point, non-authenticated users have full readonly experience with sign-in prompts.

---

## Phase 6: User Story 2 - Add, Edit, and Delete Topics (Priority: P2)

**Goal**: Logged-in users can create, edit, and delete their own topics. Editing occurs on dedicated pages (not modals) with seamless back button navigation.

**Independent Test**: A logged-in user can create a topic via form, see it appear in the list, edit it on a dedicated page, and delete it with confirmation modal.

**Output-First Rationale**: Following output-first approach, content creation is prioritized after viewing and voting functionality is available.

### Tests for User Story 2 (TDD - Write First)

- [ ] T090 [P] [US2] Unit test for CreateTopicUseCase in `tests/unit/events/test_use_cases/test_create_topic.py`
- [ ] T091 [P] [US2] Unit test for EditTopicUseCase in `tests/unit/events/test_use_cases/test_edit_topic.py`
- [ ] T092 [P] [US2] Unit test for DeleteTopicUseCase in `tests/unit/events/test_use_cases/test_delete_topic.py`
- [ ] T093 [P] [US2] Unit test for TopicService.create_topic in `tests/unit/events/test_services/test_topic_service.py`
- [ ] T094 [P] [US2] Unit test for slug generation uniqueness in `tests/unit/events/test_services/test_topic_service.py`
- [ ] T095 [P] [US2] Integration test for topic creation flow in `tests/integration/events/test_topic_creation.py`
- [ ] T096 [P] [US2] Integration test for topic edit flow in `tests/integration/events/test_topic_edit.py`
- [ ] T097 [P] [US2] Integration test for topic delete flow in `tests/integration/events/test_topic_delete.py`

### Implementation for User Story 2

- [ ] T098 [US2] Create TopicForm in `events/forms.py` for topic creation/editing with validation
- [ ] T099 [US2] Create CreateTopicUseCase in `events/use_cases/create_topic.py` (validates, generates slug, creates topic, returns DTO)
- [ ] T100 [US2] Create EditTopicUseCase in `events/use_cases/edit_topic.py` (validates ownership, updates topic, keeps slug immutable, returns DTO)
- [ ] T101 [US2] Create DeleteTopicUseCase in `events/use_cases/delete_topic.py` (validates ownership, soft deletes topic)
- [ ] T102 [US2] Add create_topic method to TopicService in `events/services/topic_service.py` (slug generation with uniqueness)
- [ ] T103 [US2] Add update_topic method to TopicService in `events/services/topic_service.py`
- [ ] T104 [US2] Add soft_delete_topic method to TopicService in `events/services/topic_service.py`
- [ ] T105 [US2] Create topic creation view in `events/views.py` for GET/POST `/topics/create/`
- [ ] T106 [US2] Create topic edit view in `events/views.py` for GET/POST `/topics/<slug>/edit/`
- [ ] T107 [US2] Create topic delete view in `events/views.py` for POST `/topics/<slug>/delete/` (HTMX, returns success response)
- [ ] T108 [US2] Add URL patterns in `events/urls.py` for create, edit, delete endpoints
- [ ] T109 [US2] Create topic form template `events/templates/events/topic_form.html` with AlpineJS character count validation
- [ ] T110 [US2] Create topic edit template `events/templates/events/topic_edit.html` with HTMX form submission
- [ ] T111 [US2] Create AlpineJS confirmation modal component for delete in `events/templates/events/partials/delete_confirm_modal.html`
- [ ] T112 [US2] Integrate delete confirmation modal in topic detail/card (AlpineJS toggle, HTMX for delete action)
- [ ] T113 [US2] Add "Add Topic" button/link in event detail template (shows sign-in popup for non-authenticated users)
- [ ] T114 [US2] Add edit/delete buttons in topic card (only visible to topic creator)
- [ ] T115 [US2] Implement rate limiting for topic creation: 10 topics/hour per user in `core/middleware.py`

**Checkpoint**: At this point, User Stories 1, 3, 6, AND 2 should work independently. Users can view, vote on, and create topics.

---

## Phase 7: User Story 4 - Comment, Edit, and Delete Comments (Priority: P2)

**Goal**: Logged-in users can add, edit, and delete comments on topics. Comments display chronologically (oldest first). Editing on dedicated pages.

**Independent Test**: A logged-in user can add a comment, see it appear, edit it on a dedicated page, and delete it with confirmation.

### Tests for User Story 4 (TDD - Write First)

- [ ] T116 [P] [US4] Unit test for Comment model in `tests/unit/events/test_models.py`
- [ ] T117 [P] [US4] Unit test for CommentDTO with `assertNumQueries` in `tests/unit/events/test_dto/test_comment_dto.py`
- [ ] T118 [P] [US4] Unit test for CommentService.add_comment in `tests/unit/events/test_services/test_comment_service.py`
- [ ] T119 [P] [US4] Unit test for AddCommentUseCase in `tests/unit/events/test_use_cases/test_add_comment.py`
- [ ] T120 [P] [US4] Unit test for EditCommentUseCase in `tests/unit/events/test_use_cases/test_edit_comment.py`
- [ ] T121 [P] [US4] Unit test for DeleteCommentUseCase in `tests/unit/events/test_use_cases/test_delete_comment.py`
- [ ] T122 [P] [US4] Integration test for comment flow in `tests/integration/events/test_comment_flow.py`

### Implementation for User Story 4

- [ ] T123 [US4] Create Comment model in `events/models.py` with UUID v7, topic FK, author FK, content, is_deleted, timestamps
- [ ] T124 [US4] Create migration for Comment model: `events/migrations/0003_comment.py`
- [ ] T125 [US4] Create CommentDTO dataclass in `events/dto/comment_dto.py`
- [ ] T126 [US4] Create CommentService in `events/services/comment_service.py` with add_comment, update_comment, soft_delete_comment methods
- [ ] T127 [US4] Create AddCommentUseCase in `events/use_cases/add_comment.py` (validates, creates comment, returns DTO)
- [ ] T128 [US4] Create EditCommentUseCase in `events/use_cases/edit_comment.py` (validates ownership, updates comment, returns DTO)
- [ ] T129 [US4] Create DeleteCommentUseCase in `events/use_cases/delete_comment.py` (validates ownership, soft deletes comment)
- [ ] T130 [US4] Create add comment HTMX view in `events/views.py` for POST `/topics/<slug>/comments/create/` (returns comment partial)
- [ ] T131 [US4] Create comment edit view in `events/views.py` for GET/POST `/topics/<slug>/comments/<id>/edit/`
- [ ] T132 [US4] Create comment delete view in `events/views.py` for POST `/topics/<slug>/comments/<id>/delete/` (HTMX)
- [ ] T133 [US4] Add URL patterns in `events/urls.py` for comment endpoints
- [ ] T134 [US4] Create comment item partial template `events/templates/events/partials/comment_item.html` for HTMX insertion
- [ ] T135 [US4] Create Django-Cotton comment item component `events/cotton/comment/item.html`
- [ ] T136 [US4] Create comment form template `events/templates/events/comment_form.html` with AlpineJS character count
- [ ] T137 [US4] Create comment edit template `events/templates/events/comment_edit.html` with HTMX form submission
- [ ] T138 [US4] Integrate comment form in topic detail template (shows sign-in popup for non-authenticated users)
- [ ] T139 [US4] Update GetTopicDetailUseCase to include comments (ordered chronologically, oldest first)
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

- [ ] T144 [US7] Create GetEventsUseCase in `events/use_cases/get_events.py` (returns list of EventDTOs)
- [ ] T145 [US7] Create EventDTO dataclass in `events/dto/event_dto.py`
- [ ] T146 [US7] Create event selector view in `events/views.py` for GET `/events/` (returns event list)
- [ ] T147 [US7] Add URL pattern in `events/urls.py` for events list
- [ ] T148 [US7] Create AlpineJS event selector dropdown component in base template or navigation
- [ ] T149 [US7] Create HTMX handler for event selection (loads event content without full page refresh)
- [ ] T150 [US7] Update navigation to include event selector (AlpineJS for dropdown, HTMX for content loading)

**Checkpoint**: At this point, users can switch between events seamlessly.

---

## Phase 9: User Story 5 - Suggest, Edit, and Delete Presenters (Priority: P3)

**Goal**: Logged-in users can suggest presenters for topics (email, URL, or full name). Limited to 3 per user per topic, 10 total per topic. Users can edit and delete their own suggestions.

**Independent Test**: A logged-in user can suggest a presenter, see it displayed, edit it on a dedicated page, and delete it with confirmation. Limits are enforced.

### Tests for User Story 5 (TDD - Write First)

- [ ] T151 [P] [US5] Unit test for PresenterSuggestion model in `tests/unit/events/test_models.py`
- [ ] T152 [P] [US5] Unit test for PresenterDTO with `assertNumQueries` in `tests/unit/events/test_dto/test_presenter_dto.py`
- [ ] T153 [P] [US5] Unit test for PresenterService.suggest_presenter with limits in `tests/unit/events/test_services/test_presenter_service.py`
- [ ] T154 [P] [US5] Unit test for SuggestPresenterUseCase in `tests/unit/events/test_use_cases/test_suggest_presenter.py`
- [ ] T155 [P] [US5] Unit test for EditPresenterSuggestionUseCase in `tests/unit/events/test_use_cases/test_edit_presenter_suggestion.py`
- [ ] T156 [P] [US5] Unit test for DeletePresenterSuggestionUseCase in `tests/unit/events/test_use_cases/test_delete_presenter_suggestion.py`
- [ ] T157 [P] [US5] Integration test for presenter suggestion flow in `tests/integration/events/test_presenter_suggestion_flow.py`

### Implementation for User Story 5

- [ ] T158 [US5] Create PresenterSuggestion model in `events/models.py` with UUID v7, topic FK, suggester FK, email, url, full_name, is_deleted, timestamps
- [ ] T159 [US5] Create migration for PresenterSuggestion model: `events/migrations/0004_presenter_suggestion.py`
- [ ] T160 [US5] Create PresenterDTO dataclass in `events/dto/presenter_dto.py`
- [ ] T161 [US5] Create PresenterService in `events/services/presenter_service.py` with suggest_presenter, update_suggestion, soft_delete_suggestion, check_limits methods
- [ ] T162 [US5] Create SuggestPresenterUseCase in `events/use_cases/suggest_presenter.py` (validates limits: 3 per user, 10 per topic, creates suggestion, returns DTO)
- [ ] T163 [US5] Create EditPresenterSuggestionUseCase in `events/use_cases/edit_presenter_suggestion.py` (validates ownership, updates suggestion, returns DTO)
- [ ] T164 [US5] Create DeletePresenterSuggestionUseCase in `events/use_cases/delete_presenter_suggestion.py` (validates ownership, soft deletes suggestion)
- [ ] T165 [US5] Create suggest presenter HTMX view in `events/views.py` for POST `/topics/<slug>/presenters/suggest/` (returns suggestion partial)
- [ ] T166 [US5] Create presenter suggestion edit view in `events/views.py` for GET/POST `/topics/<slug>/presenters/<id>/edit/`
- [ ] T167 [US5] Create presenter suggestion delete view in `events/views.py` for POST `/topics/<slug>/presenters/<id>/delete/` (HTMX)
- [ ] T168 [US5] Add URL patterns in `events/urls.py` for presenter suggestion endpoints
- [ ] T169 [US5] Create presenter suggestion partial template `events/templates/events/partials/presenter_suggestion_item.html`
- [ ] T170 [US5] Create Django-Cotton presenter suggestion component `events/cotton/presenter/suggestion.html`
- [ ] T171 [US5] Create presenter suggestion form template with AlpineJS validation
- [ ] T172 [US5] Create presenter suggestion edit template `events/templates/events/presenter_suggestion_edit.html`
- [ ] T173 [US5] Integrate presenter suggestions in topic detail template (shows sign-in popup for non-authenticated users)
- [ ] T174 [US5] Update GetTopicDetailUseCase to include presenter suggestions (ordered chronologically, oldest first)
- [ ] T175 [US5] Update TopicDetailDTO to include list of PresenterDTOs

**Checkpoint**: At this point, all user stories should be independently functional. Users can suggest presenters with proper limits.

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T176 [P] Configure Django admin for all models: Event, Topic, Vote, Comment, PresenterSuggestion in `events/admin.py`
- [ ] T177 [P] Add comprehensive admin actions: bulk soft delete recovery, export functionality
- [ ] T178 [P] Implement proper error handling and user-friendly error messages across all views
- [ ] T179 [P] Add loading indicators using HTMX hx-indicator for all HTMX requests
- [ ] T180 [P] Optimize database queries: add composite indexes per data-model.md specifications
- [ ] T181 [P] Add comprehensive logging for all use cases and services
- [ ] T182 [P] Implement proper CSRF protection for all forms
- [ ] T183 [P] Add mobile-first responsive design improvements using Pure CSS
- [ ] T184 [P] Ensure WCAG 2.1 Level AA accessibility compliance across all templates
- [ ] T185 [P] Add proper meta tags and SEO optimization
- [ ] T186 [P] Create empty state templates for events with no topics
- [ ] T187 [P] Add proper timezone handling for all datetime displays (America/Sao_Paulo)
- [ ] T188 [P] Implement proper i18n strings for all user-facing text (Portuguese pt-BR)
- [ ] T189 [P] Add comprehensive integration tests for complete user journeys
- [ ] T190 [P] Run quickstart.md validation scenarios
- [ ] T191 [P] Performance testing: verify 1000+ topics per event without degradation
- [ ] T192 [P] Security audit: verify UUID v7 prevents ID enumeration, verify rate limiting works
- [ ] T193 [P] Documentation: Update README with setup instructions
- [ ] T194 [P] Documentation: Add API documentation for HTMX endpoints (contracts)

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
Task: T028 - Unit test for TopicService
Task: T029 - Unit test for GetEventTopicsUseCase
Task: T030 - Integration test for event detail view

# Launch all models for User Story 1 together:
Task: T031 - Create Event model
Task: T032 - Create Topic model
Task: T033 - Create SoftDeleteManager

# Launch DTOs and services in parallel:
Task: T035 - Create TopicDTO
Task: T036 - Create TopicService
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

## Summary

- **Total Tasks**: 194
- **Tasks per User Story** (Output-First Priority Order):
  - US1 (View Topics - P1): 24 tasks
  - US3 (Vote - P1): 12 tasks
  - US6 (Readonly - P2): 6 tasks
  - US2 (Manage Topics - P2): 26 tasks
  - US4 (Comments - P2): 26 tasks
  - US7 (Event Switch - P2): 9 tasks
  - US5 (Presenters - P3): 25 tasks
  - Setup: 25 tasks
  - Foundational: 14 tasks
  - Polish: 19 tasks

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
- All DTO tests must include `assertNumQueries`
- AlpineJS for client-side state, HTMX for server interactions
- Custom user model MUST be created before first migration
- **All tasks MUST have GitHub issues before work begins**
- **Branch names MUST follow pattern: `{issue-id}-{description-in-slug-format}`** (e.g., `123-view-topics-list`)

