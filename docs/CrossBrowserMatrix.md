# Cross-Browser Matrix

Definitions
- Full: Full manual pass + automated suites (API + UI).
- Smoke: Login + boards list/create + open board basic flow.

Sample:
- Chrome (latest): Full suite
- Firefox (latest): Full suite except drag-drop (workaround noted)
- Safari (latest): Smoke only (login, create board, viewer restriction)
- Mobile Safari/Chrome: Smoke only (login, create card)

| Browser | Depth | Notes |
| --- | --- | --- |
| Chrome (Desktop) | Full | Primary dev/test target |
| Firefox (Desktop) | Smoke | Automated E2E runs via Playwright |
| Safari (WebKit) | Smoke | Automated E2E runs via Playwright WebKit |
| Mobile (iOS/Android) | Smoke | Manual only; focus on login + boards view |

Automated E2E coverage by browser:
- Chromium: full E2E suite
- Firefox: full E2E suite
- WebKit: full E2E suite

Manual smoke checks recommended for mobile device emulation or real devices.
