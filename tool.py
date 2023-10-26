from qbittorrentapi import Client
import time

def pause_and_resume_unregistered_torrents(qb_client):
    torrents = qb_client.torrents.info()

    for torrent in torrents:
        for tracker in torrent.trackers:
            if tracker.msg == "unregistered torrent":
                size_gb = torrent.size / (1024**3)
                if 14 < size_gb < 50:
                    print(f"Pausing torrent '{torrent.name}'")
                    torrent.pause()
                    print(f"Resuming torrent '{torrent.name}'")
                    torrent.resume()
                    break;
                else:
                    print(f"Deleting torrent '{torrent.name}' (Size: {size_gb:.2f} GB)")
                    torrent.pause()
                    torrent.delete(delete_files=True)
                    break;

qb = Client(host='127.0.0.1:8080', port=8080, username='', password='')
qb.auth_log_in()


while True:
    print("----------Start----------")
    pause_and_resume_unregistered_torrents(qb)
    time.sleep(5)
