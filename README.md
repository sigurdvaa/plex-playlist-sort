# plex-sort-playlist
- https://plexapi.dev/docs/plex/playlists

Get all playlists
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/all
```
Get playlist
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/12345/items
```
Playlist can be updated with PUT.
