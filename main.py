import sys
import json
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from custom_handler import RsyncSchedulingEventHandler
from rsync_scheduler import RsyncScheduler


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    # load config file
    with open('./config.json') as f:
        config = json.load(f)

    available_servers = config['servers']

    share_config = config['shares'][0]

    server_config = None
    for s in available_servers:
        if s['server-id'] == share_config['server']:
            server_config = s

    if server_config is None:
        exit(1)

    rsync_scheduler = RsyncScheduler(3,share_config, server_config)
    event_handler = RsyncSchedulingEventHandler(rsync_scheduler)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
