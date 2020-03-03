import logging

from files.filemanager import FileManager
from utils.date import DateUtil

class Log:

    @classmethod
    def init(cls):
        logging.basicConfig(filename= FileManager.root + "\\latest.log", level=logging.DEBUG)

    @classmethod
    def info(cls, string):
        logging.info(" " + DateUtil.current_time + "  : " + string)

    @classmethod
    def debug(cls, string):
        logging.debug(" " + DateUtil.current_time + " : " + string)

    @classmethod
    def warning(cls, string):
        logging.warning(" " + DateUtil.current_time + " : " + string)