# voicemail-fallback

Backup voicemail script for Filip's SignalWire voicemail line. SignalWire fetches
`vm.xml` (GET) only when its own LaML bin fails to load (its `call_fallback_url`),
so callers can still leave a message during a SignalWire outage. Recordings land in
SignalWire as usual, where the Voicemail app reads them. No secrets here.
