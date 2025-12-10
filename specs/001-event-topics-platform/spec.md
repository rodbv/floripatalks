# Feature Specification: Event Topics Platform

**Feature Branch**: `001-event-topics-platform`  
**Created**: 2025-12-09  
**Status**: Draft  
**Input**: User description: "we are implementing the first version of this web app. It is called FloripaTalks , created to support local events, and its goal is to be a mobile-first app in which users logged in via google/linkedin SSO can do the following: - see which topics people want to see as talks in future events (eg Advanced Django ORM, or Intro to Pandas/Polars) - vote or comment on topics they also want to see - add new topics themselves which will be available for other people to vote/comment - suggest a person who could present that talk - by  email or url (eg linkedin) or fullname - the system will start with a single monthly event (Python Floripa) but should support more in the future, in which people can switch somewhere on the site (with its own slug-like url like floripatalks/python-floripa Admins can use django admin to add or remove talks and suggestions, add and remove users, create new events, and other common admin tasks Accessibility and workoig mobile-first is a must. As frotend css library we will use pure-css"

## Clarifications

### Session 2025-12-09

- Q: How should topics be ordered in the list? → A: Vote count descending, then creation date (oldest first) for ties
- Q: How should the system handle SSO authentication failures? → A: Display user-friendly error message with retry option
- Q: Should the topics list use pagination, infinite scroll, or show all topics? → A: Infinite scroll (load more as user scrolls)
- Q: What are the maximum character limits for topic titles, descriptions, and comments? → A: 200 chars title, 2000 chars description, 1000 chars comment
- Q: Should there be limits on presenter suggestions? → A: Limit: 3 suggestions per user per topic, 10 total suggestions per topic

### Additional Requirements (2025-12-09)

- Non-authenticated users can view topics in readonly mode with sign-in popups for interactive actions
- Users can edit and delete their own topics, comments, and presenter suggestions
- Users can un-vote on topics they have voted on
- Editing occurs on dedicated pages (not modals) with seamless back button navigation
- HTMX is used for all transitions to minimize page refreshes
- Primary interface is Portuguese (pt-BR) with timezone America/Sao_Paulo, with i18n support

### Session 2025-12-09 (Continued)

- Q: When users delete content, should it be permanently removed or recoverable? → A: Soft delete (marked as deleted, hidden from users, recoverable by admins). Django ORM managers will filter by is_deleted=False by default on [Model].objects (indexed field)
- Q: Should there be rate limiting to prevent abuse? → A: Basic rate limiting (e.g., 10 topics/hour, 20 comments/hour per user)
- Q: Should users be able to search or filter topics? → A: No search/filtering in MVP (rely on vote-based sorting)

### Session 2025-12-09 (Final)

- Q: How should topic slugs be generated? → A: Automatically generated from title (using django.utils.text.slugify) with uniqueness guarantee (add numeric suffix if needed)
- Q: When a user edits a topic title, should the slug be updated automatically? → A: Keep slug immutable after creation (preserves URL stability and shared links)
- Q: How should comments be ordered in display? → A: Chronological order (oldest first)
- Q: How should presenter suggestions be ordered/displayed? → A: Chronological order (oldest first)
- Q: How many topics should be loaded per infinite scroll batch? → A: 20 topics per load

### Session 2025-12-09 (AlpineJS Integration - REVISED)

**Note**: This project prioritizes HTMX and hypermedia. AlpineJS is optional and should be used only when explicitly requested.

