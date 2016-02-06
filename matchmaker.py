from fuzzywuzzy import process
import os

shows_folder = 'G:\\Tv Shows'


def get_folders(abs_path):
    """ Args:
            abs_path (str): the path of a directory
        Yields:
            os.path.normpath (str): normalized path of subfolders
    """
    for f in os.listdir(abs_path):
        if os.path.isdir(os.path.join(abs_path, f)):
            yield os.path.normpath(f)


class MatchError(BaseException):
    """ used for errors related no unsuccessful match """
    pass


def matchshows(filename):
    """ Args:
            filename (str): to the appropriate folder based on fuzzy hash matching
        Returns:
            str: path of the matching folder
        Raises:
            MatchError: if no match found
    """
    try:
        show_names = get_folders(shows_folder)
        choice = process.extractOne(filename, show_names, score_cutoff=80)[0]
        return os.path.join(shows_folder, choice)
    except TypeError:
        raise MatchError('couldnt match %s' % filename)


if __name__ == '__main__':
    print matchshows('Shameless US S06E03 HDTV x264-LOL[ettv]')