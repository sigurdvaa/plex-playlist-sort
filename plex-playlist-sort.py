import json
import sys
import urllib.request
import urllib.parse
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    baseurl: str
    token: str
    name: str


def clear_playlist(config: Config, idx: str) -> dict:
    headers = {
        "Accept": "application/json",
        "X-Plex-Token": config.token,
    }
    req = urllib.request.Request(
        config.baseurl + f"/playlists/{idx}/items",
        headers=headers,
        method="DELETE",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlists(config: Config) -> dict:
    headers = {
        "Accept": "application/json",
        "X-Plex-Token": config.token,
    }
    req = urllib.request.Request(config.baseurl + "/playlists/all", headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlist(config: Config, idx: str) -> dict:
    headers = {
        "Accept": "application/json",
        "X-Plex-Token": config.token,
    }
    req = urllib.request.Request(config.baseurl + f"/playlists/{idx}/items", headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_server_id(config: Config) -> dict:
    headers = {
        "Accept": "application/json",
        "X-Plex-Token": config.token,
    }
    req = urllib.request.Request(config.baseurl + "/identity", headers=headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def update_playlist(config: Config, idx: str, server_id: str, playlist: dict):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Plex-Token": config.token,
    }

    playqueue_ids = ",".join(
        [item["ratingKey"] for item in playlist["MediaContainer"]["Metadata"]],
    )
    params = {"uri": f"server://{server_id}", "playQueueID": playqueue_ids}
    query_params = urllib.parse.urlencode(params)

    req = urllib.request.Request(
        config.baseurl + f"/playlists/{idx}/items?{query_params}",
        headers=headers,
        method="PUT",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlist_id(config: Config, name: str) -> Optional[str]:
    playlists = get_playlists(config)
    for container in playlists.values():
        for playlist in container["Metadata"]:
            if playlist["title"] == name:
                return playlist["ratingKey"]
    return None


def sort_playlist(playlist: dict):
    playlist["MediaContainer"]["Metadata"].sort(key=lambda x: x["title"])


def main():
    config = Config(sys.argv[1], sys.argv[2], sys.argv[3])
    server_id = get_server_id(config)

    playlist_id = get_playlist_id(config, config.name)
    if not playlist_id:
        print(f"Playlist not found: {config.name}")
        exit(1)

    playlist = get_playlist(config, playlist_id)
    if playlist["MediaContainer"]["smart"]:
        print(f"Can only sort dumb playlist, this one is smart: {config.name}")
        exit(1)

    clear_playlist(config, playlist_id)
    sort_playlist(playlist)
    result = update_playlist(
        config,
        playlist_id,
        server_id["MediaContainer"]["machineIdentifier"],
        playlist,
    )
    print(result)


if __name__ == "__main__":
    main()
