import time
import logging
from qbittorrentapi import Client
from qbittorrentapi.exceptions import NotFound404Error, APIConnectionError


logging.basicConfig(filename='tllog.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def pause_and_resume_unregistered_torrents(qb_client):
    try:
        torrents = qb_client.torrents.info()

        for torrent in torrents:
            try:
                qb_client.torrents_trackers(torrent_hash=torrent.hash)
            except NotFound404Error:
                continue

            for tracker in torrent.trackers:
                size_gb = torrent.size / (1024**3)
                if size_gb < 14:
                    logging.info(f"Deleting torrent '{torrent.name}' (Size: {size_gb:.2f} GB)")
                    torrent.pause()
                    torrent.delete(delete_files=True)
                    break;
                if size_gb > 50:
                    torrent.pause()
                    logging.info(f"Deleting torrent '{torrent.name}' (Size: {size_gb:.2f} GB)")
                    torrent.delete(delete_files=True)
                    break;
                if tracker.msg == "unregistered torrent":
                    logging.info(f"Pausing torrent '{torrent.name}'")
                    torrent.pause()
                    logging.info(f"Resuming torrent '{torrent.name}'")
                    torrent.resume()
                    break;
                else:
                    torrent.resume;
    
    except APIConnectionError as e:
        logging.error(f"Connection to qBittorrent failed: {e}")

qb = Client(host='127.0.0.1:8080', port=8080, username='fmk3325', password='3P2dAErvRdMMV5x')
qb.auth_log_in()

call_count = 0
while True:
    try:
        print("Start Running....")
        pause_and_resume_unregistered_torrents(qb)
        call_count += 1

        if call_count >= 100:
            logging.info('Re-authentication......')
            qb.auth_log_in()
            call_count = 0
    except APIConnectionError as e:
        logging.error(f"Connection to qBittorrent failed: {e}")

    time.sleep(5)

qb.auth_log_out()
