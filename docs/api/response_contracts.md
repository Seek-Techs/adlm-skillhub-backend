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
| `/auth/api/forum-posts/` | `GET/POST` | `{ "data": <paginated_list_or_created_resource> }` | default DRF error payloads (to be normalized) |
| `/auth/api/forum-posts/<id>/` | `GET/PUT/PATCH/DELETE` | `{ "data": <resource_or_empty> }` | default DRF error payloads (to be normalized) |
| `/auth/api/job-listings/` | `GET/POST` | `{ "data": <paginated_list_or_created_resource> }` | default DRF error payloads (to be normalized) |
| `/auth/api/job-listings/<id>/` | `GET/PUT/PATCH/DELETE` | `{ "data": <resource_or_empty> }` | default DRF error payloads (to be normalized) |
| `/auth/api/analytics/summary/` | `GET` | `{ "data": { "daily_active_users": ..., ... } }` | `{ "error": "Failed to retrieve analytics" }` |
| `/ai/search/` | `GET` | `{ "data": [ ... ] }` | `{ "error": "..." }` |
| `/ai/predictive/` | `GET` | `{ "data": { "forecasted_engagement": ... } }` | default/explicit error payloads |

## Notes
- Success envelopes are now normalized for auth and major non-auth read/write paths above.
- Some validation/error paths still follow default DRF error payloads and can be normalized in a future pass.
- Clients should handle the `error` envelope where provided and tolerate DRF field-error maps where still applicable.
