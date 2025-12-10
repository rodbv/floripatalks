# Implementation Plan: Event Topics Platform

**Branch**: `001-event-topics-platform` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-event-topics-platform/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

FloripaTalks is a mobile-first web application for managing talk topics for local events. Users can view, vote on, comment on, and suggest topics for future events. The system supports multiple events with slug-based URLs, SSO authentication (Google/LinkedIn), and a readonly experience for non-authenticated users. Built with Django, HTMX (for server-driven interactions), AlpineJS (for client-side state management), and Django-Cotton following TDD principles with a use case layer architecture.

## Technical Context

**Language/Version**: Python 3.12+ (with type annotations)  
**Primary Dependencies**: Django, django-allauth (SSO), HTMX, AlpineJS, django-cotton, pytest, pytest-django  
**Storage**: SQLite for all environments (development and production)  
**Testing**: pytest with pytest-django, following test pyramid (majority unit tests, fewer integration tests)  
**Code Quality**: Type annotations required, ruff for linting/formatting (line length 100)  
**Target Platform**: Web application (mobile-first, responsive design)  
**Project Type**: Web application (Django backend with server-rendered HTML + HTMX + AlpineJS)  
**Performance Goals**:
- Event pages load in <2 seconds on mobile
- Support 1000+ topics per event without degradation
- Topic creation completes in <30 seconds on mobile
- Event switching in <2 seconds

**Constraints**:
- Mobile-first design (320px-768px width support)
- WCAG 2.1 Level AA accessibility compliance
- No REST API (HTMX hypermedia pattern only)
- All templates receive DTOs (not QuerySets) to prevent N+1 queries
- Business logic in use case layer (not models)
- AlpineJS optional (only when explicitly requested), HTMX prioritized for all interactions

**Scale/Scope**:
- Initial: Single event (Python Floripa)
- Architecture supports multiple events from launch
- Target: 1000+ topics per event, multiple concurrent users
- Primary language: Portuguese (pt-BR), timezone: America/Sao_Paulo

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Test-Driven Development (TDD)
- **Status**: COMPLIANT
- **Verification**: All features will be developed using TDD (Red-Green-Refactor cycle)
- **Enforcement**: Tests written before implementation code

### ✅ II. Django Framework
- **Status**: COMPLIANT
- **Verification**: Using Django with app-based architecture, custom user model (AbstractUser), Django ORM
- **Custom User Model**: Required - will be implemented before first migration

### ✅ III. pytest Testing Framework and Test Pyramid
- **Status**: COMPLIANT
- **Verification**: pytest with pytest-django, test pyramid (majority unit tests for use cases/services, fewer integration tests)
- **DTO Tests**: All DTO tests will include `assertNumQueries`

### ✅ IV. HTMX Hypermedia Pattern
- **Status**: COMPLIANT
- **Verification**: HTMX for all dynamic interactions, HTML responses with partial fragments (no REST API)
- **Pattern**: Full pages for initial loads, partial fragments for HTMX requests
- **AlpineJS**: Used for client-side state management when server communication is not needed

### ✅ V. Component-Based UI with Django-Cotton
- **Status**: COMPLIANT
- **Verification**: Components in `cotton/` directories within Django apps, kebab-case naming

### ✅ VI. uv Dependency Management
- **Status**: COMPLIANT
- **Verification**: Using uv for package management, pyproject.toml as source of truth

### ✅ VII. justfile Task Automation
- **Status**: COMPLIANT
- **Verification**: Common tasks automated via justfile

### ✅ VIII. GitHub Actions Continuous Integration
- **Status**: COMPLIANT
- **Verification**: CI workflow will run tests, linting, formatting on all pushes/PRs

### ✅ IX. Pre-commit Hooks with Rust
- **Status**: COMPLIANT
- **Verification**: Rust-based pre-commit tools (prek/rustyhook) for code quality

