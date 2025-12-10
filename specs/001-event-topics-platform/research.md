# Research: Event Topics Platform

**Date**: 2025-12-09  
**Feature**: Event Topics Platform  
**Status**: Complete

## Research Summary

All technical decisions align with the constitution and existing specifications. No additional research required as all technology choices are well-established and documented.

## Technology Decisions

### Django SSO Authentication

**Decision**: Use django-allauth for Google SSO authentication

**Rationale**:
- django-allauth is the standard Django library for social authentication
- Supports Google OAuth2 out of the box
- Handles token management, user creation, and session management
- Well-maintained and widely used in Django community

**Implementation**:
- Google: OAuth2 provider (`allauth.socialaccount.providers.google`)

**Future Enhancement**:
- LinkedIn SSO support is planned for a future release. It will use django-allauth's OpenID Connect provider (`allauth.socialaccount.providers.openid_connect`) with `provider_id: "linkedin"`.

**Alternatives considered**:
- Custom OAuth2 implementation: Rejected - too much complexity for standard use case
- django-social-auth: Rejected - less maintained than django-allauth

### HTMX Hypermedia Pattern

**Decision**: Use HTMX with partial HTML fragment responses

**Rationale**:
- Aligns with constitution principle IV (HTMX Hypermedia Pattern)
- Partial fragments enable smooth updates without full page refreshes
- Server-rendered HTML maintains SEO and accessibility
- Simpler than SPA architecture for this use case

**Implementation pattern**:
- Full page requests return complete HTML
- HTMX requests (hx-get, hx-post) return partial HTML fragments
- Use `hx-swap` to target specific DOM elements
- Maintain browser history with `hx-push-url` for edit pages

**Alternatives considered**:
- REST API + JavaScript framework: Rejected - violates constitution (no API principle)
- Full page refreshes: Rejected - poor UX, doesn't meet smooth transition requirements

### Use Case Layer Architecture

**Decision**: Implement use case layer with services, following clean architecture principles

**Rationale**:
- Aligns with constitution principle XI (Use Case Layer Architecture)
- Separates business logic from models and views
- Enables comprehensive unit testing
- Services provide reusable logic, use cases orchestrate workflows

**Pattern**:
- Models: Data structure, validation, basic ORM (no business rules)
- Services: Reusable business logic, can return QuerySets
- Use Cases: Orchestrate workflows, return dataclasses/simple objects
- Views: Call use cases, convert to DTOs, pass to templates

**Alternatives considered**:
- Fat models: Rejected - violates constitution, harder to test
- View-based logic: Rejected - violates separation of concerns

### DTO Pattern for N+1 Prevention

**Decision**: Use dataclasses as DTOs, convert QuerySets before passing to templates

**Rationale**:
- Aligns with constitution principle X (N+1 Query Prevention with DTOs)
- Forces explicit query optimization at service/use case layer
- Makes query performance predictable and testable
- `assertNumQueries` from `pytest_django.asserts` in tests verifies N+1 prevention (pytest-django provides this without requiring TestCase inheritance)

**Implementation**:
- All views convert QuerySets to dataclass DTOs
- Prefetch/select_related in services before DTO conversion
- DTOs contain only data needed by templates
- Tests use `assertNumQueries` from `pytest_django.asserts` to verify query count

**Alternatives considered**:
- Passing QuerySets to templates: Rejected - risks N+1 queries
- Manual prefetch in templates: Rejected - violates separation of concerns

### Soft Delete Pattern

**Decision**: Use `is_deleted` boolean field with indexed custom manager

**Rationale**:
- Aligns with specification requirement
- Allows recovery by admins
- Custom manager filters `is_deleted=False` by default
- Indexed field for performance

**Implementation**:
- Add `is_deleted = models.BooleanField(default=False, db_index=True)` to models
- Custom manager: `objects = SoftDeleteManager()` filters by default
- Admin can access all objects including deleted
- Regular queries automatically exclude deleted items

**Alternatives considered**:
- Hard delete: Rejected - no recovery option
- Separate archive table: Rejected - unnecessary complexity for MVP

### AlpineJS for Client-Side State Management (Optional)

**Decision**: AlpineJS is **optional** and should be used **only when explicitly requested** by the developer. This project prioritizes showcasing HTMX and hypermedia capabilities.

**Rationale**:
- This project is a showcase of HTMX and hypermedia power
- AlpineJS should be used only when HTMX cannot elegantly solve a problem
- Prioritize demonstrating server-driven interactions, HTML fragments, and hypermedia patterns
- AlpineJS remains optional to showcase HTMX capabilities
- Served from static files when used (not CDN) for better control and offline capability

**Implementation Patterns** (HTMX-first approach):
- **Authentication redirects**: Use `HttpResponseClientRedirect` from `django-htmx` for HTMX requests, standard Django redirect for regular requests. Include `next` parameter to return users after authentication.
- **Form validation**: HTMX for server-side validation with error fragments. Character count via HTML/CSS or vanilla JS. AlpineJS only if explicitly requested.
- **Event selector**: HTMX with native HTML select (hx-get/hx-trigger) to load content. AlpineJS only if explicitly requested.
- **Confirmation dialogs**: HTMX to load confirmation dialog fragment from server. AlpineJS only if explicitly requested.
- **Loading indicators**: HTMX native (`hx-indicator`) as default. AlpineJS only if explicitly requested.

