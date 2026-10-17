# voicemail-fallback

Backup voicemail script for Filip's SignalWire voicemail line. SignalWire fetches
`vm.xml` (GET) only when its own LaML bin fails to load (its `call_fallback_url`),
so callers can still leave a message during a SignalWire outage. Recordings land in
SignalWire as usual, where the Voicemail app reads them. No secrets here.

- Every fetch must be GET: GitHub Pages answers POST with 405. That covers the
  number's fallback method and the `Record` action to `done.xml`.
- It records straight away (no key gate), but otherwise mirrors the live bin: a 1 s
  pause before the greeting, 240 s max, `#` to finish, and no SignalWire
  transcription (billed; the Voicemail app transcribes the mp3 itself).
- Public repo: never put a phone number in it.
- Pushing to `main` is the deploy. Check with `python -m unittest discover tests`
  first, then read the files back from `https://filipvariciuc1.github.io/voicemail-fallback/`.
