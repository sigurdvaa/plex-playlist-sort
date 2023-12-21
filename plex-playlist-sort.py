import json
import sys
from dataclasses import dataclass
from http.client import HTTPConnection, HTTPSConnection
from typing import Any, Optional, Union


@dataclass
class Config:
    conn: Union[HTTPConnection, HTTPSConnection]
    title: str
    headers: dict[str, str]


def get_playlist(config: Config, idx: str) -> Any:
    config.conn.request("GET", f"/playlists/{idx}/items", headers=config.headers)
    response = config.conn.getresponse()
    return json.loads(response.read())


def get_playlist_id(config: Config) -> Optional[str]:
    playlists = get_playlists(config)
    for container in playlists.values():
        for playlist in container["Metadata"]:
            if playlist["title"] == config.title and isinstance(playlist["ratingKey"], str):
                return playlist["ratingKey"]
    return None


def get_playlists(config: Config) -> Any:
    config.conn.request("GET", "/playlists/all", headers=config.headers)
    response = config.conn.getresponse()
    return json.loads(response.read())


def sorted_playlist_items(playlist: Any) -> list[int]:
    playlist["MediaContainer"]["Metadata"].sort(
        key=lambda x: x["title"][4:] if x["title"].lower().startswith("the ") else x["title"],
    )
    return [item["playlistItemID"] for item in playlist["MediaContainer"]["Metadata"]]


def update_playlist_order(config: Config, idx: str, items: list[int]) -> None:
    query = ""
    for i, item in enumerate(items):
        if i > 0:
            query = f"?after={items[i - 1]}"
        config.conn.request(
            "PUT",
            f"/playlists/{idx}/items/{item}/move{query}",
            headers=config.headers,
        )
        response = config.conn.getresponse()
        response.read()
        print(f"\rSorted {i + 1} of {len(items)} items...", end="")
    print()


def main() -> None:
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <Plex Hostname | URL> <Access Token> <Playlist Title>")
        exit(1)

    url = sys.argv[1]
    port: Optional[int] = None
    if ":" in url:
        port = int(url.split(":")[1])
    if url.startswith("http://"):
        conn = HTTPConnection(url[7:], port or 80)
    elif url.startswith("https://"):
        conn = HTTPSConnection(url[8:], port or 443)
    else:
        conn = HTTPSConnection(url, port or 443)

    config = Config(
        title=sys.argv[3],
        headers={
            "Accept": "application/json",
            "X-Plex-Token": sys.argv[2],
        },
        conn=conn,
    )

    playlist_id = get_playlist_id(config)
    if not playlist_id:
        print(f"Playlist not found: '{config.title}'")
        exit(1)
    print(f"Playlist found: '{config.title}'")

    playlist = get_playlist(config, playlist_id)
    if playlist["MediaContainer"]["smart"]:
        print(f"Can't sort smart playlist: '{config.title}'")
        exit(1)

    playlist_items = sorted_playlist_items(playlist)
    update_playlist_order(config, playlist_id, playlist_items)
    print("Done")


if __name__ == "__main__":
    main()