**General Rule**: **HTMX first, AlpineJS only when explicitly requested**. Showcase hypermedia and server-driven interactions.

**Alternatives considered**:
- HTMX for everything: **Preferred** - This is the project's primary goal
- AlpineJS for client-side state: Optional - use only when explicitly requested
- Vanilla JavaScript: Acceptable for simple interactions if HTMX cannot handle it
- Larger frameworks (React, Vue): Rejected - too heavy, contradicts project goals

### Rate Limiting

**Decision**: Use Django middleware or django-ratelimit for rate limiting

**Rationale**:
- Prevents abuse (10 topics/hour, 20 comments/hour per user)
- django-ratelimit is lightweight and Django-native
- Can be implemented as decorator or middleware

**Implementation**:
- Apply rate limiting at view level
- Store rate limit data in cache (Redis recommended for production)
- Return user-friendly error messages with retry time

**Alternatives considered**:
- Custom middleware: Rejected - django-ratelimit is battle-tested
- No rate limiting: Rejected - security risk, violates spec requirement

### Infinite Scroll Implementation

**Decision**: Use HTMX infinite scroll with `hx-trigger="revealed"`

**Rationale**:
- Aligns with specification (infinite scroll chosen)
- HTMX `hx-trigger="revealed"` triggers when element enters viewport
- Server returns partial HTML fragments with next batch
- Maintains smooth user experience

**Implementation**:
- Load initial batch (e.g., 20 topics)
- Each topic item has `hx-get` with `hx-trigger="revealed"` on last item
- Server returns next batch as partial fragment
- Append to list, repeat until all topics loaded

**Alternatives considered**:
- Pagination: Rejected - doesn't meet spec requirement
- Show all: Rejected - performance issue with 1000+ topics

### Internationalization (i18n)

**Decision**: Use Django's built-in i18n framework with pt-BR as primary language

**Rationale**:
- Django i18n is standard and well-supported
- pt-BR is primary language, timezone America/Sao_Paulo
- Framework supports future language expansion
- Use `USE_I18N = True`, `LANGUAGE_CODE = 'pt-br'`, `TIME_ZONE = 'America/Sao_Paulo'`

**Implementation**:
- Configure Django settings for pt-BR
- Use `gettext` for translatable strings
- Template tags: `{% load i18n %}`, `{% trans "text" %}`
- Future languages can be added via translation files

**Alternatives considered**:
- Hard-coded Portuguese: Rejected - violates i18n requirement
- Third-party i18n library: Rejected - Django i18n is sufficient

### Static Assets: Pure CSS and HTMX

**Decision**: Serve Pure CSS and HTMX from static folder (not CDN), using latest versions available as of 2025-12-09

**Rationale**:
- Serving from static folder provides better control and offline development capability
- No external CDN dependency reduces risk of CDN outages
- Better performance (served from same domain, no DNS lookup)
- Version control of assets ensures consistency across environments
- Works offline during development

**Implementation**:
- Download latest Pure CSS and HTMX versions
- Place in `static/css/pure-css/` and `static/js/htmx.min.js`
- Reference in templates using `{% static %}` template tag
- Update versions as needed, commit to version control
- Pure CSS: Download from https://purecss.io/ (latest version as of 2025-12-09)
- HTMX: Download from https://htmx.org/ (latest version as of 2025-12-09)

**File structure**:
```
static/
├── css/
│   └── pure-css/
│       └── pure-min.css (or individual module files)
└── js/
    └── htmx.min.js
```

**Template usage**:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/pure-css/pure-min.css' %}">
<script src="{% static 'js/htmx.min.js' %}"></script>
```

**Alternatives considered**:
- CDN (unpkg, jsDelivr): Rejected - external dependency, potential outages, privacy concerns
- npm package: Rejected - adds complexity, static files simpler for this use case

### Type Annotations

**Decision**: Use Python type annotations throughout the codebase

**Rationale**:
- Improves code readability and IDE support
- Enables static type checking with ruff
- Serves as inline documentation
- Catches type-related errors early
- Required by constitution (Principle I-A)

**Implementation**:
- All functions and methods must have type hints
- DTOs (dataclasses) must have type annotations for all fields
- Use modern Python 3.13+ syntax (`list[str]` instead of `List[str]`)
- Pre-commit hooks enforce type annotations via ruff

## No Additional Research Needed

All technology choices are:
- Aligned with constitution principles
- Well-documented in Django ecosystem
- Standard patterns for Django + HTMX applications
- No experimental or unclear technologies

## Next Steps

Proceed to Phase 1: Design & Contracts to create:
- Data model with entities and relationships
- HTMX view contracts (not REST API)
- Quickstart guide