- Q: How should the sign-in popup be implemented when non-authenticated users click interactive buttons? → A: **HTMX-first approach**: Use HTMX to load a sign-in modal fragment from the server. AlpineJS only if explicitly requested.
- Q: How should form validation feedback be implemented (e.g., character count, real-time error messages)? → A: **HTMX-first approach**: Server-side validation with HTMX responses showing errors. Character count can be done with HTML/CSS or vanilla JS if needed. AlpineJS only if explicitly requested.
- Q: How should the event selector work in the interface? → A: **HTMX-first approach**: Use HTMX to load content when event is selected (native HTML select with hx-get/hx-trigger). AlpineJS only if explicitly requested.
- Q: How should confirmation dialogs (e.g., delete confirmation) be implemented? → A: **HTMX-first approach**: Use HTMX to load a confirmation dialog fragment from the server. AlpineJS only if explicitly requested.
- Q: How should loading indicators be implemented for HTMX requests? → A: HTMX native (hx-indicator) as default. AlpineJS only if explicitly requested for custom loading states.
- Q: What format should error messages use (validation, rate limiting, etc.)? → A: Inline messages below the relevant field/area, in Portuguese (pt-BR), using semantic HTML (e.g., `<div role="alert">`) for accessibility. Aligns with semantic HTML principles and progressive enhancement.
- Q: What happens when two users edit the same content (topic/comment/suggestion) simultaneously? → A: Last-write-wins (no locking). Simple approach for MVP, aligns with HTMX's fast update pattern. Optional warning if content changed since load.
- Q: How should the system handle network failures during HTMX requests (timeout, connection lost, server unavailable)? → A: Display inline error message in Portuguese (pt-BR) with retry button, using HTMX to retry the request. Aligns with semantic HTML principles and allows recovery without page reload.
- Q: What happens when a user's session expires during an action (vote, comment, edit)? → A: Redirect to login, after authentication return and automatically execute the original action. Preserves user context and allows completion of intended action.
- Q: How should the system format large numbers in display (e.g., vote counts > 1000, many comments)? → A: Simple formatting in Portuguese (pt-BR) (e.g., "1.234 votos", "567 comentários") without abbreviations like "1.2k". Maintains clarity and aligns with pt-BR conventions.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View and Browse Topics (Priority: P1)

A user (logged in or not) visits the event page and can see a list of topics that people want to see as talks in future events. Each topic displays its title, vote count, comment count, and any suggested presenters. Users can browse topics to understand what the community is interested in. Non-authenticated users have a readonly experience and see popups inviting them to sign in when attempting interactive actions.

**Why this priority**: This is the core value proposition - users need to see what topics exist before they can interact with them. Without this, the platform has no purpose. Allowing non-authenticated viewing increases discoverability and engagement.

**Independent Test**: A user (logged in or not) can navigate to an event page and see a list of topics with their vote counts and comment counts displayed. The list is readable and functional on mobile devices. Non-authenticated users see interactive buttons/links but receive sign-in prompts when clicking them.

**Acceptance Scenarios**:

1. **Given** a user (logged in or not) navigates to the Python Floripa event page, **When** they view the page, **Then** they see an initial set of topics for that event ordered by vote count (descending), then by creation date (oldest first) for ties, with vote counts and comment counts displayed, and more topics load automatically as they scroll down
2. **Given** a user is on a mobile device, **When** they view the topics list, **Then** the layout is optimized for mobile viewing with readable text and touch-friendly interactions
3. **Given** a topic has suggested presenters, **When** a user views that topic, **Then** they can see the presenter suggestions (email, URL, or fullname) associated with that topic
4. **Given** multiple events exist, **When** a user switches between events using the event selector, **Then** they see topics specific to the selected event
5. **Given** a non-authenticated user is viewing topics, **When** they click a vote button or other interactive element, **Then** a popup appears inviting them to sign in or sign up

---

### User Story 2 - Add, Edit, and Delete Topics (Priority: P2)

A logged-in user can create a new topic suggestion for an event. They provide a topic title and optionally a description. Once created, the topic appears in the list and is available for other users to vote on and comment. Users can edit and delete their own topics.

**Why this priority**: Following output-first approach, viewing and voting on existing topics is prioritized over creating new ones. Users can contribute topics after the core viewing and voting functionality is available. Allowing users to edit and delete their own topics gives them control over their contributions.

**Independent Test**: A logged-in user can fill out a form to add a new topic, submit it, immediately see their topic appear in the topics list, edit their own topic on a dedicated page, and delete their own topic.

**Acceptance Scenarios**:

