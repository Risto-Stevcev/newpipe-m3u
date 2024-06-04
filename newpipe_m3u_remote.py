import sqlite3
import sys
import urllib.request, json

if (len(sys.argv) < 2):
    raise FileNotFoundError('Usage: python newpipe_m3u.py path/to/newpipe.db')

db_path = sys.argv[1]

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query for playlists
playlists_query = "SELECT name, url FROM remote_playlists"
cursor.execute(playlists_query)

playlists = [
    (playlist_id[len('https://www.youtube.com/playlist?list='):], playlist_name)
    for (playlist_name, playlist_id) in cursor.fetchall()
]

for (playlist_id, playlist_name) in playlists:
    print(f"Processing {playlist_name}...")
    try:
        url = f'https://yt.drgnz.club/api/v1/playlists/{playlist_id}'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        streams = [
            (f"https://www.youtube.com/watch?v={video['videoId']}",
             f"{data['title']} - {video['title']}")
            for video in data['videos']
        ]

        # Create an M3U file for this playlist
        m3u_content = "#EXTM3U\n"
        for url, title in streams:
            m3u_content += f"#EXTINF:-1,{title}\n{url}\n"

        # Write to a file
        with open(f"{playlist_name.replace('/', '_')}.m3u", 'w', encoding='utf-8') as m3u_file:
            m3u_file.write(m3u_content)
    except:
        print("Failed")

# Close the database connection
conn.close()
