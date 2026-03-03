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

## Notes
- Non-auth endpoints currently include mixed legacy/raw payloads and should be normalized in future PRs.
- Clients should handle `error` envelope consistently for all auth failures.
