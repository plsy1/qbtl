import time
from qbittorrentapi import Client
from qbittorrentapi.exceptions import NotFound404Error, APIConnectionError

def pause_and_resume_unregistered_torrents(qb_client):
    try:
        torrents = qb_client.torrents.info()

        for torrent in torrents:
            try:
                qb_client.torrents_trackers(torrent_hash=torrent.hash)
            except NotFound404Error:
                continue

            for tracker in torrent.trackers:
                if tracker.msg == "unregistered torrent":
                    size_gb = torrent.size / (1024**3)
                    if 14 < size_gb < 50:
                        print(f"Pausing torrent '{torrent.name}'")
                        torrent.pause()
                        print(f"Resuming torrent '{torrent.name}'")
                        torrent.resume()
                        break
                    else:
                        print(f"Deleting torrent '{torrent.name}' (Size: {size_gb:.2f} GB)")
                        torrent.delete(delete_files=True)
                        break
    except APIConnectionError as e:
        print(f"Connection to qBittorrent failed: {e}")


qb = Client(host='127.0.0.1:8080', port=8080, username='', password='')
qb.auth_log_in()

call_count = 0
while True:
    try:
        print("Start Running....")
        pause_and_resume_unregistered_torrents(qb)
        call_count += 1
        
        if call_count >= 100:
            print('Re-authentication......')
            qb.auth_log_in()
            call_count = 0
    except APIConnectionError as e:
        print(f"Connection to qBittorrent failed: {e}")

    time.sleep(5)

qb.auth_log_out()