### ✅ X. N+1 Query Prevention with DTOs
- **Status**: COMPLIANT
- **Verification**: All templates receive dataclass DTOs, not QuerySets. All DTO tests include `assertNumQueries`

### ✅ XI. Use Case Layer Architecture
- **Status**: COMPLIANT
- **Verification**: Business logic in use cases/services as functions (not classes), models contain only data structure. Use case functions follow "verb + noun" naming pattern (e.g., `get_event_topics()`, `create_topic()`). Use cases return DTOs/simple objects

### ✅ XII. No REST API (Current Version)
- **Status**: COMPLIANT
- **Verification**: HTMX hypermedia pattern only, no REST API endpoints

### ✅ XIII. UUID v6 for Primary Keys
- **Status**: COMPLIANT
- **Verification**: All models use UUIDField with uuid6.uuid6 default

### ✅ XIV. SlugField for URL Routes
- **Status**: COMPLIANT
- **Verification**: Events and topics use SlugField for URLs, slugs auto-generated from titles with uniqueness guarantee

### ✅ XV. AlpineJS for Client-Side State Management (Optional)
- **Status**: COMPLIANT
- **Verification**: AlpineJS is optional and used only when explicitly requested. HTMX prioritized for all interactions.
- **Usage Patterns** (HTMX-first):
  - Sign-in popups: HTMX to load modal fragment. AlpineJS only if explicitly requested.
  - Form validation: HTMX for server-side validation. AlpineJS only if explicitly requested.
  - Event selector: HTMX with native HTML select. AlpineJS only if explicitly requested.
  - Confirmation dialogs: HTMX to load dialog fragment. AlpineJS only if explicitly requested.
  - Loading indicators: HTMX native (hx-indicator) as default. AlpineJS only if explicitly requested.

**Overall Status**: ✅ ALL GATES PASSED - Ready for implementation

## Project Structure

### Documentation (this feature)

```text
specs/001-event-topics-platform/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command) ✅ Complete
├── data-model.md        # Phase 1 output (/speckit.plan command) ✅ Complete
├── quickstart.md        # Phase 1 output (/speckit.plan command) ✅ Complete
├── contracts/           # Phase 1 output (/speckit.plan command) ✅ Complete
│   └── htmx-views.md    # HTMX view contracts
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
floripatalks/
├── manage.py
├── pyproject.toml
├── justfile
├── floripatalks/          # Django project root
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── events/                 # Django app: Events and Topics
│   ├── __init__.py
│   ├── models.py          # Event, Topic, Vote, Comment, PresenterSuggestion models (data only, no business rules)
│   ├── models.py          # BaseModel, SoftDeleteModel, SoftDeleteManager
│   ├── use_cases/         # Business logic orchestration
│   │   ├── __init__.py
│   │   ├── create_topic.py
│   │   ├── edit_topic.py
│   │   ├── delete_topic.py
│   │   ├── vote_topic.py
│   │   ├── unvote_topic.py
│   │   ├── add_comment.py
│   │   ├── edit_comment.py
│   │   ├── delete_comment.py
│   │   ├── suggest_presenter.py
│   │   ├── edit_presenter_suggestion.py
│   │   └── delete_presenter_suggestion.py
│   ├── services/          # Reusable business logic
│   │   ├── __init__.py
│   │   ├── topic_service.py
│   │   ├── vote_service.py
│   │   ├── comment_service.py
│   │   └── presenter_service.py
│   ├── dto/               # Data Transfer Objects (dataclasses)
│   │   ├── __init__.py
│   │   ├── topic_dto.py
│   │   ├── comment_dto.py
│   │   └── presenter_dto.py
│   ├── views.py           # Django views (call use cases, convert to DTOs)
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── templates/
│   │   └── events/
│   │       ├── event_detail.html
│   │       ├── topic_list.html
│   │       ├── topic_detail.html
│   │       ├── topic_form.html
│   │       ├── topic_edit.html
│   │       └── partials/   # HTMX partial fragments
│   │           ├── topic_item.html
│   │           ├── topic_list_fragment.html
│   │           ├── comment_item.html
│   │           └── vote_button.html
│   └── cotton/            # Django-Cotton components
│       ├── topic/
│       │   ├── card.html
│       │   └── vote_button.html
│       ├── comment/
│       │   └── item.html
│       └── presenter/
│           └── suggestion.html
├── accounts/               # Django app: User authentication
│   ├── __init__.py
│   ├── models.py          # Custom user model (AbstractUser)
│   ├── views.py           # SSO authentication views
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           └── login_popup.html  # AlpineJS popup component
├── core/                   # Shared utilities and base models
│   ├── __init__.py
│   ├── models.py           # BaseModel, SoftDeleteModel, SoftDeleteManager
│   ├── middleware.py      # Rate limiting middleware
│   └── utils.py           # Shared utilities
├── tests/
│   ├── __init__.py
│   ├── unit/              # Unit tests (majority)
│   │   ├── events/
│   │   │   ├── test_use_cases/
│   │   │   ├── test_services/
│   │   │   └── test_dto/
│   │   └── accounts/
│   ├── integration/       # Integration tests (fewer)
│   │   ├── events/
│   │   └── accounts/
│   └── conftest.py        # pytest fixtures
└── static/
    ├── css/
    │   └── pure-css/      # Pure CSS library
    └── js/
        ├── htmx.min.js
        └── alpine.min.js  # AlpineJS (optional, only when explicitly requested)
```

