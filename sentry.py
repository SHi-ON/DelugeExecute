import datetime
import logging
import os
import pathlib
import re
import shutil
import subprocess
import time
from configparser import ConfigParser
from typing import List, Union

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

JUNK_FILE_NAMES = [
    # RARBG
    'rarbg.txt',
    'rarbg_do_not_mirror.exe',
    'torrent downloaded from rarbg.to.txt',
    # YTS
    'www.yts.re.jpg',
    'www.yts.mx.jpg',
    'www.yts.am.jpg',
    'ytsproxies.com.txt',
    'ytsyifyup... (tor).txt',
]

SUBTITLE_DIR_NAMES = ['subs', 'subtitle', 'subtitles']
SUBTITLE_LANGUAGE = 'english'

VIDEO_EXTENSIONS = ['.mp4', '.mkv']

CATEGORY_SHOW = 'show'
CATEGORY_MOVIE = 'movie'
CATEGORY_TRANQUILITY = 'tranquility'
PATTERN_SHOW = re.compile(r'(\.S[0-9]{2}\.)|(\.S[0-9]{2}E[0-9]{2}\.)',
                          re.IGNORECASE)
PATTERN_TRANQUILITY = re.compile(r'\.X{3}\.',
                                 re.IGNORECASE)


def is_valid(file_name: str):
    return file_name.lower() not in JUNK_FILE_NAMES and \
        not file_name.endswith('.nfo')


def is_subtitle_dir(dir_name: str):
    return dir_name.lower() in SUBTITLE_DIR_NAMES


def _delete_junk_file(file_path: pathlib.Path):
    if not is_valid(file_path.name):
        file_path.unlink()
    if file_path.is_dir() and not any(file_path.iterdir()):
        file_path.rmdir()


def delete_junks(dir_path: pathlib.Path):
    if not dir_path.is_dir():
        _delete_junk_file(dir_path)
        return
    for fp in dir_path.iterdir():
        _delete_junk_file(fp)


def discover_subtitles_dir(dir_path: pathlib.Path):
    for fp in dir_path.iterdir():
        if fp.is_dir() and is_subtitle_dir(fp.name):
            return fp


def discover_subtitle_file(dir_path: pathlib.Path):
    for sfp in sorted(dir_path.iterdir()):
        if SUBTITLE_LANGUAGE in sfp.stem.lower():
            return sfp


def discover_video_file(dir_path: pathlib.Path):
    for fp in sorted(dir_path.iterdir()):
        if fp.suffix.lower() in VIDEO_EXTENSIONS:
            return fp


def move_subtitles(dir_path: pathlib.Path, category: str):
    if not dir_path.is_dir():
        return
    if not (subtitles_dir_path := discover_subtitles_dir(dir_path)):
        logging.warning('subtitles directory not found!')
        return

    if category == CATEGORY_SHOW:
        for dp in subtitles_dir_path.iterdir():
            if not dp.is_dir():
                continue
            subtitle_path = discover_subtitle_file(dp)
            t_subtitle_path = subtitle_path.with_stem(dp.name)
            subtitle_path.rename(dir_path / t_subtitle_path.name)
            shutil.rmtree(dp)
    elif category == CATEGORY_MOVIE:
        if not (video_file_path := discover_video_file(dir_path)):
            logging.warning('video file were not found!')
            return
        if not (
                subtitle_file_path := discover_subtitle_file(
                    subtitles_dir_path)):
            logging.warning('subtitle file not found!')
            return

        t_subtitle_file_path = subtitle_file_path.with_stem(
            video_file_path.stem)
        subtitle_file_path.rename(t_subtitle_file_path)
        t_subtitle_file_path.rename(dir_path / t_subtitle_file_path.name)

    shutil.rmtree(subtitles_dir_path)


def get_year_index(name_fields: List[str]):
    for i, field_ in enumerate(name_fields):
        try:
            datetime.datetime.strptime(field_, '%Y')
            return i
        except ValueError:
            continue


def format_dir_name(dir_path: Union[str, pathlib.Path], category: str):
    dir_path = pathlib.Path(dir_path)

    name_fields = dir_path.name.split('.')
    if category == CATEGORY_SHOW:
        return dir_path
    elif category == CATEGORY_MOVIE:
        if not (year_index := get_year_index(name_fields)):
            logging.warning('year string not found!')
            return dir_path
        name = ' '.join(name_fields[:year_index])
        year = name_fields[year_index]
        target_dir_path = dir_path.with_name(f'{name} ({year})')

        dir_path.rename(target_dir_path)
        return target_dir_path
    elif category == CATEGORY_TRANQUILITY:
        try:
            xxx_index = dir_path.name.lower().split('.').index('xxx')
        except ValueError:
            logging.warning(f'misclassified as {CATEGORY_TRANQUILITY}')
            return dir_path
        studio_name = name_fields[0]
        video_name = ' '.join(name_fields[4: xxx_index])
        target_dir_path = dir_path.with_name(f'{studio_name} - {video_name}')

        dir_path.rename(target_dir_path)
        return target_dir_path
    else:
        target_dir_path = dir_path
        return target_dir_path



def classify(dir_path: Union[str, pathlib.Path]):
    dir_path = pathlib.Path(dir_path)

    if PATTERN_SHOW.search(dir_path.name):
        return CATEGORY_SHOW
    elif get_year_index(dir_path.name.lower().split('.')):
        return CATEGORY_MOVIE
    elif PATTERN_TRANQUILITY.search(dir_path.name):
        return CATEGORY_TRANQUILITY


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
    def __init__(self, source_path, user, host, port, dest_path):
        self.source_path = source_path
        self.user = user
        self.host = host
        self.port = port
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

    def rsync_files(self, source: Union[str, pathlib.Path]):
        source_path = str(source)
        destination_path = f'{self.user}@{self.host}:{self.dest_path}'
        ssh_command = f'ssh -p {self.port}'
        args = ['rsync', '-Parvzh', '-e', ssh_command, source_path, destination_path]
        return subprocess.call(args)

    def on_created(self, event):
        """
        On created event handler.
        useful attribute: event.src_path

        :param event: event
        """
        source_path = pathlib.Path(event.src_path)
        category = classify(source_path)

        source_path = format_dir_name(source_path, category)
        move_subtitles(source_path, category)
        delete_junks(source_path)

        ret = self.rsync_files(source_path)
        if ret == 0:
            try:
                shutil.rmtree(source_path)
            except NotADirectoryError:
                os.remove(source_path)

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


def main():
    config_parser = ConfigParser()
    config_parser.read('config.env')
    configs = config_parser.items(section='sync')
    configs = dict(configs)
    sync = Sync(**configs)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sync.close()


if __name__ == '__main__':
    main()