1. **Given** a user is logged in, **When** they click "Add Topic" and fill in a topic title, **Then** they can submit the topic and it appears in the list
2. **Given** a user is adding a topic, **When** they provide only a title (no description), **Then** the topic is created successfully with just the title
3. **Given** a user submits a topic, **When** the topic is created, **Then** it appears in the topics list for that event and is available for voting and commenting
4. **Given** a user is on mobile, **When** they add a topic, **Then** the form is easy to use with mobile-friendly input fields
5. **Given** a user has created a topic, **When** they click edit on their own topic, **Then** they are taken to a dedicated edit page (not a modal) where they can modify the topic
6. **Given** a user is editing their topic on a dedicated page, **When** they submit the changes, **Then** they are returned to the topic list or detail page with their updated topic displayed, and the browser back button works seamlessly
7. **Given** a user has created a topic, **When** they click delete on their own topic, **Then** a confirmation modal appears (AlpineJS), and after confirmation, the topic is removed via HTMX

---

### User Story 3 - Vote and Un-vote on Topics (Priority: P1)

A logged-in user can vote on topics they want to see as talks. Each user can vote once per topic and can later un-vote (remove their vote). The vote count is displayed and updates in real-time when users vote or un-vote.

**Why this priority**: Following output-first approach, voting is a core interaction that allows users to engage with existing content immediately. Voting enables the community to prioritize topics, showing which talks are most desired. This is essential for event organizers to understand community interest. Allowing un-voting gives users flexibility to change their mind.

**Independent Test**: A logged-in user can click a vote button on any topic, see the vote count increment, and can later click to un-vote, which decreases the vote count. The user cannot vote again on the same topic after un-voting without first un-voting.

**Acceptance Scenarios**:

1. **Given** a user is logged in and viewing a topic, **When** they click the vote button, **Then** the vote count increases by one and the button indicates they have voted
2. **Given** a user has already voted on a topic, **When** they click the vote button again, **Then** they can un-vote, the vote count decreases by one, and the button indicates they have not voted
3. **Given** multiple users vote on a topic, **When** any user views the topic, **Then** they see the current total vote count
4. **Given** a user is on mobile, **When** they vote or un-vote on a topic, **Then** the vote action is easy to perform with a touch-friendly button

---

### User Story 4 - Comment, Edit, and Delete Comments on Topics (Priority: P2)

A logged-in user can add comments to topics to discuss them or provide additional context. Comments are displayed with the commenter's name and timestamp. Users can read all comments on a topic. Users can edit and delete their own comments.

**Why this priority**: Comments enable community discussion and provide context about why a topic is valuable or what aspects should be covered. This enhances the voting mechanism. Allowing users to edit and delete their own comments gives them control over their contributions.

**Independent Test**: A logged-in user can add a comment to a topic, see their comment appear immediately, edit their own comment, delete their own comment, and view all comments from other users on that topic.

**Acceptance Scenarios**:

1. **Given** a user is logged in and viewing a topic, **When** they add a comment and submit it, **Then** their comment appears in the comments section with their name and timestamp
2. **Given** a topic has multiple comments, **When** a user views that topic, **Then** they see all comments in chronological order (oldest first)
3. **Given** a user is on mobile, **When** they add or view comments, **Then** the comment interface is optimized for mobile with readable text and easy input
4. **Given** a user has created a comment, **When** they click edit on their own comment, **Then** they are taken to a dedicated edit page (not a modal) where they can modify the comment
5. **Given** a user is editing their comment on a dedicated page, **When** they submit the changes, **Then** they are returned to the topic page with their updated comment displayed, and the browser back button works seamlessly
6. **Given** a user has created a comment, **When** they click delete on their own comment, **Then** a confirmation modal appears (AlpineJS), and after confirmation, the comment is removed via HTMX

---

### User Story 5 - Suggest, Edit, and Delete Presenters (Priority: P3)

A logged-in user can suggest a person who could present a topic. They can provide either an email address, a URL (such as LinkedIn profile), or a full name. Multiple presenter suggestions can be associated with a single topic. Users can edit and delete their own presenter suggestions.

**Why this priority**: Presenter suggestions help event organizers identify potential speakers, but this is less critical than the core topic voting and commenting functionality. Allowing users to edit and delete their own suggestions gives them control over their contributions.

**Independent Test**: A logged-in user can add a presenter suggestion to a topic by providing at least one of: email, URL, or full name. The suggestion appears associated with that topic. The user can edit and delete their own suggestions.

