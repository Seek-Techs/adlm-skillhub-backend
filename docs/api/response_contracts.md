# API Response Contract Table

## Envelope standard
- Success envelopes should use:
  ```json
  { "message": "optional", "data": { ... } }
  ```
- Error envelopes should use:
  ```json
  { "error": "..." }
  ```

## Endpoint contract table

| Endpoint | Method | Success shape | Error shape |
|---|---|---|---|
| `/auth/register/` | `POST` | `{ "message": "User registered, check email" }` | `{ "error": <serializer_or_message> }` |
| `/auth/verify/<uidb64>/<token>/` | `GET` | `{ "message": "Email verified successfully" }` | `{ "error": "Invalid token" \| "Invalid verification link" }` |
| `/auth/token/` | `POST` | `{ "data": { "refresh": "...", "access": "..." } }` | `{ "error": <validation_detail> }` |
| `/auth/refresh/` | `POST` | `{ "data": { "access_token": "..." } }` | `{ "error": "refresh_token is required" \| "Invalid refresh token" \| "Token refresh failed" }` |
| `/auth/api/forum-posts/` | `GET/POST` | `{ "data": <paginated_list_or_created_resource> }` | { "error": <validation_or_permission_detail> } |
| `/auth/api/forum-posts/<id>/` | `GET/PUT/PATCH/DELETE` | `{ "data": <resource_or_empty> }` | { "error": <validation_or_permission_detail> } |
| `/auth/api/job-listings/` | `GET/POST` | `{ "data": <paginated_list_or_created_resource> }` | { "error": <validation_or_permission_detail> } |
| `/auth/api/job-listings/<id>/` | `GET/PUT/PATCH/DELETE` | `{ "data": <resource_or_empty> }` | { "error": <validation_or_permission_detail> } |
| `/auth/api/analytics/summary/` | `GET` | `{ "data": { "daily_active_users": ..., ... } }` | `{ "error": "Failed to retrieve analytics" }` |
| `/ai/search/` | `GET` | `{ "data": [ ... ] }` | `{ "error": "..." }` |
| `/ai/predictive/` | `GET` | `{ "data": { "forecasted_engagement": ... } }` | { "error": <detail> } |

## Notes
- Success envelopes are normalized under `data` (and optional `message`) across the listed endpoints.
- Error responses are normalized under the `error` key, including DRF validation/permission details wrapped by the global exception handler.
