import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer


def on_created(event):
    print(f"hey, {event.src_path} has been created!\n")


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!\n")


def on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified\n")


def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}\n")


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
                      path='.',
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