**Acceptance Scenarios**:

1. **Given** a user is viewing a topic, **When** they suggest a presenter with an email address, **Then** the suggestion is saved and displayed with the topic
2. **Given** a user suggests a presenter, **When** they provide a LinkedIn URL, **Then** the URL is stored and displayed as a clickable link
3. **Given** a user suggests a presenter, **When** they provide only a full name, **Then** the suggestion is saved with just the name
4. **Given** multiple presenter suggestions exist for a topic, **When** a user views that topic, **Then** they see all suggested presenters
5. **Given** a user has created a presenter suggestion, **When** they click edit on their own suggestion, **Then** they are taken to a dedicated edit page (not a modal) where they can modify the suggestion
6. **Given** a user is editing their presenter suggestion on a dedicated page, **When** they submit the changes, **Then** they are returned to the topic page with their updated suggestion displayed, and the browser back button works seamlessly
7. **Given** a user has created a presenter suggestion, **When** they click delete on their own suggestion, **Then** a confirmation modal appears (AlpineJS), and after confirmation, the suggestion is removed via HTMX

---

### User Story 6 - Readonly Experience for Non-Authenticated Users (Priority: P2)

Non-authenticated users can view topics, vote counts, comments, and presenter suggestions in a readonly mode. When they attempt to interact (vote, comment, add topic, suggest presenter), a popup appears inviting them to sign in or sign up via Google or LinkedIn SSO.

**Why this priority**: Allowing non-authenticated viewing increases discoverability and engagement. The popup mechanism provides a clear path to authentication without blocking content discovery.

**Independent Test**: A non-authenticated user can view topics, see vote counts and comments, and when clicking interactive buttons, receives a sign-in prompt popup.

**Acceptance Scenarios**:

1. **Given** a non-authenticated user is viewing topics, **When** they see the topics list, **Then** they can read all topic information (title, description, vote count, comments, presenter suggestions)
2. **Given** a non-authenticated user clicks a vote button, **When** the button is clicked, **Then** a popup appears inviting them to sign in or sign up
3. **Given** a non-authenticated user clicks "Add Topic", **When** the link is clicked, **Then** a popup appears inviting them to sign in or sign up
4. **Given** a non-authenticated user clicks a comment button, **When** the button is clicked, **Then** a popup appears inviting them to sign in or sign up
5. **Given** a non-authenticated user is on mobile, **When** they view topics or receive sign-in popups, **Then** the experience is optimized for mobile devices

---

### User Story 7 - Switch Between Events (Priority: P2)

A logged-in user can switch between different events using an event selector. Each event has its own URL slug (e.g., floripatalks/python-floripa). When switching events, users see topics specific to that event.

**Why this priority**: While starting with one event, the system must support multiple events from the beginning. Users need a way to navigate between events.

**Independent Test**: A user can access different event pages via their slug URLs and see topics specific to each event. The event selector allows switching between available events.

**Acceptance Scenarios**:

1. **Given** multiple events exist, **When** a user navigates to an event's slug URL, **Then** they see topics for that specific event
2. **Given** a user is viewing one event, **When** they use the event selector to switch to another event, **Then** they see topics for the newly selected event
3. **Given** a user is on mobile, **When** they switch events, **Then** the event selector is accessible and easy to use on mobile devices

---

### Edge Cases

