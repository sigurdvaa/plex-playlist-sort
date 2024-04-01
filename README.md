# plex-playlist-sort
Sorts list items alphabetically by title, updates the non-smart playlist in-place.

`Usage: plex-playlist-sort.py <Plex Hostname | URL> <Access Token> <Playlist Title>`

- `Plex Hostname`: Hostname of the server. Can also include protocol and port. Example: `plex.example.com`
- `Access token`: API token, used with the header X-Plex-Token. Token can be found by opening any library item -> Get Info -> View XML. The token will be visible in the URL as a query parameter.
- `Playlist Title`: the given display name of the playlist. First match will be selected. Case-sensitive.
