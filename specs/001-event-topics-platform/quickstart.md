# Quickstart Guide: Event Topics Platform

**Date**: 2025-12-09  
**Feature**: Event Topics Platform

## Overview

This guide provides a quick overview of how to get started with the Event Topics Platform feature. It covers the key user flows and system behavior.

## User Flows

### Non-Authenticated User Flow

1. **Browse Topics**
   - Navigate to `/events/python-floripa/`
   - View topics list with vote counts and comment counts
   - Scroll down to load more topics (infinite scroll)
   - Read topic descriptions, comments, and presenter suggestions

2. **Attempt Interaction**
   - Click "Vote" button → Popup appears: "Please sign in to vote"
   - Click "Add Topic" → Popup appears: "Please sign in to add topics"
   - Click "Comment" → Popup appears: "Please sign in to comment"
   - Popup offers Google or LinkedIn SSO login options

3. **Sign In**
   - Click "Sign in with Google" or "Sign in with LinkedIn" in popup
   - Complete SSO authentication
   - Redirected back to page, now authenticated

### Authenticated User Flow

1. **View Topics**
   - Navigate to event page
   - See topics ordered by vote count (descending), then creation date (oldest first)
   - Infinite scroll loads more topics as you scroll

2. **Create Topic**
   - Click "Add Topic"
   - Fill in title (required, max 200 chars) and description (optional, max 2000 chars)
   - Submit form
   - Topic appears at top of list (HTMX updates without full page refresh)
   - Can create up to 10 topics per hour (rate limit)

3. **Vote on Topic**
   - Click vote button on any topic
   - Vote count increments, button shows "Voted" state
   - Can un-vote by clicking again
   - Vote count decrements, button shows "Vote" state

4. **Comment on Topic**
   - Click "Comment" on a topic
   - Enter comment text (max 1000 chars)
   - Submit comment
   - Comment appears in comments section (HTMX updates)
   - Can create up to 20 comments per hour (rate limit)

5. **Edit Own Content**
   - Click "Edit" on own topic/comment/suggestion
   - Navigate to dedicated edit page (not modal)
   - Modify content and submit
   - Redirected back with updated content
   - Browser back button works seamlessly

6. **Delete Own Content**
   - Click "Delete" on own topic/comment/suggestion
   - Confirm deletion
   - Content is soft-deleted (hidden from regular users, recoverable by admins)
   - HTMX removes element from view

7. **Suggest Presenter**
   - On topic page, click "Suggest Presenter"
   - Provide at least one of: email, URL (LinkedIn), or full name
   - Submit suggestion
   - Suggestion appears with topic
   - Limited to 3 suggestions per user per topic, 10 total per topic

8. **Switch Events**
   - Use event selector in navigation
   - Switch to different event
   - See topics specific to that event
   - URL updates to event slug (e.g., `/events/python-floripa/`)

## Admin Flow

1. **Access Django Admin**
   - Navigate to `/admin/`
   - Login with admin credentials

2. **Manage Content**
   - View all topics, comments, suggestions (including soft-deleted)
   - Recover soft-deleted content by setting `is_deleted=False`
   - Permanently delete content if needed
   - Manage users and events
   - Moderate inappropriate content

## Key Behaviors

### Infinite Scroll
- Initial load: First 20 topics
- Scroll down: More topics load automatically when last item enters viewport
- Loading indicator shown while fetching
- End of list handled gracefully

### HTMX Interactions
- Vote/un-vote: Button updates without page refresh
- Comment creation: Comment appears immediately
- Topic creation: Topic appears at top of list
- Delete actions: Element removed from view
- All transitions smooth, no full page refreshes

### Soft Delete
- User deletes content → Hidden from regular users immediately
- Content remains in database with `is_deleted=True`
- Admins can view and recover deleted content
- Recovery restores content to regular view

### Rate Limiting
- Topic creation: 10 per hour per user
- Comment creation: 20 per hour per user
- Exceeding limit: Error message shows retry time
- Limits reset after time window

### Mobile-First Design
- All functionality accessible on mobile devices
- Touch-friendly buttons and inputs
- Responsive layout (320px to 768px width)
- Optimized for mobile viewing

### Internationalization
- Primary language: Portuguese (pt-BR)
- Timezone: America/Sao_Paulo
- Dates and times formatted according to locale
- Future languages can be added via translation files

## Error Scenarios

### SSO Authentication Failure
- Provider unavailable: Error message with retry option
- User cancels: Return to page with message
- Network error: Error message with retry option
- All errors user-friendly, no technical jargon

### Validation Errors
- Empty topic title: Error message, form not submitted
- Exceeds character limit: Error message with current count
- Exceeds rate limit: Error message with retry time
- All errors displayed inline, form state preserved

### Authorization Errors
- Edit/delete others' content: 403 Forbidden, error message
- Access admin without permissions: 403 Forbidden
- All errors explain what went wrong

## Performance Expectations

- Event pages load in under 2 seconds on mobile
- HTMX transitions complete without noticeable delay
- Infinite scroll loads next batch smoothly
- System handles 1000+ topics per event without degradation
- Query optimization prevents N+1 queries (verified with assertNumQueries in tests)

## Accessibility

- WCAG 2.1 Level AA compliance
- Keyboard navigation supported
- Screen reader compatible
- Focus indicators visible
- Color contrast meets standards
- All interactive elements accessible