- What happens when a user tries to add a topic with an empty title? The system should prevent submission and show an inline error message below the title field using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR).
- What happens when a user exceeds character limits? The system uses HTML5 native validation and/or vanilla JS for real-time character count, prevents submission when limit is reached, shows an inline error message below the field indicating the limit using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR), and HTMX handles form submission with server-side validation.
- What happens when a user tries to add more than 3 presenter suggestions to a topic? The system should prevent the addition and show an inline error message using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) indicating the per-user limit.
- What happens when a topic already has 10 presenter suggestions? The system should prevent new suggestions and show an inline error message using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) indicating the topic has reached the maximum number of suggestions.
- How does the system handle duplicate topics? Users can create topics with similar titles, but the system should allow this (admins can manage duplicates via admin interface).
- What happens when a user tries to vote multiple times on the same topic? The system prevents duplicate votes and shows the user has already voted.
- How does the system handle very long topic titles or comments? Text should be displayed with appropriate truncation or wrapping for readability on mobile devices.
- How should the system format large numbers in display (e.g., vote counts > 1000, many comments)? The system uses simple formatting in Portuguese (pt-BR) conventions (e.g., "1.234 votos", "567 comentários") without abbreviations like "1.2k". This maintains clarity and aligns with pt-BR number formatting standards.
- What happens when a user suggests a presenter with invalid email format or broken URL? The system accepts the input but does not validate format (admins can review and clean up via admin interface).
- How does the system handle users who are not logged in? Non-authenticated users can view topics in readonly mode but cannot vote, comment, add topics, or suggest presenters. When they click interactive buttons/links, a popup appears inviting them to sign in or sign up.
- What happens when an event has no topics? The event page displays an empty state message encouraging users to add the first topic.
- How does infinite scroll handle loading states? The system loads 20 topics per batch, uses HTMX native loading indicators (hx-indicator) while fetching additional topics, and handles end-of-list gracefully when all topics are loaded. AlpineJS may be used for custom loading states if needed.
- How does the system handle event switching when a user has unsaved changes (e.g., typing a comment)? The system should warn users about unsaved changes or auto-save draft content.
- What happens when two users edit the same content (topic/comment/suggestion) simultaneously? The system uses last-write-wins approach (no locking). The last user to save their changes overwrites previous changes. This simple approach aligns with HTMX's fast update pattern and is acceptable for MVP. Optional: system may warn user if content changed since they loaded the edit page.
- What happens when SSO authentication fails (provider unavailable, user cancels, network error)? The system displays an inline error message using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) explaining the issue and provides a retry option without losing context.
- How does the system handle editing of user content? Users can edit their own topics, comments, and presenter suggestions on dedicated pages (not modals). The browser back button works seamlessly, and HTMX is used to minimize page refreshes during transitions.
- How does the system handle language and localization? The primary interface is in Portuguese (pt-BR) with timezone set to São Paulo, but the system supports internationalization for future language expansion.
- What happens when a user deletes their content? Content is soft-deleted (marked as deleted with is_deleted flag), hidden from regular users immediately, but remains in the database and is recoverable by admins via Django admin interface.
- What happens when a user exceeds rate limits? The system prevents the action (topic creation, comment submission) and displays an inline error message using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) indicating the rate limit and when they can try again (e.g., "Você atingiu o limite de 10 tópicos por hora. Tente novamente em X minutos").
- How does the system handle network failures during HTMX requests (timeout, connection lost, server unavailable)? The system displays an inline error message using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) with a retry button. The retry button uses HTMX to retry the failed request, allowing recovery without page reload.
- What happens when a user's session expires during an action (vote, comment, edit)? The system redirects the user to the login page. After successful authentication, the system returns the user to the original context and automatically executes the intended action (vote, comment submission, edit save). This preserves user context and allows completion of the intended action.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to authenticate via Google SSO
- **FR-002**: System MUST allow users to authenticate via LinkedIn SSO
- **FR-021**: System MUST handle SSO authentication failures by displaying inline error messages using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) with retry options
- **FR-003**: System MUST display a list of topics for a selected event, ordered by vote count (descending), then by creation date (oldest first) for ties, showing topic title, vote count, and comment count
- **FR-022**: System MUST implement infinite scroll for topics list, loading 20 topics per batch as user scrolls down
- **FR-004**: System MUST allow logged-in users to create new topics with a title (max 200 characters) and optional description (max 2000 characters)
- **FR-038**: System MUST automatically generate a unique slug for each topic from its title (using django.utils.text.slugify), ensuring uniqueness within the event (add numeric suffix if duplicate)
- **FR-039**: System MUST keep topic slugs immutable after creation (slug does not change when title is edited, preserving URL stability and shared links)
- **FR-026**: System MUST allow logged-in users to edit their own topics
- **FR-027**: System MUST allow logged-in users to delete their own topics (soft delete - content is marked as deleted and hidden from users but recoverable by admins)
- **FR-005**: System MUST allow logged-in users to vote on topics (one vote per user per topic)
- **FR-023**: System MUST allow logged-in users to un-vote (remove their vote) on topics they have voted on
- **FR-006**: System MUST display vote counts for each topic
- **FR-007**: System MUST allow logged-in users to add comments to topics (max 1000 characters per comment)
- **FR-024**: System MUST allow logged-in users to edit their own comments
- **FR-025**: System MUST allow logged-in users to delete their own comments (soft delete - content is marked as deleted and hidden from users but recoverable by admins)
- **FR-008**: System MUST display comments with commenter name and timestamp, ordered chronologically (oldest first)
- **FR-009**: System MUST allow logged-in users to suggest presenters for topics by providing email, URL, or full name, with a limit of 3 suggestions per user per topic and 10 total suggestions per topic
- **FR-028**: System MUST allow logged-in users to edit their own presenter suggestions
- **FR-029**: System MUST allow logged-in users to delete their own presenter suggestions (soft delete - content is marked as deleted and hidden from users but recoverable by admins)
- **FR-010**: System MUST display presenter suggestions associated with topics, ordered chronologically (oldest first)
- **FR-011**: System MUST support multiple events, each with a unique URL slug
- **FR-012**: System MUST allow users to switch between events using an event selector. Use HTMX-first approach: native HTML select with hx-get/hx-trigger to load content when event is selected. AlpineJS only if explicitly requested.
- **FR-013**: System MUST display topics specific to the selected event
- **FR-014**: System MUST provide Django admin interface for admins to manage topics, comments, presenter suggestions, users, and events
- **FR-036**: System MUST implement soft delete for topics, comments, and presenter suggestions (marked as deleted, hidden from regular users, recoverable by admins)
- **FR-037**: System MUST implement rate limiting to prevent abuse: maximum 10 topics per hour per user, maximum 20 comments per hour per user
- **FR-040**: System MUST display error messages inline below the relevant field/area using semantic HTML (`<div role="alert">` or similar) in Portuguese (pt-BR) for accessibility and progressive enhancement
- **FR-041**: System MUST handle concurrent edits using last-write-wins approach (no locking). The last user to save changes overwrites previous changes. Optional: system may warn user if content changed since edit page was loaded.
- **FR-042**: System MUST handle network failures during HTMX requests (timeout, connection lost, server unavailable) by displaying inline error messages using semantic HTML (`<div role="alert">`) in Portuguese (pt-BR) with a retry button. The retry button uses HTMX to retry the failed request.
- **FR-043**: System MUST handle session expiration during actions (vote, comment, edit) by redirecting to login, then after authentication returning to original context and automatically executing the intended action.
- **FR-044**: System MUST format large numbers in display (vote counts, comment counts) using simple Portuguese (pt-BR) formatting conventions (e.g., "1.234 votos", "567 comentários") without abbreviations like "1.2k".
- **FR-015**: System MUST be mobile-first, with all functionality accessible and usable on mobile devices
- **FR-016**: System MUST meet accessibility standards (WCAG 2.1 Level AA compliance)
- **FR-017**: System MUST allow non-authenticated users to view topics but require authentication for voting, commenting, adding topics, and suggesting presenters
- **FR-030**: System MUST display popups inviting non-authenticated users to sign in or sign up when they click interactive buttons/links (vote, comment, add topic, suggest presenter). Use HTMX-first approach: HTMX to load a sign-in modal fragment from the server. AlpineJS only if explicitly requested.
- **FR-031**: System MUST provide edit functionality on dedicated pages (not modals/popups) for topics, comments, and presenter suggestions
- **FR-032**: System MUST ensure browser back button works seamlessly when navigating to and from edit pages
- **FR-033**: System MUST use HTMX to minimize page refreshes for all transitions, maintaining smooth user experience
- **FR-034**: System MUST have primary interface in Portuguese (pt-BR) with timezone set to São Paulo (America/Sao_Paulo)
- **FR-035**: System MUST support internationalization (i18n) for future language support
- **FR-018**: System MUST prevent users from voting multiple times on the same topic
- **FR-019**: System MUST display an empty state when an event has no topics
- **FR-020**: System MUST handle event switching and maintain user context appropriately

