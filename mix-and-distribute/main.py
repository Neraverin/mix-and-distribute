import fire
import logging
import sys
import os
import shutil
import random

logger = logging.getLogger()


def init_logger(log_level):
    # custom hndlers won't work without defaul logger configuration
    logger.setLevel(logging.DEBUG)

    log_file_handle = logging.FileHandler('mix-and-disribute.log', mode='w')
    log_file_handle.setLevel(logging.DEBUG)

    log_console_handle = logging.StreamHandler(sys.stdout)
    numeric_log_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    log_console_handle.setLevel(numeric_log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    log_file_handle.setFormatter(formatter)
    log_console_handle.setFormatter(formatter)

    logger.addHandler(log_file_handle)
    logger.addHandler(log_console_handle)


def random_filename(in_path, extension):
    return os.path.join(in_path, str(random.randrange(10000)).zfill(5) + extension)


def create_files(create, in_path):
    if (create == 0):
        return

    if os.path.isdir(in_path):
        logger.debug('Removing folder %s', in_path)
        shutil.rmtree(in_path)

    logger.debug('Creating new folder %s', in_path)
    os.makedirs(in_path)

    logger.debug('Generating file names')
    random.seed(a=None, version=2)

    n = 0
    filenames = []
    while n < create:
        filename = random_filename(in_path, '.jpg')
        if filename not in filenames:
            filenames.append(filename)
            n = n + 1

    for i in range(create):
        with open(filenames[i], "w", encoding='UTF-8') as file:
            file.write('Temp text in' + filenames[i])
            logger.debug('Creating new file %s', filenames[i])

    return


def mix_files(in_path, mix):
    if not mix:
        return

    logger.debug('Listing files in %s', in_path)

    filenames = []
    for filename in os.listdir(in_path):
        logger.debug('Found file %s', filename)
        extension = '.' + filename.split('.')[-1]

        new_filename = ''
        while new_filename not in filenames:
            new_filename = random_filename(in_path, extension)
            if new_filename not in filenames:
                filenames.append(new_filename)

        logger.debug('Renaming %s file into %s file', os.path.join(in_path, filename), new_filename)
        os.rename(os.path.join(in_path, filename), new_filename)

    return


def distribute_files(distribute, in_path, out_path):
    if (distribute == 0):
        return

    if os.path.isdir(out_path):
        logger.debug('Removing folder %s', out_path)
        shutil.rmtree(out_path)

    logger.debug('Listing files in %s', in_path)

    filenames = []
    for filename in os.listdir(in_path):
        logger.debug('Found file %s', filename)
        filenames.append(filename)

    if (len(filenames) == 0):
        logger.error('Folder %s is empty. No files to distribute', in_path)
        return

    n = len(filenames) // distribute + 1
    for i in range(n):
        foldername = os.path.join(out_path, 'folder_' + str(i).zfill(3))
        logger.debug('Creating folder %s', foldername)
        os.makedirs(foldername)

        for _ in range(distribute):
            if (len(filenames) > 0):
                logger.debug('Moving file %s in folder %s', filenames[0], foldername)
                os.rename(os.path.join(in_path, filenames[0]),
                          os.path.join(foldername, filenames[0]))
                del filenames[0]

    return


def commands(create=10, mix=True, distribute=3, in_path='./input_folder',
             out_path='./test_folder', log_level='INFO'):
    """Create or/and mix or/and distribute files in folders

    Parameters
    ----------
    create : int
      Number of test files you want to generate. Set to 0 to disable file generation.
    mix : boolean
      Mixing is renaming files to random names (to change file order).
    distribute : int
      How many files would be in every new created folder. Set to 0 to disable file distribution.
      Warning! File distribution is moving files in your filesystem.
    in_path : str
      Path used for file generator and file mixer. Could be relative.
    out_path : str
      Path used for creating new folders by file distributor.
    log_level: str
      Logging level (default python logger levels).
    """

    try:
        init_logger(log_level)

        logger.info('Starting mix-and-disribute with loglevel = %s', log_level)
        logger.info('Creation: create %s files with random names in %s folder', create, in_path)
        logger.info('Mix: %s', 'with mixing' if mix else 'witout mixing')
        logger.info('Disribute: saving folders with %s files in %s folder', distribute, out_path)

        create_files(create, in_path)
        mix_files(in_path, mix)
        distribute_files(distribute, in_path, out_path)

    except Exception as e:
        logger.error(e)


if __name__ == '__main__':
    fire.Fire(commands)
