import json
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    baseurl: str
    name: str
    headers: dict[str, str]


def clear_playlist(config: Config, idx: str) -> dict:
    req = urllib.request.Request(
        f"{config.baseurl}/playlists/{idx}/items",
        headers=config.headers,
        method="DELETE",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlists(config: Config) -> dict:
    req = urllib.request.Request(f"{config.baseurl}/playlists/all", headers=config.headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlist(config: Config, idx: str) -> dict:
    req = urllib.request.Request(
        f"{config.baseurl}/playlists/{idx}/items",
        headers=config.headers,
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_server_id(config: Config) -> dict:
    req = urllib.request.Request(f"{config.baseurl}/identity", headers=config.headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def add_to_playlist(config: Config, idx: str, server_id: str, playqueue_ids: list[int]):
    query_params = f"uri=server://{server_id}/com.plexapp.plugins.library/library/metadata/{','.join(playqueue_ids)}"
    req = urllib.request.Request(
        f"{config.baseurl}/playlists/{idx}/items?{query_params}",
        headers=config.headers,
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
    config = Config(
        baseurl=sys.argv[1],
        name=sys.argv[3],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Plex-Token": sys.argv[2],
        },
    )
    server_id = get_server_id(config)

    playlist_id = get_playlist_id(config, config.name)
    if not playlist_id:
        print(f"Playlist not found: {config.name}")
        exit(1)

    playlist = get_playlist(config, playlist_id)
    if playlist["MediaContainer"]["smart"]:
        print(f"Can only sort dumb playlist, this one is smart: {config.name}")
        exit(1)

    sort_playlist(playlist)
    playqueue_ids = [item["ratingKey"] for item in playlist["MediaContainer"]["Metadata"]]

    clear_playlist(config, playlist_id)
    result = add_to_playlist(
        config,
        playlist_id,
        server_id["MediaContainer"]["machineIdentifier"],
        playqueue_ids,
    )
    print(result)


if __name__ == "__main__":
    main()
