# plex-sort-playlist
## Usage
`Usage: plex-playlist-sort.py <Plex URL> <Access Token> <Playlist Title>`

- Plex URL: URL to the server. Example: `https://plex.example.com`
- Access token: API token, used with the header X-Plex-Token. Token can be found by opening any library item -> Get Info -> View XML. The token will be visible in the URL as a query parameter.
- Playlist Title: The given display name of the playlist. First match will be selected. Case-sensitive.
