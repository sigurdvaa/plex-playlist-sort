import json
import sys
import urllib.request
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Config:
    baseurl: str
    title: str
    headers: dict[str, str]


def get_playlist(config: Config, idx: str) -> Any:
    req = urllib.request.Request(
        f"{config.baseurl}/playlists/{idx}/items",
        headers=config.headers,
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def get_playlist_id(config: Config) -> Optional[str]:
    playlists = get_playlists(config)
    for container in playlists.values():
        for playlist in container["Metadata"]:
            if playlist["title"] == config.title and isinstance(playlist["ratingKey"], str):
                return playlist["ratingKey"]
    return None


def get_playlists(config: Config) -> Any:
    req = urllib.request.Request(f"{config.baseurl}/playlists/all", headers=config.headers)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def sort_playlist(playlist: Any) -> None:
    playlist["MediaContainer"]["Metadata"].sort(key=lambda x: x["title"])


def update_playlist_order(config: Config, idx: str, items: list[int]) -> None:
    query = ""
    for i, item in enumerate(items):
        if i > 0:
            query = f"?after={items[i - 1]}"

        req = urllib.request.Request(
            f"{config.baseurl}/playlists/{idx}/items/{item}/move{query}",
            headers=config.headers,
            method="PUT",
        )
        urllib.request.urlopen(req)
        print(f"Sorted {i + 1} of {len(items)} items...", end="\r")
    print()


def main() -> None:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <Plex URL> <Access Token> <Playlist Title>")
        exit(1)

    config = Config(
        baseurl=sys.argv[1],
        title=sys.argv[3],
        headers={
            "Accept": "application/json",
            "X-Plex-Token": sys.argv[2],
        },
    )

    playlist_id = get_playlist_id(config)
    if not playlist_id:
        print(f"Playlist not found: '{config.title}'")
        exit(1)
    print(f"Found Playlist '{config.title}'")

    playlist = get_playlist(config, playlist_id)
    if playlist["MediaContainer"]["smart"]:
        print(f"Can't sort smart playlist: '{config.title}'")
        exit(1)

    sort_playlist(playlist)
    playlist_items = [item["playlistItemID"] for item in playlist["MediaContainer"]["Metadata"]]

    update_playlist_order(config, playlist_id, playlist_items)
    print("Done")


if __name__ == "__main__":
    main()
