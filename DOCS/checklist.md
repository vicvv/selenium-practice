CHECKLIST - BEFORE AUTOMATING AGAINST  DEV TARGET

Target: https://targeturl


NETWORK ACCESS

- [ ] Onsite: reachable directly, no VPN needed.
- [ ] Offsite: connect VPN FIRST, then run tests.
- [ ] Sanity check: can I open the URL in a normal Chrome window right now? (If yes, Selenium can reach it too.)


PERMISSION / POLICY (do this BEFORE pointing automation at it)

- [ ] Confirmed with the system owner  that automated Selenium traffic against the DEV instance is OK.
- [ ] Confirmed I'm only hitting DEV, never a production instance.
- [ ] Confirmed no sensitive/real data is at risk.


TEST ACCOUNT

- [ ] Have a dedicated TEST login (not my personal credentials).
- [ ] Confirmed whether login uses SSO / AD / Okta, and whether MFA is enforced (MFA is the hard part to automate).


CREDENTIALS SAFETY (never commit secrets)

- [ ] Credentials stored OUTSIDE the repo:
  - via environment variables, OR
  - a git-ignored config file (e.g. .env, listed in .gitignore).
- [ ] Double-checked .gitignore excludes any file holding secrets.
- [ ] If I ever paste a secret into a commit by accident: revoke/rotate it immediately (deleting the commit is NOT enough).


CERTIFICATES

- [ ] If the site shows "connection not private," plan to use Chrome option accept_insecure_certs (covered ~Module 8).


READY-TO-GO SIGNAL

- [ ] All boxes above ticked -> safe to write the first real test. Until then: keep practicing on public practice sites.