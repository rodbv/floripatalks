<!--
Sync Impact Report:
Version Change: 1.2.0 → 1.3.0 (added security and data model principles)
Modified Principles: 
  - II. Django Framework (expanded with custom user model requirement)
Added Sections: 
  - XIII. UUID v7 for Primary Keys
  - XIV. SlugField for URL Routes
  - Custom User Model (added to Django Framework principle)
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/plan-template.md (✅ no changes needed - data model decisions)
  - .specify/templates/spec-template.md (✅ no changes needed)
  - .specify/templates/tasks-template.md (✅ no changes needed)
Follow-up TODOs: None
-->

# FloripaTalks Constitution

## Project Overview

**Project Type**: Web Application

**Technology Stack**:
- **Backend Framework**: Django
- **Testing Framework**: pytest
- **Frontend Enhancement**: HTMX
- **Component System**: Django-Cotton
- **Package Manager**: uv
- **Task Runner**: justfile
- **CI/CD**: GitHub Actions
- **Pre-commit**: Rust-based tools (prek/rustyhook)

**Development Methodology**: Test-Driven Development (TDD)

**Rationale**: This is a web application built with Django, using HTMX for frontend interactivity and Django-Cotton for component-based UI. The project follows TDD principles with pytest, uses modern Python tooling (uv), and enforces code quality through automated CI/CD and pre-commit hooks.

## Core Principles

### I. Test-Driven Development (TDD) - NON-NEGOTIABLE

All features MUST be developed using Test-Driven Development methodology. The Red-Green-Refactor cycle is strictly enforced:

1. **Red**: Write a failing test that describes the desired behavior
2. **Green**: Write the minimum code necessary to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

**Rationale**: TDD ensures code reliability, facilitates refactoring, provides living documentation, and prevents regressions. Tests serve as a safety net for future changes.

**Enforcement**: Tests MUST be written before implementation code. Pull requests without corresponding tests will be rejected.

### II. Django Framework

The project MUST use Django as the primary web framework, adhering to Django best practices and conventions:

