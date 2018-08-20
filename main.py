import sys
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

    rsync_scheduler = RsyncScheduler(3)
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
