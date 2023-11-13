import datetime

from ...osascript import OSAScript
from ...helper_bridging import OSAObjProxy

class Reminder(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)

    # properties
    @property
    def alarm(self) -> str:
        """Alarm of reminder."""
        return self._call_method('alarm')

    @alarm.setter
    def alarm(self, value: str):
        self._set_property('alarm', value)

    @property
    def alarm_string(self) -> str:
        """Name of sound, text to speak, text of alert/notification, source/path of script or recipient of email. Text can also contain placeholders."""
        return self._call_method('alarmString')

    @alarm_string.setter
    def alarm_string(self, value: str):
        self._set_property('alarmString', value)

    @property
    def day_of_week(self) -> str:
        """Scheduled day of week."""
        return self._call_method('dayOfWeek')

    @day_of_week.setter
    def day_of_week(self, value: str):
        self._set_property('dayOfWeek', value)

    @property
    def due_date(self) -> datetime.datetime:
        """Due date."""
        return self._get_property('dueDate')

    @due_date.setter
    def due_date(self, value: datetime.datetime):
        # TODO: Implement this
        raise NotImplementedError()

    @property
    def interval(self) -> int:
        """Interval of schedule (every n hours, days, weeks, months or years)"""
        return self._get_property('interval')

    @interval.setter
    def interval(self, value: int):
        self._set_property('interval', value)

    @property
    def masc(self) -> int:
        """Bitmap specifying scheduled days of week/month or scheduled months of year."""
        return self._get_property('masc')

    @masc.setter
    def masc(self, value: int):
        self._set_property('masc', value)

    @property
    def schedule(self) -> str:
        """Schedule of reminder."""
        return self._call_method('schedule')

    @schedule.setter
    def schedule(self, value: str):
        self._set_property('schedule', value)

    @property
    def week_of_month(self) -> str:
        """Scheduled week of month."""
        return self._call_method('weekOfMonth')

    @week_of_month.setter
    def week_of_month(self, value: str):
        self._set_property('weekOfMonth', value)