### Key Entities *(include if feature involves data)*

- **Event**: Represents a recurring event series (e.g., Python Floripa). Inherits from `BaseModel` (provides UUID v6 id, created_at, updated_at). Has a name, slug for URL, and optional description. Can have multiple topics associated with it.
- **Topic**: Represents a suggested talk topic for an event. Inherits from `SoftDeleteModel` (provides UUID v6 id, created_at, updated_at, is_deleted). Has a title (max 200 characters), slug (auto-generated from title using django.utils.text.slugify, unique per event), optional description (max 2000 characters), vote count, creator. Belongs to one event. Can have multiple comments and presenter suggestions. Soft-deleted topics are hidden from regular users but visible to admins.
- **Vote**: Represents a user's vote on a topic. Inherits from `BaseModel` (provides UUID v6 id, created_at, updated_at). Links a user to a topic. Each user can have only one vote per topic.
- **Comment**: Represents a user's comment on a topic. Inherits from `SoftDeleteModel` (provides UUID v6 id, created_at, updated_at, is_deleted). Has text content (max 1000 characters), author. Belongs to one topic. Soft-deleted comments are hidden from regular users but visible to admins.
- **Presenter Suggestion**: Represents a suggested presenter for a topic. Inherits from `SoftDeleteModel` (provides UUID v6 id, created_at, updated_at, is_deleted). Has either an email address, URL, or full name (at least one required). Belongs to one topic. Limited to 3 suggestions per user per topic and 10 total suggestions per topic. Soft-deleted suggestions are hidden from regular users but visible to admins.
- **User**: Represents an authenticated user. Has authentication information from SSO provider (Google or LinkedIn), display name, and account creation timestamp. Can create topics, vote, comment, and suggest presenters.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete topic creation in under 30 seconds on a mobile device
- **SC-002**: Users can view and browse topics list on mobile devices with 100% functionality (no desktop-only features)
- **SC-003**: 95% of users successfully complete voting on a topic on their first attempt
- **SC-004**: All interactive elements meet WCAG 2.1 Level AA accessibility standards
- **SC-005**: Users can switch between events in under 2 seconds
- **SC-006**: System supports at least 1000 topics per event without performance degradation
- **SC-007**: 90% of users can add a comment to a topic without assistance
- **SC-008**: Event pages load and display topics in under 2 seconds on mobile devices
- **SC-009**: Admin users can manage all content types (topics, comments, suggestions, users, events) via Django admin interface
- **SC-010**: System maintains responsive layout and functionality across mobile screen sizes from 320px to 768px width
- **SC-011**: Non-authenticated users can view topics and receive sign-in prompts in under 1 second on mobile devices
- **SC-012**: Users can edit their own content (topics, comments, suggestions) on dedicated pages with seamless back button navigation
- **SC-013**: All page transitions using HTMX complete without full page refreshes, maintaining smooth user experience
- **SC-014**: System displays content in Portuguese (pt-BR) with correct timezone (America/Sao_Paulo) formatting for dates and times

## Assumptions

- Users have Google or LinkedIn accounts for SSO authentication
- Event organizers will use Django admin for content management and moderation
- Topics do not require approval before appearing in the list (admins can remove inappropriate content)
- Presenter suggestions are informational only and do not require validation or contact
- The system starts with one event (Python Floripa) but architecture supports multiple events from launch
- Mobile-first means the interface is designed for mobile but works on desktop
- Pure CSS library will be used for styling. HTMX for server-driven interactions, AlpineJS for client-side state management (popups, toggles, form validation feedback)
- Users can edit and delete their own topics, comments, and presenter suggestions
- Editing occurs on dedicated pages (not modals) to ensure mobile-friendliness and proper browser navigation
- HTMX is used for all page transitions to minimize refreshes and provide smooth user experience
- Primary interface language is Portuguese (pt-BR) with timezone America/Sao_Paulo, but system supports i18n for future expansion
- Vote counts are displayed in real-time but do not require WebSocket connections (HTMX polling or page refresh is acceptable)
- Deletion uses soft delete pattern: content is marked with is_deleted flag (indexed field), hidden from regular users, but recoverable by admins. Django ORM managers filter by is_deleted=False by default.
