import sched
import subprocess
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def on_created(event):
    """
    On created event handler.
    useful attribute: event.src_path

    :param event: event
    """
    global scheduler

    scheduler.enter(5, 1, rsync_files, kwargs={'file_name': event.src_path})
    scheduler.run()


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


def rsync_files(file_name=None):
    file_path = file_name or 'buffer'

    args = ['sudo',
	    'rsync',
	    '--remove-source-files',
            '-Parvzh',
            file_path,
            'shi-on@68.129.239.249:~/Downloads/d']
    subprocess.call(args)


if __name__ == '__main__':

    # setting the event handler
    event_handler = PatternMatchingEventHandler(patterns='*',
                                                ignore_patterns='',
                                                ignore_directories=False,
                                                case_sensitive=True)
    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    # schedule the observer
    observer = Observer()
    observer.schedule(event_handler=event_handler,
                      path='./buffer',
                      recursive=False)

    observer.start()
    print('Observer started...')

    scheduler = sched.scheduler(time.time, time.sleep)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nObserver stopped\n')
        observer.stop()
        observer.join()
