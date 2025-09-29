# API Reference

## Authentication

### `POST /api/auth/register`
Create a new applicant account.

### `POST /api/auth/token`
Obtain a JWT access token using email and password credentials.

## Evaluations

### `POST /api/evaluations/trigger`
Invoke a GPT-5 holistic evaluation for the authenticated applicant. Stores scores, narrative summary, and auto-generated suggestions.

### `GET /api/evaluations/`
List evaluation history for the authenticated applicant.

## Essays

### `POST /api/essays/`
Upload a new essay draft.

### `POST /api/essays/{essay_id}/critique`
Request an AI critique for a specific essay draft.

## Suggestions

### `GET /api/suggestions/`
Retrieve current improvement recommendations.

### `POST /api/suggestions/{suggestion_id}/acknowledge`
Mark a recommendation as acknowledged.

## Milestones

### `GET /api/milestones/`
Return planner milestones linked to evaluations and recommendations.
