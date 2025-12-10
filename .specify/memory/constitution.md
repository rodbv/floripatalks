<!--
Sync Impact Report:
Version Change: 1.7.0 → 1.8.0 (added Django Admin Interface Requirements principle)
Modified Principles:
  - Django Framework (added subsection II-A for admin requirements)
Added Sections:
  - Django Admin Interface Requirements (II-A) - comprehensive admin pages for all models with excellent 1:N relationship support
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/plan-template.md (✅ no changes needed)
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
- **Client-Side State**: AlpineJS (minimized, only when explicitly requested)
- **Component System**: Django-Cotton
- **Package Manager**: uv
- **Task Runner**: justfile
- **CI/CD**: GitHub Actions
- **Pre-commit**: pre-commit framework

**Development Methodology**: Test-Driven Development (TDD)

**Rationale**: This is a web application built with Django, using HTMX for frontend interactivity, AlpineJS for client-side state management when needed, and Django-Cotton for component-based UI. The project follows TDD principles with pytest, uses modern Python tooling (uv), and enforces code quality through automated CI/CD and pre-commit hooks.

## Core Principles

### I. Test-Driven Development (TDD) - NON-NEGOTIABLE

All features MUST be developed using Test-Driven Development methodology. The Red-Green-Refactor cycle is strictly enforced:

1. **Red**: Write a failing test that describes the desired behavior
2. **Green**: Write the minimum code necessary to make the test pass
3. **Refactor**: Improve code quality while keeping tests green

**Rationale**: TDD ensures code reliability, facilitates refactoring, provides living documentation, and prevents regressions. Tests serve as a safety net for future changes.

**Enforcement**: Tests MUST be written before implementation code. Pull requests without corresponding tests will be rejected.

### I-A. Type Annotations

All Python code MUST use type annotations:

- Functions and methods MUST have type hints for parameters and return values
- Class attributes SHOULD have type hints
- Use `typing` module for complex types (Optional, List, Dict, etc.)
- Use modern Python 3.12+ syntax when available (e.g., `list[str]` instead of `List[str]`)
- Type annotations help with IDE support, static analysis, and code documentation
- Pre-commit hooks will check type annotations via ruff

**Rationale**: Type annotations improve code readability, enable better IDE support, catch type-related errors early, and make the codebase more maintainable. They serve as inline documentation and help with static analysis tools.

### II. Django Framework

The project MUST use Django as the primary web framework, adhering to Django best practices and conventions:

- Follow Django's app-based architecture
- Use Django's ORM for database operations
- Leverage Django's built-in features (admin, authentication, etc.) before introducing external alternatives
- Maintain separation of concerns: models, views, templates, forms
- Use Django's class-based views where appropriate
- Follow Django naming conventions and project structure
- Use a custom user model inheriting from `AbstractUser` (not Django's default User model)

**Model Base Classes**:
- All models MUST inherit from `BaseModel` (defined in `core/models.py`) which provides:
  - UUID v6 primary key (`id`)
  - `created_at` timestamp (auto_now_add)
  - `updated_at` timestamp (auto_now)
- Models requiring soft delete MUST inherit from `SoftDeleteModel` (defined in `core/models.py`) which extends `BaseModel` with:
  - `is_deleted` boolean field (indexed, default=False)
  - Custom `SoftDeleteManager` that filters `is_deleted=False` by default
  - `all_objects` manager for accessing deleted records (admin use)
- Models that don't need soft delete inherit directly from `BaseModel`
- This pattern ensures DRY, consistency, and maintainability across all models

**Rationale**: Django provides a robust, scalable foundation with built-in security features, admin interface, and a mature ecosystem. Consistency with Django conventions improves maintainability and developer onboarding. Using a custom user model from the start (Django best practice) prevents migration issues later and allows customization of user fields. Base model classes eliminate code duplication, ensure consistency across models, and centralize common patterns like soft delete.

### III. pytest Testing Framework and Test Pyramid

All tests MUST be written using pytest following the test pyramid principle:

- **Unit tests** (majority): Focus on use cases and services with data-oriented tests covering edge cases
- **Integration tests** (fewer): Test happy paths end-to-end, verify component interactions
- **Contract tests**: For interfaces and boundaries when applicable
- Test fixtures for reusable test data and setup
- pytest-django for Django-specific testing utilities
- All DTO tests MUST include `assertNumQueries` to verify N+1 query prevention
- Test strategy: More unit tests, fewer integration tests (test pyramid principle)

**Testing Tools and Best Practices**:
- **model-bakery**: Use `model_bakery` for creating test model instances when useful (simpler than manual creation)
- **pytest fixtures**: Use fixtures in `tests/conftest.py` for shared test data and setup (e.g., user fixtures, event fixtures)
- **faker**: Use `faker` library for generating random test data (usernames, emails, text) instead of manual timestamps or hardcoded values
- **Fixtures organization**: Place app-specific fixtures in `tests/conftest.py` or app-specific conftest files
- **Fixture reuse**: Extract common patterns (e.g., `user_factory`, `event_factory`) into fixtures to reduce duplication

**Rationale**: pytest offers superior test discovery, fixtures, parametrization, and plugin ecosystem compared to Django's default test runner. The test pyramid (more unit tests, fewer integration tests) provides faster feedback, better isolation, and more comprehensive edge case coverage. Unit tests on use cases and services are data-oriented and easier to maintain. Using model-bakery, fixtures, and faker simplifies test code, reduces duplication, and makes tests more maintainable and readable.

### IV. HTMX Hypermedia Pattern

Frontend interactivity MUST be implemented using HTMX following hypermedia principles:

- Use HTMX attributes (`hx-get`, `hx-post`, `hx-swap`, etc.) for dynamic behavior
- Prefer HTMX over custom JavaScript for server-driven interactions
- Follow hypermedia pattern: serve HTML responses (not JSON) with partial HTML fragments for HTMX requests
- Return partial HTML fragments from Django views for HTMX requests (not full pages)
- Use HTMX events for complex interactions when needed
- Maintain progressive enhancement: core functionality works without JavaScript
- The system does NOT have a REST API in the current version (may exist in the future)
- For client-side state management and simple interactions that don't require server communication, use AlpineJS (see Principle XV)

**Rationale**: HTMX enables dynamic, interactive UIs without writing extensive JavaScript, keeping the frontend simple and maintainable while leveraging Django's template system. The hypermedia pattern (HTML responses with partial fragments) aligns with HTMX best practices and provides a simpler, more maintainable architecture than traditional REST APIs. AlpineJS complements HTMX by handling client-side state when server communication is not needed.

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

Python dependencies and commands MUST be managed using `uv`:

- Use `uv` for installing, updating, and managing packages
- Maintain `pyproject.toml` as the source of truth for dependencies
- Use `uv.lock` for reproducible builds (commit lock file to version control)
- Run `uv sync` to ensure development environment matches dependencies
- Use `uv add <package>` and `uv remove <package>` for dependency changes
- **Use `uv run <command>` for ALL Python/Django commands** (e.g., `uv run python manage.py migrate`, `uv run pytest`, `uv run django-admin`)
- Do NOT activate virtual environments manually - `uv run` handles this automatically
- Do NOT use `source .venv/bin/activate` - always use `uv run` instead

**Rationale**: `uv` provides fast, reliable Python package management with better performance than pip and built-in virtual environment management. It ensures consistent environments across development and CI/CD. Using `uv run` for all commands eliminates the need to manually manage virtual environments and ensures consistent execution contexts.

### VII. justfile Task Automation

Common development tasks MUST be automated using `justfile`:

- Define tasks for: running tests, starting dev server, running migrations, linting, formatting
- Use descriptive task names and include help text
- Make tasks composable and reusable
- Document task dependencies and prerequisites
- Include tasks for common workflows (e.g., `just test`, `just dev`, `just migrate`, `just lint`)
- **Use `just` commands instead of direct `uv run python manage.py` for ergonomics** (e.g., `just manage migrate` instead of `uv run python manage.py migrate`)
- All Django management commands should be accessible via `just manage <command>`

**Rationale**: `justfile` provides a simple, fast task runner that centralizes common commands, reduces manual errors, and improves developer productivity. It's more maintainable than shell scripts or complex Makefiles. Using `just` commands improves ergonomics and makes the codebase more approachable for new developers.

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

### IX. Pre-commit Hooks

Code quality checks MUST be enforced via pre-commit hooks:

- Use `pre-commit` (Python-based) for hook management
- Install with: `uv add --dev pre-commit` or `pip install pre-commit`
- Configure hooks for: code formatting, linting, type checking, security scanning
- Initialize with: `pre-commit install`
- Ensure hooks run quickly to not impede development workflow
- All hooks MUST pass before commits are accepted
- Document hook configuration and requirements

**Rationale**: Pre-commit hooks catch issues early, enforce code standards, and maintain codebase consistency without requiring manual intervention. The standard `pre-commit` framework is well-maintained, widely used, and integrates seamlessly with Python projects.

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

### XIII. UUID v6 for Primary Keys

All model primary keys MUST use UUID v6 (not auto-incrementing integers):

- Use `uuid6` library with UUID v6 format for all model primary keys
- UUID v6 is time-ordered and sortable (unlike UUID v4)
- Prevents ID enumeration attacks (security benefit)
- Use Django's `uuid` field: `id = models.UUIDField(primary_key=True, default=uuid6.uuid6, editable=False)`
- Install `uuid6` package: `uv add uuid6`

**Rationale**: UUID v6 provides security by preventing ID guessing/enumeration attacks while maintaining sortability (time-ordered). Unlike sequential integers, UUIDs make it difficult for attackers to enumerate resources. UUID v6's time-ordered nature allows efficient database indexing and sorting by creation time. UUID v6 is used instead of v7 because it's available via the `uuid6` library and provides the same time-ordered benefits.

### XIV. SlugField for URL Routes

Events and topics MUST use Django SlugField for URL-friendly identifiers:

- Events use `slug` field (e.g., "python-floripa") for URLs: `/events/python-floripa/`
- Topics use `slug` field for URLs: `/topics/<slug>/`
- Use Django's `SlugField` with appropriate `max_length` and `unique` constraints
- Slugs are human-readable and SEO-friendly
- Primary keys remain UUID v6 (slugs are for URLs, not primary keys)

**Rationale**: Slugs provide human-readable, SEO-friendly URLs while maintaining security through UUID primary keys. Users can share meaningful URLs (e.g., `/events/python-floripa/`) while the system uses UUIDs internally for security. This follows Django best practices for URL design.

### XV. AlpineJS for Client-Side State Management (Optional)

**Primary Principle**: This project is a showcase of HTMX and hypermedia capabilities. AlpineJS is **optional** and should be used **only when explicitly requested** by the developer.

- **HTMX First**: Always explore HTMX solutions first (hypermedia, HTML fragments, server-driven interactions)
- **AlpineJS as Last Resort**: Use AlpineJS only when explicitly requested, after demonstrating that HTMX cannot solve the problem elegantly
- **Showcase Hypermedia**: Prioritize demonstrating the power of HTMX, small HTML fragments, and server-driven UI updates
- **Static Files**: When AlpineJS is used, serve it from static files (not CDN) for better control and offline capability
- **Inline Directives**: AlpineJS directives (`x-data`, `x-show`, `x-if`, `x-for`, etc.) should be used inline in templates when needed
- **No Complex Components**: Do not create complex AlpineJS components - prefer Django-Cotton components or HTMX patterns

**Rationale**: This project aims to showcase how far HTMX and hypermedia can go before needing client-side JavaScript. AlpineJS is optional and should be used only when explicitly requested to demonstrate the power of server-driven interactions, HTML fragments, and the hypermedia approach. Only use AlpineJS when explicitly requested by the developer after exploring HTMX solutions.

### XVI. Semantic HTML and Modern HTML Controls

All HTML MUST use semantic elements and modern HTML5 controls to leverage native browser capabilities:

- **Semantic HTML**: Use appropriate semantic elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`, `<form>`, `<button>`, etc.) instead of generic `<div>` elements when semantically appropriate
- **Modern HTML Controls**: Use native HTML5 input types and controls to avoid unnecessary JavaScript validators:
  - `<input type="email">` for email addresses
  - `<input type="url">` for URLs
  - `<input type="tel">` for phone numbers
  - `<input type="number">` for numeric input
  - `<input type="date">` for date selection
  - `<input type="time">` for time selection
  - `<input type="datetime-local">` for date and time
  - `<input type="color">` for color selection
  - `<input type="range">` for numeric ranges
  - `<input type="search">` for search inputs
  - `<input type="password">` for password fields
  - `<textarea>` with appropriate attributes for multi-line text
  - `<select>` for dropdown selections
  - `<datalist>` for autocomplete suggestions
- **Native Validation**: Leverage HTML5 native validation attributes (`required`, `min`, `max`, `minlength`, `maxlength`, `pattern`, etc.) instead of custom JavaScript validators when possible
- **Accessibility**: Semantic HTML improves accessibility by providing proper structure for screen readers and assistive technologies
- **Progressive Enhancement**: Native controls work without JavaScript, ensuring core functionality is always available

**Rationale**: Semantic HTML improves accessibility, SEO, and code maintainability. Modern HTML5 controls provide native browser validation, better mobile experience (e.g., native date pickers on mobile), and reduce the need for custom JavaScript validators. This approach aligns with progressive enhancement principles and reduces client-side complexity while improving user experience across devices.

## Development Workflow

### Task Implementation Workflow

All task implementation MUST follow a strict workflow with mandatory human review:

**Workflow Steps**:
1. Create GitHub issue ONLY for the task currently being worked on (not in advance)
2. Create branch: `{issue-id}-{description-in-slug-format}` (use two leading zeros, e.g., `029-custom-user-model`)
3. AI implements task with tests (following TDD)
4. AI waits for developer review
5. Developer reviews, commits, and pushes (if satisfied)
6. Create PR with "Closes #X" to automatically close issue on merge
7. Developer explicitly notifies AI when task is complete
8. Only then does AI proceed to next task

**Key Rules**:
- **One Issue Per Task**: Create issue only when starting work on that specific task, not in bulk
- **Branch Naming**: Must follow pattern `{issue-id}-{description-in-slug-format}` with two leading zeros
- **Issue Labels**: Issues created via `speckit.taskstoissues` MUST be labeled with `speckit`
- **No Automatic Progression**: AI agents MUST NEVER automatically mark tasks complete or move to next task
- **Human Review Required**: Every change must be reviewed before commit/push

**Rationale**: Creating issues only for current task prevents outdated issues. Human review ensures code quality and developer control. Branch naming with issue IDs creates clear traceability. This workflow prevents issues from becoming outdated and ensures every change is consciously reviewed.

### Git and Data Operations Restrictions

AI agents and automated tools MUST NOT perform certain operations automatically:

**Git Operations**:
- **NEVER commit changes automatically** - Always allow developer to review diffs first
- **NEVER push to remote automatically** - Developer must explicitly request push operations
- Changes should be staged and ready for review, but commits must be initiated by the developer

**Database Operations**:
- **NEVER delete databases, database files, or data** without explicit developer request
- **NEVER drop tables, truncate data, or reset migrations** without explicit approval
- **NEVER remove user data, test data, or production-like data** without explicit request
- If migration conflicts occur, propose solutions that preserve data (e.g., fake migrations, data migration scripts)
- Always ask before performing any operation that could result in data loss

**Rationale**: Developers need full control over version control history and data. Automatic operations can cause data loss, messy history, and prevent proper code review. This ensures developers maintain control and visibility over all critical operations.

### Commit Message Format (Conventional Commits)

Commit messages MUST follow the Conventional Commits specification and be validated by commitlint:

- **Format**: `<type>: <subject>` (max 50 chars for subject, lowercase)
- **Total length**: Maximum 300 characters (including subject and body)
- **Types**: `feature` (or `ft`), `hotfix` (or `hf`), `fix` (or `fx`), `bugfix` (or `bf`), `chore` (or `ch`)
- **Style**: Imperative mood, lowercase ("add feature" not "Added feature")
- **Body**: Optional, wrap at 72 chars, keep total under 300 chars
- **Footer**: Optional, for breaking changes or issue references
- **Language**: English only
- **Enforcement**: commitlint validates all commit messages via pre-commit hooks

**Examples**:
- `feature: add HTMX infinite scroll`
- `ft: add HTMX infinite scroll`
- `hotfix: resolve critical database connection issue`
- `hf: resolve critical database connection issue`
- `fix: resolve static files warning`
- `fx: resolve static files warning`
- `bugfix: resolve static files warning`
- `bf: resolve static files warning`
- `chore: update Django to 6.0`
- `ch: update Django to 6.0`

**Rationale**: Conventional Commits provide a standardized format that improves readability, enables automated tooling, and makes git history more scannable. The 300-character limit provides flexibility while keeping messages focused. commitlint ensures consistency across all commits.

### Code Comments and Documentation

Code comments and docstrings are NOT recommended as they may contradict code or compensate for non-clean code:

- **Code should be obvious and simple**: Well-written code should be self-explanatory and not require comments to understand
- **Only comment non-obvious, surprising code**: Comments should only be used for code that intentionally breaks best practices or contains non-obvious logic that cannot be made clearer through refactoring
- **No intermediary comments**: Do not leave temporary or intermediary comments explaining implementation decisions (e.g., "# using uuidv6 due to problem with uuidv7")
- **Same rule for docstrings**: Docstrings follow the same principle - only add them when the code's purpose cannot be made clear through better naming or structure
- **Prefer refactoring over commenting**: If code needs a comment to be understood, refactor it to be more obvious instead

**Rationale**: Comments can become outdated, contradict the code, and indicate that the code itself is not clear enough. Clean, well-named code with good structure should be self-documenting. Comments should be rare exceptions for truly surprising or intentionally non-standard code.

### Code Review and Quality Gates

All code changes MUST be reviewed via pull request and meet quality standards before merging:

**Review Requirements**:
- Pull requests MUST reference the GitHub issue number in the title or description
- Pull requests MUST include tests (per TDD principle)
- At least one approval required before merge
- Constitution compliance MUST be verified during review

**Quality Gates** (all must pass before merging):
- Pass all tests (unit, integration, contract)
- Pass linting and formatting checks
- Pass pre-commit hooks
- Pass all CI checks
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

**Version**: 1.8.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
