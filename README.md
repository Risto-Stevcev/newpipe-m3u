# newpipe-m3u

Convert newpipe backups to m3u format

## Usage

### Playlists

```
python newpipe_m3u.py /path/to/newpipe/backup/newpipe.db
```

### Remote playlists

```
python newpipe_m3u_remote.py /path/to/newpipe/backup/newpipe.db
```

## Why use this?

VLC can run playlists that point to youtube urls. Alternatively, you can choose
to convert it to whichever frontned you would use instead (ie: Invidious).

To keep a backup or port of your music in a straighforward and ubiquitous format
like m3u. Many streaming services, android players, etc, have their own
proprietary format and/or they don't give you the option to export.
