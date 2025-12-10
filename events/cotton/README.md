# Django-Cotton Components for Events App

This directory contains reusable UI components for the events app, following Django-Cotton conventions.

## Structure

- `topic/` - Topic-related components
  - `card.html` - Topic card component (to be created)
  - `vote_button.html` - Vote button component (to be created)
- `comment/` - Comment-related components
  - `item.html` - Comment item component (to be created)
- `presenter/` - Presenter suggestion components
  - `suggestion.html` - Presenter suggestion component (to be created)

## Usage

Components are used in templates using Django-Cotton syntax:

```html
<c-topic.card title="..." vote_count="..." />
<c-topic.vote-button topic_slug="..." />
<c-comment.item comment="..." />
<c-presenter.suggestion suggestion="..." />
```

## Naming Convention

- Use kebab-case for component files (e.g., `vote-button.html`)
- Component names map to template paths (e.g., `topic/vote-button.html` → `<c-topic.vote-button />`)
