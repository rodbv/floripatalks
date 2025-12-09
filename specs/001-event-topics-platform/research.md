# Research: Event Topics Platform

**Date**: 2025-12-09  
**Feature**: Event Topics Platform  
**Status**: Complete

## Research Summary

All technical decisions align with the constitution and existing specifications. No additional research required as all technology choices are well-established and documented.

## Technology Decisions

### Django SSO Authentication

**Decision**: Use django-allauth for Google and LinkedIn SSO authentication

**Rationale**: 
- django-allauth is the standard Django library for social authentication
- Supports Google and LinkedIn OAuth2 out of the box
- Handles token management, user creation, and session management
- Well-maintained and widely used in Django community

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
- `assertNumQueries` in tests verifies N+1 prevention

**Implementation**:
- All views convert QuerySets to dataclass DTOs
- Prefetch/select_related in services before DTO conversion
- DTOs contain only data needed by templates
- Tests use `assertNumQueries` to verify query count

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

