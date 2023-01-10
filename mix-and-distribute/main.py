import fire
import logging, sys

def commands(command_str="create,mix,distribute", path='./test_folder', log_level='INFO'):
  logger = logging.getLogger()
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
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  log_file_handle.setFormatter(formatter)
  log_console_handle.setFormatter(formatter)
  
  # add the handlers to the logger
  logger.addHandler(log_file_handle)
  logger.addHandler(log_console_handle)
  
  logger.debug('command_str %s', command_str)
  logger.warning('path %s', path)
  logger.warning('log level %s', log_level)
  return

if __name__ == '__main__':
  fire.Fire(commands)
