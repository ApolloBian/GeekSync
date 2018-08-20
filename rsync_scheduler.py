import os

class RsyncScheduler():
    # sync download according 
    """
    threshold: unit in bytes
    """
    def __init__(self, schedule_size_threshold):
        # self.buffered_syncsize = 0
        self.schedule_size_threshold = schedule_size_threshold
        self.__buffered_syncsize = 0

    def update_syncsize(self, size):
        # self.buffered_syncsize = self.buffered_sync + size
        self.__buffered_syncsize += size
        if self.__buffered_syncsize > self.schedule_size_threshold:
            # schedule and update
            self.__buffered_syncsize = 0
            self.schedule_upsync()


    def schedule_upsync(self):
        # TODO: implememnt
        print("upsync scheduled")

    @property
    def buffered_syncsize(self):
        return self.__buffered_syncsize
