# FloripaTalks Constitution

Core principles and learnings that guide development decisions.

## Debugging Principles

**Always verify fundamental assumptions first**: When debugging production issues, immediately check which settings file is loaded (`DJANGO_SETTINGS_MODULE`), what `DEBUG` value is active, and what `ALLOWED_HOSTS` contains. Symptoms can mask root causes—verify core assumptions before diving deep into symptoms.
