from qbittorrentapi import Client
import time

def pause_and_resume_unregistered_torrents(qb_client):
    torrents = qb_client.torrents.info()

    for torrent in torrents:
        for tracker in torrent.trackers:
            if tracker.msg == "unregistered torrent":
                print(f"Pausing torrent '{torrent.name}'")
                torrent.pause()
                print(f"Resuming torrent '{torrent.name}'")
                torrent.resume()
                break;


# 连接到qBittorrent客户端

qb = Client(host='', port=8080, username='', password='')
qb.auth_log_in()


while True:
    print("----------Start----------")
    pause_and_resume_unregistered_torrents(qb)
    time.sleep(10)

# 退出
qb.auth_log_out()