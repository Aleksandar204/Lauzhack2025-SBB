Project: Secure Public Transport Validation System

Short description
- This project provides a secure validation system for public-transport trips. It allows controllers (inspection devices) to validate digital travel cards using a challenge-response protocol with HMAC-SHA256, preventing replay and cloning attacks.

Key components
- `server/` : FastAPI backend that stores card/trip records in `cards.json`, validates card signatures, and provides endpoints to generate and check trips.
- `controller-app/` : Android app (controller side) that issues validation requests to the server and simulates card scanning. It contains simulated card logic and UI screens.
- `frontend/` : Simple web frontend for interacting with the service (demo/UX).

Security design (brief)
- Each card has a `secret_key` and a monotonic `counter` stored on the server.
- Validation uses a combined string (uid + challenge + counter) and computes a Base64 HMAC-SHA256 MAC using the card's secret. The controller provides the uid, counter, challenge, and mac to the server for verification.
- Server performs constant-time MAC comparison and checks the provided counter against its stored counter to prevent replay. On success, the server increments and persists the counter.

Usage
- Controllers call `/validate` with the `uid`, `counter`, `mac`, and `challenge` to verify a card.
- Trips can be generated with `/generate_trip` and checked with `/check`.

Goals
- Provide a small, auditable demonstration of secure card validation for public transport inspection.
- Make the system extensible for production features (secure secret storage, TLS enforcement, audit logs, rate limiting, and revocation).

Contact
- See repository root and `server/app.py` for implementation details and developer notes.