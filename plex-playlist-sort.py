import json
import sys
import urllib.request

baseurl = "https://plex.sigtown.lan"
headers = {
    "Accept": "application/json",
    "X-Plex-Token": sys.argv[1],
}

req = urllib.request.Request(baseurl + "/playlists/all", headers=headers)
with urllib.request.urlopen(req) as response:
    playlists = json.loads(response.read())
print(playlists)
