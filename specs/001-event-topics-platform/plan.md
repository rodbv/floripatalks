# Implementation Plan: Event Topics Platform

**Branch**: `001-event-topics-platform` | **Date**: 2025-12-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-event-topics-platform/spec.md`

## Summary

FloripaTalks is a mobile-first web application for managing event topics where users can suggest, vote on, and comment about talk topics for local events. The system uses Django with HTMX hypermedia pattern, following a use case layer architecture with DTOs to prevent N+1 queries. Users authenticate via Google/LinkedIn SSO, and the interface is primarily in Portuguese (pt-BR) with timezone America/Sao_Paulo.

## Technical Context

**Language/Version**: Python 3.12+  
**Primary Dependencies**: Django, HTMX, Django-Cotton, pytest, pytest-django, django-allauth (for SSO), pure-css  
**Storage**: PostgreSQL (recommended) or SQLite (development)  
**Testing**: pytest with pytest-django, following test pyramid (more unit tests, fewer integration tests)  
**Target Platform**: Web (mobile-first, responsive)  
**Project Type**: Web application  
**Performance Goals**: Event pages load in under 2 seconds on mobile, support 1000+ topics per event without degradation  
**Constraints**: Mobile-first design, WCAG 2.1 Level AA accessibility, no REST API (HTMX hypermedia only), Portuguese (pt-BR) primary language, timezone America/Sao_Paulo  
**Scale/Scope**: Multiple events, 1000+ topics per event, unlimited users, rate limiting (10 topics/hour, 20 comments/hour per user)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Research Gates

✅ **I. TDD**: All features will be developed using TDD (Red-Green-Refactor)  
✅ **II. Django Framework**: Using Django with app-based architecture  
✅ **III. pytest & Test Pyramid**: Using pytest with focus on unit tests for use cases/services, fewer integration tests  
✅ **IV. HTMX Hypermedia Pattern**: Using HTMX with HTML responses and partial fragments (no REST API)  
✅ **V. Django-Cotton Components**: Using Django-Cotton for component-based UI  
✅ **VI. uv Dependency Management**: Using uv for package management  
✅ **VII. justfile**: Using justfile for task automation  
✅ **VIII. GitHub Actions**: CI/CD via GitHub Actions  
✅ **IX. Pre-commit with Rust**: Using Rust-based pre-commit tools  
✅ **X. N+1 Prevention with DTOs**: All templates receive dataclasses as DTOs, not QuerySets  
✅ **XI. Use Case Layer**: Business logic in use cases/services, not models  
✅ **XII. No REST API**: Hypermedia pattern only, no API endpoints

### Post-Design Gates

✅ **I. TDD**: Plan includes TDD approach for all features  
✅ **II. Django Framework**: Architecture follows Django app-based structure  
✅ **III. pytest & Test Pyramid**: Test structure defined (unit tests in use_cases/services, integration tests for happy paths)  
✅ **IV. HTMX Hypermedia Pattern**: All views return HTML (full pages or partial fragments), no JSON responses  
✅ **V. Django-Cotton Components**: Component structure defined in `cotton/` directories  
✅ **VI. uv Dependency Management**: Dependencies will be managed with uv  
✅ **VII. justfile**: Task automation via justfile  
✅ **VIII. GitHub Actions**: CI/CD will run tests automatically  
✅ **IX. Pre-commit with Rust**: Pre-commit hooks will use Rust-based tools  
✅ **X. N+1 Prevention with DTOs**: Architecture includes DTO layer, views convert QuerySets to DTOs before templates  
✅ **XI. Use Case Layer**: Architecture clearly separates models, services, use cases, and views  
✅ **XII. No REST API**: All contracts are HTMX views returning HTML, no API endpoints

**All gates pass.** Architecture fully aligns with constitution principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-event-topics-platform/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
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
│   ├── models.py          # Event, Topic models (data only, no business rules)
│   ├── managers.py        # Custom managers with is_deleted filtering
│   ├── use_cases/         # Business logic orchestration
│   │   ├── __init__.py
│   │   ├── create_topic.py
│   │   ├── edit_topic.py
│   │   ├── delete_topic.py
│   │   ├── vote_topic.py
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
│   ├── models.py          # Custom user model if needed
│   ├── views.py           # SSO authentication views
│   ├── urls.py
│   └── templates/
│       └── accounts/
│           └── login_popup.html
├── core/                   # Shared utilities
│   ├── __init__.py
│   ├── middleware.py      # Rate limiting middleware
│   └── utils.py
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
    │   └── pure-css/      # Pure CSS library (served from static, not CDN)
    │       └── pure-min.css
    └── js/
        └── htmx.min.js     # HTMX library (served from static, not CDN)
```

**Structure Decision**: Django web application structure with app-based architecture. Events app contains all topic/comment/vote functionality. Use case layer separates business logic from models. DTOs ensure N+1 prevention. Django-Cotton components in `cotton/` directories. HTMX partial fragments in `templates/partials/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. Architecture aligns with constitution principles.
