import sqlite3
import sys

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
    
    # Create an M3U file for this playlist
    m3u_content = "#EXTM3U\n"
    for url, title in streams:
        m3u_content += f"#EXTINF:-1,{title}\n{url}\n"
    
    # Write to a file
    with open(f"{playlist_name.replace('/', '_')}.m3u", 'w', encoding='utf-8') as m3u_file:
        m3u_file.write(m3u_content)

# Close the database connection
conn.close()
