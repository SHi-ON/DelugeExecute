import os
import sched
import subprocess
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def rsync_files(file_name=None):
    file_path = file_name or 'buffer'

    args = ['sudo',
            'rsync',
            '--remove-source-files',
            '-Parvzh',
            file_path,
            'shi-on@70.18.8.224:~/Downloads/d']
    subprocess.call(args)


def remove_residues(file_name):
    global scheduler

    total_size = sum(os.path.getsize(f)
                     for f in os.listdir(file_name))
    if total_size > 500_000:
        scheduler.enter(300, 1, remove_residues,
                        kwargs={'file_name': file_name})
        return

    if file_name:
        args = ['rm',
                '-rf',
                file_name]
        subprocess.call(args)
        print('files removed:', file_name)
    else:
        print('cannot remove files:', file_name)


def on_created(event):
    """
    On created event handler.
    useful attribute: event.src_path

    :param event: event
    """
    global scheduler

    scheduler.enter(150, 1, rsync_files,
                    kwargs={'file_name': event.src_path})
    print('rsync scheduled:', event.src_path)
    scheduler.enter(750, 1, remove_residues,
                    kwargs={'file_name': event.src_path})
    print('remove remaining files scheduled:', event.src_path)

    scheduler.run()


def on_deleted(event):
    """
    On deleted event handler.
    useful attribute: event.src_path

    :param event: event
    """
    print('delete event captured on', event.src_path)


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
