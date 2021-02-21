import time
import os
import subprocess

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def on_created(event):
    """
    On created event handler.
    useful attribute: event.src_path

    :param event: event
    """
    command = 'rsync -Parvzh * shi-on@68.129.239.249:/Users/shi-on/Downloads/d'
    # subprocess.system(command)
    subprocess.call(['ls', '-lah'])
    subprocess.call(['rsync', '-Parvzh', '*', 'shi-on@68.129.239.249:/Users/shi-on/Downloads/d'])


def on_deleted(event):
    """
    On deleted event handler.
    useful attribute: event.src_path

    :param event: event
    """
    pass


def on_modified(event):
    """
    On modified event handler.
    useful attribute: event.src_path

    :param event: event
    """
    pass


def on_moved(event):
    """
    On moved event handler.
    useful attributes: event.src_path, event.dest_path

    :param event: event
    """
    pass


if __name__ == '__main__':

    event_handler = PatternMatchingEventHandler(patterns='*',
                                                ignore_patterns='',
                                                ignore_directories=False,
                                                case_sensitive=True)
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    observer = Observer()
    observer.schedule(event_handler=event_handler,
                      path='./buffer',
                      recursive=True)

    observer.start()
    print('Observer started...')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nObserver stopped\n')
        observer.stop()
        observer.join()
