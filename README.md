# plex-sort-playlist
- https://plexapi.dev/docs/plex/playlists

Get all playlists
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/all
```
Get playlist
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/44206//playlists/44206/itemsitems
```
Playlist can be updated with PUT.
