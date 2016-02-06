from plexapi.server import PlexServer


def refresh_plex():
    """refreshes local plex library."""
    plex = PlexServer()   # Defaults to localhost:32400
    plex.library.refresh()

if __name__ == '__main__':
    refresh_plex()


