from datetime import datetime


class DateUtil:
    now = datetime.now()

    @classmethod
    def getCurrentDate(cls, dateFormat):

        current_time = cls.now.strftime(dateFormat)
        return current_time
