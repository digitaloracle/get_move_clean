import os
import re
import logging
from matchmaker import matchshows
import win32file

logging.basicConfig(filename='cleaner.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
del_folders_re = re.compile('(Subs|Sample)')
mkv_re = re.compile('(mkv|avi)')


def get_folders(abs_path):
    for f in os.listdir(abs_path):
        if os.path.isdir(os.path.join(abs_path, f)):
            yield os.path.normpath(f)


class FolderContent:
    def __init__(self, abs_path):
        self.path = str(abs_path)
        self.contains = list()

    @property
    def isempty(self):
        for fi in os.listdir(self.path):
            self.contains.append(os.path.join(self.path, fi))
        if len(self.contains) == 0:
            return True
        else:
            return False

    def __str__(self):
        return str(self.path)

    def delete(self):
        try:
            os.rmdir(self.path)
        except Exception as e:
            raise e


class FileContent:
    def __init__(self, abs_path):
        self.path = str(abs_path)
        self.ext = str(self.path.split('.')[-1:])

    def __str__(self):
        return self.path

    def delete(self):
        try:
            os.remove(self.path)
        except Exception as e:
            raise e

    @property
    def isdelete(self):
        if re.search(mkv_re, self.ext):
            return False
        else:
            return True

    @property
    def __len__(self):
        return len(self.path)


if __name__ == '__main__':
    mypath = 'G:\\uTorrent Downloads'
    folders = list()
    files = list()
    for folder in get_folders(mypath):
        if os.path.isdir(os.path.join(mypath, folder)):
            folders.append(FolderContent(os.path.join(mypath, folder)))

    for f in folders:
        _folder = FolderContent(f)
        if _folder.isempty:
            logging.info('deleted: %s' % _folder)
            _folder.delete()
        else:
            for content in _folder.contains:
                if os.path.isdir(content):
                    folders.append(FolderContent(content))
                elif os.path.isfile(content):
                    files.append(FileContent(content))
    for f in files:
        if f.isdelete:
            logging.info('deleting %s' % f)
            f.delete()
        else:
            file_name = os.path.basename(f.path)
            dest = matchshows(file_name)
            logging.info('moving %s to %s' % (f, dest))
            try:
                win32file.MoveFile(f.path, os.path.join(dest, file_name))
            except Exception as e:
                logging.error(e)

