import sqlite3
import sys
import json

if (len(sys.argv) < 2):
    raise FileNotFoundError('Usage: python newpipe_m3u.py path/to/newpipe.db')

db_path = sys.argv[1]

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query for playlists
playlists_query = "SELECT uid, name FROM playlists"
cursor.execute(playlists_query)
playlists = cursor.fetchall()

json_playlists = []

for playlist in playlists:
    playlist_id, playlist_name = playlist
    # Fetch streams associated with this playlist
    streams_query = """
    SELECT s.url, s.title
    FROM streams s
    JOIN playlist_stream_join psj ON s.uid = psj.stream_id
    WHERE psj.playlist_id = ?
    ORDER BY psj.join_index
    """
    cursor.execute(streams_query, (playlist_id,))
    streams = cursor.fetchall()

    # Create an piped.video playlists entry for this playlist
    json_playlists.append({
        'name': playlist_name, 'type': 'playlist', 'visibility': 'private',
        'videos': [url for (url, title) in streams]
    })

with open('playlists.json', 'w', encoding='utf-8') as file:
    json.dump(
        { 'format': 'Piped', 'version': 1, 'playlists': json_playlists },
        file,
        ensure_ascii=False,
        indent=4
    )

# Close the database connection
conn.close()