- Follow Django's app-based architecture
- Use Django's ORM for database operations
- Leverage Django's built-in features (admin, authentication, etc.) before introducing external alternatives
- Maintain separation of concerns: models, views, templates, forms
- Use Django's class-based views where appropriate
- Follow Django naming conventions and project structure
- Use a custom user model inheriting from `AbstractUser` (not Django's default User model)

**Rationale**: Django provides a robust, scalable foundation with built-in security features, admin interface, and a mature ecosystem. Consistency with Django conventions improves maintainability and developer onboarding. Using a custom user model from the start (Django best practice) prevents migration issues later and allows customization of user fields.

### III. pytest Testing Framework and Test Pyramid

All tests MUST be written using pytest following the test pyramid principle:

- **Unit tests** (majority): Focus on use cases and services with data-oriented tests covering edge cases
- **Integration tests** (fewer): Test happy paths end-to-end, verify component interactions
- **Contract tests**: For interfaces and boundaries when applicable
- Test fixtures for reusable test data and setup
- pytest-django for Django-specific testing utilities
- All DTO tests MUST include `assertNumQueries` to verify N+1 query prevention
- Test strategy: More unit tests, fewer integration tests (test pyramid principle)

**Rationale**: pytest offers superior test discovery, fixtures, parametrization, and plugin ecosystem compared to Django's default test runner. The test pyramid (more unit tests, fewer integration tests) provides faster feedback, better isolation, and more comprehensive edge case coverage. Unit tests on use cases and services are data-oriented and easier to maintain.

### IV. HTMX Hypermedia Pattern

Frontend interactivity MUST be implemented using HTMX following hypermedia principles:

- Use HTMX attributes (`hx-get`, `hx-post`, `hx-swap`, etc.) for dynamic behavior
- Prefer HTMX over custom JavaScript for server-driven interactions
- Follow hypermedia pattern: serve HTML responses (not JSON) with partial HTML fragments for HTMX requests
- Return partial HTML fragments from Django views for HTMX requests (not full pages)
- Use HTMX events for complex interactions when needed
- Maintain progressive enhancement: core functionality works without JavaScript
- The system does NOT have a REST API in the current version (may exist in the future)

**Rationale**: HTMX enables dynamic, interactive UIs without writing extensive JavaScript, keeping the frontend simple and maintainable while leveraging Django's template system. The hypermedia pattern (HTML responses with partial fragments) aligns with HTMX best practices and provides a simpler, more maintainable architecture than traditional REST APIs.

### V. Component-Based UI with Django-Cotton

UI components MUST be created using Django-Cotton following these best practices:

- **Component Organization**: Organize components in a `cotton/` directory within each Django app, using subdirectories to reflect hierarchy (e.g., `cotton/sidebar/menu/link.html` → `<c-sidebar.menu.link />`)
- **Component Syntax**: Use HTML-like syntax for components to benefit from editor features:
  ```html
  <c-button variant="primary">Click me</c-button>
  ```
- **Reusability**: Extract repeated UI patterns into reusable components
- **Props/Slots**: Use Django-Cotton's prop and slot system for component composition
- **Naming**: Use kebab-case for component names (e.g., `user-card.html` → `<c-user-card />`)
- **Documentation**: Document component props, usage, and examples in component files

**Rationale**: Django-Cotton promotes modular, maintainable frontend code by enabling reusable components while staying within Django's template system. Component-based architecture reduces duplication and improves consistency.

### VI. uv Dependency Management

Python dependencies MUST be managed using `uv`:

- Use `uv` for installing, updating, and managing packages
- Maintain `pyproject.toml` as the source of truth for dependencies
- Use `uv.lock` for reproducible builds (commit lock file to version control)
- Run `uv sync` to ensure development environment matches dependencies
- Use `uv add <package>` and `uv remove <package>` for dependency changes

**Rationale**: `uv` provides fast, reliable Python package management with better performance than pip and built-in virtual environment management. It ensures consistent environments across development and CI/CD.

### VII. justfile Task Automation

Common development tasks MUST be automated using `justfile`:

- Define tasks for: running tests, starting dev server, running migrations, linting, formatting
- Use descriptive task names and include help text
- Make tasks composable and reusable
- Document task dependencies and prerequisites
- Include tasks for common workflows (e.g., `just test`, `just dev`, `just lint`)

**Rationale**: `justfile` provides a simple, fast task runner that centralizes common commands, reduces manual errors, and improves developer productivity. It's more maintainable than shell scripts or complex Makefiles.

### VIII. GitHub Actions Continuous Integration

All tests MUST run automatically via GitHub Actions on:

- Every push to any branch
- Every pull request
- Before merging to main branch

The CI workflow MUST:
- Run the full test suite using pytest
- Check code formatting and linting
- Verify pre-commit hooks pass
- Fail the build if any check fails
- Provide clear feedback on failures

**Rationale**: Automated testing in CI ensures code quality, prevents regressions, and provides confidence in merges. Early detection of issues reduces debugging time and maintains codebase health.

### IX. Pre-commit Hooks with Rust

Code quality checks MUST be enforced via pre-commit hooks using Rust-based tools:

- Use Rust-based pre-commit runners (e.g., `prek` or `rustyhook`) for performance
- Configure hooks for: code formatting, linting, type checking, security scanning
- Ensure hooks run quickly to not impede development workflow
- All hooks MUST pass before commits are accepted
- Document hook configuration and requirements

**Rationale**: Rust-based pre-commit tools offer superior performance compared to Python-based alternatives. Pre-commit hooks catch issues early, enforce code standards, and maintain codebase consistency without requiring manual intervention.

### X. N+1 Query Prevention with DTOs

All templates (full pages and partial fragments) MUST receive dataclasses as Data Transfer Objects (DTOs), NOT Django QuerySets or model instances:

- All views MUST convert QuerySets to dataclass DTOs before passing to templates
- Templates receive only dataclasses, single values, or simple objects
- All DTO tests MUST include `assertNumQueries` to verify query count
- Prefetch related objects and select related fields to prevent N+1 queries at the service/use case layer
- Query optimization MUST happen before DTO conversion

**Rationale**: Passing QuerySets to templates risks N+1 queries when templates access related objects. DTOs force explicit data fetching and optimization at the service layer, making query performance predictable and testable. `assertNumQueries` ensures N+1 prevention is verified in tests.

### XI. Use Case Layer Architecture

Business logic MUST be separated from models using a use case layer:

- **Models**: Contain only data structure, validation, and basic ORM operations (no business rules)
- **Services**: Provide reusable business logic, can access ORM models and return QuerySets
- **Use Cases**: Orchestrate business workflows, use services for common code, return only dataclasses, single values, or simple objects (NOT QuerySets or Django model instances)
- **Views**: Call use cases, convert results to DTOs, pass to templates
- Business rules MUST NOT be in models - they belong in use cases or services

**Rationale**: Separating business logic from models improves testability, maintainability, and follows single responsibility principle. Use cases are data-oriented and easily unit testable. Services provide reusable logic while use cases orchestrate workflows. This architecture enables comprehensive unit testing with fewer integration tests.

### XII. No REST API (Current Version)

The system does NOT expose a REST API in the current version:

- All interactions use HTMX hypermedia pattern (HTML responses with partial fragments)
- Future API support may be added but is out of scope for initial version
- Focus on server-rendered HTML with HTMX for dynamic interactions

**Rationale**: The hypermedia approach with HTMX provides a simpler architecture for the current needs, reducing complexity and maintenance overhead. API support can be added later if needed without affecting the core hypermedia implementation.

### XIII. UUID v7 for Primary Keys

All model primary keys MUST use UUID v7 (not auto-incrementing integers):

- Use `uuid.UUID` with UUID v7 format for all model primary keys
- UUID v7 is time-ordered and sortable (unlike UUID v4)
- Prevents ID enumeration attacks (security benefit)
- Use Django's `uuid` field: `id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)`

**Rationale**: UUID v7 provides security by preventing ID guessing/enumeration attacks while maintaining sortability (time-ordered). Unlike sequential integers, UUIDs make it difficult for attackers to enumerate resources. UUID v7's time-ordered nature allows efficient database indexing and sorting by creation time.

### XIV. SlugField for URL Routes

Events and topics MUST use Django SlugField for URL-friendly identifiers:

- Events use `slug` field (e.g., "python-floripa") for URLs: `/events/python-floripa/`
- Topics use `slug` field for URLs: `/topics/<slug>/`
- Use Django's `SlugField` with appropriate `max_length` and `unique` constraints
- Slugs are human-readable and SEO-friendly
- Primary keys remain UUID v7 (slugs are for URLs, not primary keys)

**Rationale**: Slugs provide human-readable, SEO-friendly URLs while maintaining security through UUID primary keys. Users can share meaningful URLs (e.g., `/events/python-floripa/`) while the system uses UUIDs internally for security. This follows Django best practices for URL design.

## Development Workflow

### Code Review Requirements

- All code changes MUST be reviewed via pull request
- Pull requests MUST include tests (per TDD principle)
- Pull requests MUST pass all CI checks
- At least one approval required before merge
- Constitution compliance MUST be verified during review

### Quality Gates

Before merging, code MUST:
- Pass all tests (unit, integration, contract)
- Pass linting and formatting checks
- Pass pre-commit hooks
- Have appropriate test coverage
- Follow Django and project conventions
- Include documentation for new features

## Governance

### Amendment Procedure

Changes to this constitution require:
1. Proposal via pull request with clear rationale
2. Discussion and review by project maintainers
3. Approval from project maintainers
4. Update to version number following semantic versioning
5. Update to "Last Amended" date
6. Propagation to dependent templates and documentation

### Versioning Policy

This constitution follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Backward-incompatible changes, removal of principles, or fundamental governance changes
- **MINOR**: Addition of new principles, significant expansions to existing principles, or new mandatory sections
- **PATCH**: Clarifications, typo fixes, wording improvements, or non-semantic refinements

### Compliance Review

- All pull requests MUST verify constitution compliance
- Regular reviews should be conducted to ensure adherence
- Violations must be documented and addressed promptly
- Complexity exceptions must be explicitly justified

### Constitution Supremacy

This constitution supersedes all other development practices and guidelines. When conflicts arise, the constitution takes precedence. All team members and contributors are expected to follow these principles.

**Version**: 1.3.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