**Structure Decision**: Django web application structure with app-based architecture. Events app contains all topic-related functionality. Accounts app handles authentication. Core app provides shared utilities. Tests follow test pyramid structure (majority unit tests, fewer integration tests). AlpineJS and HTMX work together: AlpineJS for client-side UI state, HTMX for server interactions.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all constitution principles are followed.

## Phase Status

### Phase 0: Outline & Research ✅ COMPLETE
- **research.md**: Generated with technology decisions (django-allauth, HTMX patterns, use case architecture, AlpineJS integration patterns)
- All technical unknowns resolved
- Best practices documented for all technology choices including AlpineJS usage patterns

### Phase 1: Design & Contracts ✅ COMPLETE
- **data-model.md**: Complete data model with all entities, relationships, and validation rules
- **contracts/htmx-views.md**: HTMX view contracts defined (no REST API)
- **quickstart.md**: Setup and development guide created
- Agent context updated

### Phase 2: Task Breakdown
- **Status**: Pending `/speckit.tasks` command
- **Next Step**: Run `/speckit.tasks` to generate implementation task list

## AlpineJS/HTMX Integration Patterns

Based on clarifications, the following patterns are established:

1. **Sign-in Popups**: AlpineJS (`x-show`/`x-if`) for toggle, HTMX for authentication flow
2. **Form Validation**: AlpineJS for real-time client-side feedback (character count, validation), HTMX for form submission and server-side validation
3. **Event Selector**: AlpineJS for dropdown toggle, HTMX to load selected event content
4. **Confirmation Dialogs**: AlpineJS for modal toggle, HTMX to execute confirmed actions
5. **Loading Indicators**: HTMX native (`hx-indicator`) as default, AlpineJS optional for custom loading states

**General Rule**: AlpineJS for client-side UI state (no server communication needed), HTMX for all server interactions.

## Next Steps

1. ✅ Constitution check passed
2. ✅ Research completed (research.md)
3. ✅ Data model designed (data-model.md)
4. ✅ Contracts defined (contracts/htmx-views.md)
5. ✅ Quickstart guide created (quickstart.md)
6. ✅ AlpineJS integration patterns documented
7. ⏭️ **Run `/speckit.tasks`** to generate implementation task breakdown

**Recommended next command**: `/speckit.tasks`
