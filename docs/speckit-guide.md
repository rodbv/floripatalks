# SpecKit Usage Guide

This guide explains how to use SpecKit (Spec-Driven Development) in the FloripaTalks project. SpecKit helps maintain clear specifications, structured implementation plans, and documentation aligned with code.

## Table of Contents

- [What is SpecKit?](#what-is-speckit)
- [Available Commands](#available-commands)
- [Workflow Overview](#workflow-overview)
- [Best Practices](#best-practices)
- [Issue Management](#issue-management)
- [When to Update Specs vs Document for Later](#when-to-update-specs-vs-document-for-later)
- [Common Workflows](#common-workflows)
- [Troubleshooting](#troubleshooting)

---

## What is SpecKit?

SpecKit is a specification-driven development system that helps you:

- **Maintain consistency** between specifications, plans, and implementation
- **Generate actionable tasks** from user stories and requirements
- **Track progress** through structured documentation
- **Ensure quality** through automated consistency checks

### Key Artifacts

SpecKit uses several key documents:

- **`spec.md`**: User stories, functional requirements, acceptance criteria
- **`plan.md`**: Technical architecture, tech stack, project structure
- **`tasks.md`**: Actionable, dependency-ordered task list
- **`data-model.md`**: Database entities and relationships
- **`contracts/`**: API/HTMX endpoint definitions
- **`research.md`**: Technical decisions and rationale
- **`.specify/memory/constitution.md`**: Project principles and constraints

---

## Available Commands

### `/speckit.specify`

**Purpose**: Create a new feature specification from scratch.

**When to use**: Starting a new feature or major functionality.

**What it does**:
- Creates a new feature branch
- Generates `spec.md` template
- Sets up feature directory structure

**Example**:
```
/speckit.specify
```

---

### `/speckit.clarify`

**Purpose**: Identify underspecified areas and ask clarification questions.

**When to use**: After creating a spec, before planning implementation.

**What it does**:
- Scans spec for ambiguities
- Asks up to 5 targeted clarification questions
- Encodes answers back into the spec

**Example**:
```
/speckit.clarify
```

**Best practice**: Run this BEFORE `/speckit.plan` to reduce rework.

---

### `/speckit.plan`

**Purpose**: Generate technical implementation plan.

**When to use**: After clarifying the spec, before creating tasks.

**What it does**:
- Generates `plan.md` with tech stack and architecture
- Creates `research.md` for technical decisions
- Generates `data-model.md` for database design
- Creates `contracts/` for API/HTMX endpoints
- Creates `quickstart.md` for test scenarios

**Example**:
```
/speckit.plan
```

**Output**: Technical plan and design artifacts in `specs/{feature-name}/`

---

### `/speckit.tasks`

**Purpose**: Generate actionable, dependency-ordered task list.

**When to use**: After planning, when ready to start implementation.

**What it does**:
- Reads `spec.md` and `plan.md`
- Generates `tasks.md` with all implementation tasks
- Organizes tasks by user story and priority
- Marks parallelizable tasks with `[P]`
- Creates dependency graph

**Example**:
```
/speckit.tasks
```

**Output**: `tasks.md` with numbered, organized tasks

---

### `/speckit.analyze`

**Purpose**: Check consistency across all artifacts.

**When to use**:
- After generating tasks
- After making changes to specs/plans
- Before starting implementation
- Periodically during development

**What it does**:
- Reads-only (non-destructive)
- Checks consistency between spec, plan, and tasks
- Identifies missing requirements
- Detects contradictions
- Validates against constitution

**Example**:
```
/speckit.analyze
```

**Output**: Analysis report with issues and optional remediation plan

---

### `/speckit.implement`

**Purpose**: Execute implementation plan by processing tasks.

**When to use**: When ready to start coding.

**What it does**:
- Checks checklist completion (if checklists exist)
- Loads tasks from `tasks.md`
- Executes tasks in dependency order
- Updates task status as work progresses

**Example**:
```
/speckit.implement
```

---

### `/speckit.checklist`

**Purpose**: Create checklists for quality gates.

**When to use**: Before implementation, to define quality criteria.

**Example**:
```
/speckit.checklist
```

---

### `/speckit.taskstoissues`

**Purpose**: Convert tasks to GitHub issues.

**When to use**: When ready to track tasks in GitHub.

**Example**:
```
/speckit.taskstoissues
```

---

### `/speckit.constitution`

**Purpose**: Manage project constitution (principles and constraints).

**When to use**: When project principles need to be updated.

**Example**:
```
/speckit.constitution
```

---

## Workflow Overview

### Standard Feature Development Flow

```
1. /speckit.specify          → Create feature spec
2. /speckit.clarify          → Clarify ambiguities
3. /speckit.plan             → Generate technical plan
4. /speckit.tasks            → Generate task list
5. /speckit.analyze          → Check consistency
6. /speckit.implement        → Start implementation
```

### Quick Iteration Flow

If you're iterating on an existing feature:

```
1. Update spec.md or plan.md manually
2. /speckit.tasks            → Regenerate tasks
3. /speckit.analyze          → Verify consistency
4. Continue implementation
```

---

## Best Practices

### 1. Keep Specs Focused

- One feature per spec directory
- Clear user stories with priorities
- Explicit acceptance criteria

### 2. Run Analysis Regularly

- After generating tasks
- After updating specs
- Before major implementation phases

### 3. Update Tasks When Needed

- When requirements change
- When architecture decisions are made
- When dependencies are discovered

### 4. Document Decisions

- Use `research.md` for technical decisions
- Update `plan.md` when architecture changes
- Keep `constitution.md` aligned with principles

### 5. Maintain Consistency

- Run `/speckit.analyze` before committing major changes
- Fix inconsistencies immediately
- Keep all artifacts in sync

---

## Issue Management

### Creating Issues

**Best Practice**: Create issues for:
- Bugs and defects
- Feature requests
- Non-blocking improvements
- Future optimizations
- Questions and discussions

### Issue Labels

Use labels to categorize:

- `bug`: Something broken
- `enhancement`: New feature or improvement
- `documentation`: Documentation updates
- `future`: Non-blocking, can be deferred
- `blocking`: Prevents progress
- `question`: Needs discussion

### Issue Workflow

1. **Create issue** with clear description
2. **Add labels** for categorization
3. **Link to related tasks** in `tasks.md` (optional)
4. **Assign priority** (P1, P2, P3)
5. **Update status** as work progresses

### When to Create Issues vs Update Specs

**Create Issue**:
- Non-blocking improvements
- Future optimizations
- Questions that need discussion
- Ideas for later consideration

**Update Specs**:
- Blocking requirements
- Breaking changes
- Architectural decisions
- Already implemented features (update docs to match code)

---

## When to Update Specs vs Document for Later

This is a critical decision that affects workflow efficiency.

### Decision Matrix

| Change Type | Impact | Action | Example |
|------------|--------|--------|---------|
| **Bug fix** | Blocks current work | **Update immediately** | Critical bug preventing login |
| **Breaking API change** | Blocks current work | **Update immediately** | Changing authentication method |
| **New requirement** | Blocks current work | **Update immediately** | New user story added |
| **Code quality improvement** | Non-blocking | **Document for later** | Switching to a better testing library |
| **Performance optimization** | Non-blocking | **Document for later** | Query optimization technique |
| **Tool/library upgrade** | Depends | **Assess first** | Django version upgrade |
| **Documentation update** | Non-blocking | **Document for later** | Adding examples to docs |

### Quick Assessment Questions

Ask yourself:

1. **Does this block current tasks?**
   - ✅ Yes → Update specs immediately
   - ❌ No → Document for later

2. **Can this wait until the polish phase?**
   - ✅ Yes → Create issue, document for later
   - ❌ No → Update specs immediately

3. **Will changing specs disrupt current focus?**
   - ✅ Yes → Document for later
   - ❌ No → Update specs immediately

### Recommended Process

#### For Non-Blocking Improvements

1. **Create GitHub Issue**:
   ```
   Title: Consider using [tool/library] for [purpose]
   Labels: enhancement, future
   Description:
   - Current approach: [what we use now]
   - Proposed: [what we want to use]
   - Rationale: [why it's better]
   - Impact: [what needs to change]
   - Priority: Low (non-blocking)
   ```

2. **Add Brief Note** (optional):
   - Add a comment in relevant spec file: `<!-- Future: See issue #XXX -->`
   - Don't change tasks.md or plan.md

3. **Continue Current Work**:
   - Don't change existing specs/tasks
   - Stay focused on current phase

4. **Review During Polish Phase**:
   - Batch process accumulated improvements
   - Update specs together
   - Run `/speckit.analyze` to verify consistency

#### For Blocking Changes

1. **Assess Impact**:
   - What specs need updating?
   - What tasks are affected?
   - What code needs changes?

2. **Update Artifacts**:
   - Update `spec.md` if requirements change
   - Update `plan.md` if architecture changes
   - Update `tasks.md` if tasks change
   - Update `constitution.md` if principles change

3. **Verify Consistency**:
   - Run `/speckit.analyze`
   - Fix any inconsistencies
   - Regenerate tasks if needed

4. **Continue Implementation**:
   - Proceed with updated specs

### Example: "We should use django-assert-num-queries"

**Scenario**: You think a different testing tool would be better, but current approach works.

**Assessment**:
- ✅ Current approach works (`pytest_django.asserts.assertNumQueries`)
- ✅ Non-blocking improvement
- ✅ Can wait until polish phase

**Action**: **Document for later**

1. Create GitHub issue:
   ```
   Title: Consider django-assert-num-queries for query testing
   Labels: enhancement, testing, future
   Description: [rationale, comparison, impact]
   ```

2. Add optional note to `spec.md`:
   ```markdown
   ## Future Improvements
   - Consider django-assert-num-queries (see issue #XXX)
   ```

3. Continue with current tasks

4. Revisit during polish phase

**Why this approach?**
- Maintains focus on current work
- Captures idea for later
- Avoids disrupting workflow
- Allows batch processing of improvements

---

## Common Workflows

### Starting a New Feature

```bash
# 1. Create specification
/speckit.specify

# 2. Clarify ambiguities
/speckit.clarify

# 3. Generate technical plan
/speckit.plan

# 4. Generate tasks
/speckit.tasks

# 5. Check consistency
/speckit.analyze

# 6. Start implementation
/speckit.implement
```

### Updating an Existing Feature

```bash
# 1. Update spec.md or plan.md manually
# (edit files directly)

# 2. Regenerate tasks
/speckit.tasks

# 3. Verify consistency
/speckit.analyze

# 4. Continue implementation
```

### Handling a New Idea During Development

```bash
# 1. Quick assessment: blocking or non-blocking?
# If non-blocking:

# 2. Create GitHub issue
# (use GitHub web interface or CLI)

# 3. Add brief note to spec (optional)
# <!-- Future: See issue #XXX -->

# 4. Continue current work
# Don't change specs/tasks

# 5. Revisit during polish phase
```

### Fixing Inconsistencies

```bash
# 1. Run analysis
/speckit.analyze

# 2. Review report
# Identify issues

# 3. Fix inconsistencies
# Update relevant artifacts

# 4. Re-run analysis
/speckit.analyze

# 5. Verify all issues resolved
```

---

## Troubleshooting

### "Migration socialaccount.0001_initial is applied before its dependency sites.0001_initial"

**Problem**: Database migration history is inconsistent.

**Solution**:
```bash
# Mark sites migrations as applied
sqlite3 db.sqlite3 "INSERT OR IGNORE INTO django_migrations (app, name, applied) VALUES ('sites', '0001_initial', datetime('now'));"

# Create sites table if missing
sqlite3 db.sqlite3 "CREATE TABLE IF NOT EXISTS django_site (id INTEGER PRIMARY KEY AUTOINCREMENT, domain VARCHAR(100) NOT NULL UNIQUE, name VARCHAR(50) NOT NULL);"

# Run migrations
uv run python manage.py migrate
```

### "No installed app with label 'sites'"

**Problem**: `django.contrib.sites` not in `INSTALLED_APPS`.

**Solution**: Add to `floripatalks/settings/base.py`:
```python
INSTALLED_APPS = [
    # ...
    "django.contrib.sites",  # Required for django-allauth
    # ...
]
```

### Tasks.md is Out of Sync

**Problem**: Tasks don't match current spec/plan.

**Solution**:
```bash
# Regenerate tasks
/speckit.tasks

# Verify consistency
/speckit.analyze
```

### Analysis Shows Inconsistencies

**Problem**: `/speckit.analyze` reports issues.

**Solution**:
1. Review the analysis report
2. Identify which artifacts need updating
3. Update specs, plan, or tasks as needed
4. Re-run analysis to verify fixes

---

## Tips for Future Developers

### 1. Read Before Writing

- Read existing specs to understand patterns
- Review `constitution.md` for project principles
- Check `research.md` for past decisions

### 2. Keep Specs Updated

- Update specs when requirements change
- Update plans when architecture changes
- Keep tasks in sync with specs

### 3. Use Analysis Regularly

- Run `/speckit.analyze` before major commits
- Fix inconsistencies immediately
- Don't let issues accumulate

### 4. Document Decisions

- Use `research.md` for technical decisions
- Explain "why" not just "what"
- Link to relevant issues or discussions

### 5. Stay Focused

- Don't change specs for non-blocking improvements
- Create issues for future work
- Batch improvements during polish phase

### 6. Ask Questions

- If unsure, create an issue with `question` label
- Discuss with team before making breaking changes
- Review constitution before changing principles

---

## Additional Resources

- [SpecKit Repository](https://github.com/github/spec-kit)
- [Project Constitution](.specify/memory/constitution.md)
- [OAuth Setup Guide](oauth-setup-instructions.md)

---

## Quick Reference

### Command Cheat Sheet

| Command | When to Use | Output |
|---------|-------------|--------|
| `/speckit.specify` | New feature | `spec.md` |
| `/speckit.clarify` | After specify | Updated `spec.md` |
| `/speckit.plan` | After clarify | `plan.md`, `research.md`, etc. |
| `/speckit.tasks` | After plan | `tasks.md` |
| `/speckit.analyze` | Before/after changes | Analysis report |
| `/speckit.implement` | Ready to code | Implementation progress |

### Decision Quick Reference

**Update Specs Now**:
- ✅ Blocks current work
- ✅ Breaking change
- ✅ Architectural decision
- ✅ Already implemented (update docs)

**Document for Later**:
- ✅ Non-blocking improvement
- ✅ Future optimization
- ✅ Nice-to-have feature
- ✅ In middle of phase

---

**Last Updated**: 2025-12-10  
**Maintained By**: FloripaTalks Team
