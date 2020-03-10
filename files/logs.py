import logging
import os

from zipfile import ZipFile
from files.filemanager import FileManager
from utils.date import DateUtil

class Log:

    @classmethod
    def init(cls):

        if os.path.exists(FileManager.logs + "\\latest.log"):
            cls.compressLatest()

        file = open(FileManager.logs + "\\latest.log", 'w+')
        file.write(DateUtil.getCurrentDate("%d_%m_%y") + "\n")

        logging.basicConfig(filename=FileManager.logs + "\\latest.log", level=logging.DEBUG)

    @classmethod
    def info(cls, string):
        logging.info(DateUtil.getCurrentDate("%H:%M:%S") + ": " + string)

    @classmethod
    def debug(cls, string):
        logging.debug(DateUtil.getCurrentDate("%H:%M:%S") + ": " + string)

    @classmethod
    def warning(cls, string):
        logging.warning(DateUtil.getCurrentDate("%H:%M:%S") + ": " + string)

    @classmethod
    def error(cls, string):
        logging.error(DateUtil.getCurrentDate("%H:%M:%S") + ": " + string)

    @classmethod
    def compressLatest(cls):

        count = 0

        with open(FileManager.logs + '\\latest.log') as latest:
            first_line = latest.readline()

        files = FileManager.get_all_file_paths(FileManager.root)

        while os.path.exists(FileManager.logs + '\\log_' + first_line[0:8] + '_' + str(count) + '.zip'):
            count += 1

        with ZipFile(FileManager.logs + '\\log_' + first_line[0:8] + '_' + str(count) + '.zip', 'w') as zip:
            for file in files:
                if "latest.log" in file:
                    zip.write(file, os.path.basename(file))

        if os.path.exists(FileManager.logs + '\\latest.log'):
            os.remove(FileManager.logs + '\\latest.log')

