from fuzzywuzzy import process
import os

shows_folder = 'G:\\Tv Shows'


def get_folders(abs_path):
    for f in os.listdir(abs_path):
        if os.path.isdir(os.path.join(abs_path, f)):
            yield os.path.normpath(f)


class MatchError(BaseException):
    pass


def matchshows(filename):
    try:
        show_names = get_folders(shows_folder)
        choice = process.extractOne(filename, show_names, score_cutoff=80)[0]
        return os.path.join(shows_folder, choice)
    except TypeError as te:
        raise MatchError('couldnt match %s' % filename)

if __name__ == '__main__':
    print matchshows('Shameless US S06E03 HDTV x264-LOL[ettv]')