from watchdog.events import FileSystemEventHandler
import os
import logging

class RsyncSchedulingEventHandler(FileSystemEventHandler):
    def __init__(self, rsync_scheduler):
        super().__init__()
        self.rsync_scheduler = rsync_scheduler
        # something more?

    def on_moved(self, event):
        # super(RsyncSchedulingEventHandler, self).on_moved(event)
        super().on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        if what is 'file':
            # get size
            size = os.path.getsize(event.dest_path)
            logging.info("Moved %s: from %s to %s, size %d", what, event.src_path,
                         event.dest_path, size)
            self.rsync_scheduler.update_syncsize(size)
            print(self.rsync_scheduler.buffered_syncsize)

    def on_created(self, event):
        # super(RsyncSchedulingEventHandler, self).on_created(event)
        super().on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        # super(RsyncSchedulingEventHandler, self).on_deleted(event)
        super().on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        # super(RsyncSchedulingEventHandler, self).on_modified(event)
        super().on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)
