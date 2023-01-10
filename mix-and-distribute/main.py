import fire
import logging, sys, os, shutil, random, pathlib

logger = logging.getLogger()

def init_logger(log_level):
  #logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  # file handler which logs even debug messages
  log_file_handle = logging.FileHandler('mix-and-disribute.log', mode='w')
  log_file_handle.setLevel(logging.DEBUG)

  # console handler with a user log level
  log_console_handle = logging.StreamHandler(sys.stdout)
  numeric_log_level = getattr(logging, log_level.upper(), None)
  if not isinstance(numeric_log_level, int):
      raise ValueError('Invalid log level: %s' % log_level)
  log_console_handle.setLevel(numeric_log_level)

  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
  log_file_handle.setFormatter(formatter)
  log_console_handle.setFormatter(formatter)

  # add the handlers to the logger
  logger.addHandler(log_file_handle)
  logger.addHandler(log_console_handle)
  return

def random_filename(in_path):
  return in_path + '/tempfile_' + str(random.randrange(10000)).zfill(5)

def create_files(create, in_path):
  if os.path.isdir(in_path):
    logger.debug('Removing folder %s', in_path)
    shutil.rmtree(in_path)

  logger.debug('Creating new folder %s', in_path)
  pathlib.Path(in_path).mkdir(parents=True)

  logger.debug('Generating file names')
  random.seed(a=None, version=2)

  n = 0
  filenames = []
  while n < create:
    filename = random_filename(in_path)
    if filename not in filenames:
      filenames.append(filename)
      n = n + 1

  for i in range(create):
    with open(filenames[i], "w") as file:
      file.write('Temp text in'+ filenames[i])
      logger.debug('Creating new file %s', filenames[i])

  return

def mix_files(in_path, mix):
  logger.debug('Listing files in %s', in_path)

  filenames = []
  for filename in os.listdir(in_path):
    logger.debug('Found file %s', filename)

    new_filename = ''
    while new_filename not in filenames:
      new_filename = random_filename(in_path)
      if new_filename not in filenames:
        filenames.append(new_filename)

    logger.debug('Renaming %s file into %s file', os.path.join(in_path, filename), new_filename)
    os.rename(os.path.join(in_path, filename), new_filename)

  return

def distribute_files(distribute, in_path, out_path):
  if os.path.isdir(out_path):
    logger.debug('Removing folder %s', out_path)
    shutil.rmtree(out_path)

  logger.debug('Listing files in %s', in_path)

  filenames = []
  for filename in os.listdir(in_path):
    logger.debug('Found file %s', filename)
    filenames.append(filename)

  n = len(filenames)//distribute + 1
  for i in range(n):
    foldername = out_path + '/folder_' + str(i).zfill(3)
    logger.debug('Creating folder %s', foldername)
    pathlib.Path(foldername).mkdir(parents=True)
    
    
    for j in range(distribute):
      if (len(filenames) > 0):
        logger.debug('Moving file %s in folder %s', filenames[0], foldername)
        os.rename(os.path.join(in_path, filenames[0]), os.path.join(foldername, filenames[0]))
        del filenames[0]

  return


def commands(create = 10, mix = True, distribute = 3, in_path='./input_folder', out_path='./test_folder', log_level='INFO'):
  init_logger(log_level)

  logger.info('Starting mix-and-disribute with loglevel = %s', log_level)
  logger.info('Creation params: create %s files with random names in %s folder', create, in_path)
  logger.info('Mix params: %s', 'with mixing' if mix else 'witout mixing')
  logger.info('Disribute params: saving new folders in %s folder', out_path)

  create_files(create, in_path)
  mix_files(in_path, mix)
  distribute_files(distribute, in_path, out_path)

  return

if __name__ == '__main__':
  fire.Fire(commands)
