# plex-sort-playlist
- https://plexapi.dev/docs/plex/playlists

Get all playlists
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/all
```
Get playlist
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/12345
```
Get playlist items
```
curl -H "X-Plex-Token: *********" -H "Accept: application/json" https://plex.example.com/playlists/12345/items
```

- can clear the list, and add the sorted items back:
  - PUT https://plex.example.com/playlists/59983/items?uri=server://c09c5ac6a7100f6d4100948506db992561e651be/com.plexapp.plugins.library/library/metadata/59769,59768,59772
- can move items in the list:
  - PUT https://plex.sigtown.lan/playlists/59983/items/6446/move?after=6445
    - drop "after=" param to move to top
