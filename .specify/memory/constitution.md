<!--
Sync Impact Report:
Version Change: 1.4.0 → 1.5.0 (added GitHub issues and branch naming requirements)
Modified Principles:
  - Development Workflow (expanded with GitHub issues and branch naming)
Added Sections:
  - GitHub Issues and Branch Naming (added to Development Workflow)
Removed Sections: None
Templates Requiring Updates:
  - .specify/templates/plan-template.md (✅ no changes needed)
  - .specify/templates/spec-template.md (✅ no changes. NM needed)
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
- **Client-Side State**: AlpineJS (when needed)
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

### XV. AlpineJS for Client-Side State Management

AlpineJS MUST be used for simple client-side state control and interactions when server communication is not required:

- Use AlpineJS for local UI state management (toggles, dropdowns, form validation feedback, etc.)
- Serve AlpineJS from static files (not CDN) for better control and offline capability
- Prefer HTMX for server-driven interactions; use AlpineJS only when client-side state is sufficient
- Keep AlpineJS usage minimal and focused on simple state management
- AlpineJS directives (`x-data`, `x-show`, `x-if`, `x-for`, etc.) should be used inline in templates
- Do not create complex AlpineJS components - prefer Django-Cotton components for reusable UI patterns

**Rationale**: AlpineJS provides lightweight client-side reactivity without the overhead of larger JavaScript frameworks. It complements HTMX by handling simple UI state (modals, dropdowns, form toggles) that don't require server communication. Serving from static files ensures better control, versioning, and offline capability. Keeping AlpineJS usage minimal maintains the simplicity of the HTMX hypermedia approach.

## Development Workflow

### GitHub Issues and Branch Naming

All implementation tasks MUST be tracked via GitHub issues:

- Every task MUST have a corresponding GitHub issue before work begins
- GitHub issues MUST be linked to pull requests
- Branch names MUST follow the pattern: `{issue-id}-{description-in-slug-format}`
  - Example: `123-view-topics-list`, `456-add-vote-functionality`
  - Issue ID is the GitHub issue number
  - Description is a short, descriptive slug (kebab-case, no special characters)
- Branch names MUST be descriptive and traceable to the GitHub issue
- **Issues created automatically from `tasks.md` via `speckit.taskstoissues` MUST be labeled with `speckit`** to distinguish them from manually created issues

**Rationale**: GitHub issues provide traceability, discussion context, and project management visibility. Standardized branch naming makes it easy to identify which issue a branch addresses and maintains consistency across the team. The `speckit` label helps identify issues that were automatically generated from the specification process.

### Git Operations and Version Control

AI agents and automated tools MUST NOT perform git commits or pushes automatically:

- **NEVER commit changes automatically** - Always allow the developer to review diffs first
- **NEVER push to remote automatically** - Developer must explicitly request push operations
- Changes should be staged and ready for review, but commits must be initiated by the developer
- This ensures developers maintain control over version control history and can review changes before committing

**Rationale**: Developers need to review code changes, understand diffs, and maintain control over git history. Automatic commits can create messy history, make it harder to track changes, and prevent proper code review. This principle ensures developers have full visibility and control over version control operations.

### Task Implementation Workflow with Human Review

All task implementation MUST follow a strict workflow with mandatory human review:

- **Implementation Phase**: AI agent implements the task with tests (following TDD)
- **Review Phase**: Developer manually reviews the implementation, tests, and diffs
- **Commit Phase**: Developer commits and pushes changes when satisfied
- **Completion Phase**: Developer notifies the AI agent that the task is complete
- **Task Progression**: AI agent MUST NOT proceed to the next task until explicitly notified by the developer
- **No Automatic Progression**: AI agents MUST NEVER automatically mark tasks as complete or move to the next task

**Workflow Steps**:
1. AI implements task with tests
2. AI waits for developer review
3. Developer reviews, commits, and pushes (if satisfied)
4. Developer explicitly notifies AI: "task done" or "próxima task" or similar
5. Only then does AI mark task complete and proceed to next task

**Rationale**: Human review is essential for code quality, understanding, and maintaining control over the development process. Automatic task progression can lead to issues being overlooked, poor code quality, and loss of developer agency. This workflow ensures every change is consciously reviewed and approved before moving forward.

### Commit Message Format

Commit messages MUST be concise and follow a consistent format:

- **Format**: `<type>: <subject>` (max 50 chars for subject)
- **Total length**: Maximum 200 characters (including subject and body)
- **Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`
- **Style**: Imperative mood ("Add feature" not "Added feature")
- **Body**: Optional, wrap at 72 chars, keep total under 200 chars

**Examples**:
- `feat: Add HTMX infinite scroll`
- `fix: Resolve static files warning`
- `docs: Update constitution with uv run rule`
- `refactor: Split settings into base/dev/prod`

**Rationale**: Concise commit messages improve readability in git history and make it easier to understand changes at a glance. The 200-character limit ensures messages remain focused and scannable.

### Code Review Requirements

- All code changes MUST be reviewed via pull request
- Pull requests MUST reference the GitHub issue number in the title or description
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

**Version**: 1.5.1 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
