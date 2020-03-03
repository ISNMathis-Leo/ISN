from datetime import datetime

class DateUtil:

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")