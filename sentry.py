import os
import subprocess
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

SOURCE_PATH = 'buffer'
USER = 'shi-on'
HOST = '68.129.234.107'
DEST_PATH = '~/Downloads/buffer/'

DEBUG = True


def del_path(p):
    try:
        os.rmdir(p)
    except NotADirectoryError:
        os.remove(p)


def calculate_path_size(p):
    def __real_size(fp):
        return os.stat(fp).st_blocks * 512

    if os.path.isfile(p):
        return __real_size(p)
    p_size = 0
    for path, dirs, files in os.walk(p):
        for f in files:
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path):
                p_size += __real_size(file_path)
    return p_size


class Sync:
    def __init__(self, source_path, user, host, dest_path):
        self.source_path = source_path
        self.user = user
        self.host = host
        self.dest_path = dest_path
        self.observer = self.__init_observer()

    def __init_observer(self):
        # setting the event handler
        event_handler = PatternMatchingEventHandler(patterns='*',
                                                    ignore_patterns='',
                                                    ignore_directories=False,
                                                    case_sensitive=True)
        event_handler.on_created = self.on_created
        event_handler.on_deleted = self.on_deleted
        event_handler.on_modified = self.on_modified
        event_handler.on_moved = self.on_moved

        # schedule the observer
        observer = Observer()
        observer.schedule(event_handler=event_handler,
                          path=self.source_path,
                          recursive=False)

        observer.start()
        print('Observer started...')
        return observer

    def rsync_files(self, source):
        dest = f'{self.user}@{self.host}:{self.dest_path}'
        args = ['sudo',
                'rsync',
                '--remove-source-files',
                '-Parvzh',
                source,
                dest]
        subprocess.call(args)

    def on_created(self, event):
        """
        On created event handler.
        useful attribute: event.src_path

        :param event: event
        """
        source_path = event.src_path
        if '+-+' in source_path:
            path = event.src_path.split('+-+')[0]
            self.rsync_files(path)

    def on_deleted(self, event):
        """
        On deleted event handler.
        useful attribute: event.src_path

        :param event: event
        """
        pass

    def on_modified(self, event):
        """
        On modified event handler.
        useful attribute: event.src_path

        :param event: event
        """
        pass

    def on_moved(self, event):
        """
        On moved event handler.
        useful attributes: event.src_path, event.dest_path

        :param event: event
        """
        pass

    def close(self):
        self.observer.stop()
        self.observer.join()
        print('\nObserver stopped\n')


if __name__ == '__main__':
    sync = Sync(SOURCE_PATH, USER, HOST, DEST_PATH)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sync.close()
