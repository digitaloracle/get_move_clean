import os
import re
import logging
from matchmaker import matchshows, MatchError
import win32file
import json

logging.basicConfig(filename='cleaner.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
mkv_re = re.compile('(mkv|avi|mp4|iso|mp3|flac|m3u8|zip)$')


class FolderContent:
    """abstraction for folder object."""
    def __init__(self, abs_path):
        """
        receives path to folder and extracts relevant attributes.
        Args:
            abs_path (str): the absolute path to given folder
        """
        if os.path.isdir(abs_path):
            self.path = abs_path
        else:
            raise ValueError('%s is not a dir' % abs_path)

        self.files, self.folders = get_content(self.path)

    def __str__(self):
        """
        Returns:
            string of the given absolute path on init
        """
        return str(self.path)

    @property
    def isempty(self):
        """
        Returns:
            True if the folder contents is empty or
            False iotherwise
        """
        if len(self.folders) + len(self.files) == 0:
            return True
        else:
            return False

    def delete(self):
        """will delete given folder."""
        try:
            os.rmdir(self.path)
        except Exception as e:
            raise e


class FileContent:
    """abstraction for file object"""
    def __init__(self, abs_path):
        """receives path to file and extracts relevant attributes."""
        self.path = abs_path
        self.ext = os.path.splitext(self.path)[1]
        self.size = int(os.path.getsize(self.path) / (1024**2))
        self.base = os.path.basename(self.path)

    def __str__(self):
        return 'name=%s,deletable=%s,size=%d' % (self.base, self.isdelete, self.size)

    @property
    def json(self):
        """
        Returns:
            file object attributes in json format.
        """
        arr = {"name": os.path.basename(self.path), "isdelete": self.isdelete, "size": self.size}
        return json.dumps(arr, sort_keys=False)

    def delete(self):
        """deletes given file."""
        try:
            os.remove(self.path)
        except Exception as e:
            raise e

    @property
    def isdelete(self):
        """evaluate if file is safe to delete."""
        if re.search(mkv_re, self.ext):
            return False
        else:
            return True


def get_content(path):
    """
    Returns:
        list of files and list of dirs in given path.
    """
    folders = []
    files = []
    for content in os.listdir(path):
        cpath = os.path.join(path, content)
        if os.path.isdir(cpath):
            folders.append(FolderContent(cpath))
        elif os.path.isfile(cpath):
            files.append(FileContent(cpath))
    return files, folders


def clean():
    moved = False
    mypath = 'G:\\uTorrent Downloads'
    folders = list()
    files = list()

    for dir_ in FolderContent(mypath).folders:
        folders.append(dir_)

    for fol in folders:
        if fol.isempty:
            fol.delete()
        elif len(fol.folders) > 0:
            for f in fol.folders:
                folders.append(f)
        else:
            [files.append(f) for f in fol.files]

    for f in files:
        if f.isdelete:
            f.delete()
            logging.info('deleted %s' % f)
        else:
            try:
                dest = matchshows(f.base)
                logging.info('matched %s with %s' % (f.base, dest))
            except MatchError as me:
                logging.error(me)
                continue
            try:
                logging.info('moving %s to %s' % (f, dest))
                win32file.MoveFile(f.path, os.path.join(dest, f.base))
                moved = True
            except Exception as e:
                logging.error(e)
                if e[0] == 183:
                    f.delete()
                    logging.info('%s exists already, deleting duplicate' % f.base)
    return moved


if __name__ == '__main__':
    clean()
