from datetime import date, datetime, timedelta
import pytz


class Ordertime:

    @classmethod
    def _parse24h(cls, string):
        try:
            return datetime.strptime(string, "%I:%M").time()
        except ValueError:
            return None

    @classmethod
    def _parse12h(cls, string):
        try:
            return datetime.strptime(string, "%H:%M").time()
        except ValueError:
            return None

    @classmethod
    def _parse12h_ampm(cls, string):
        try:
            return datetime.strptime(string, "%H:%M %p").time()
        except ValueError:
            return None

    @classmethod
    def parse_time(cls, string, tzstring):
        input_time = cls._parse24h(string) or cls._parse12h(string) or cls._parse12h_ampm(string)
        if not input_time:
            raise ValueError("Unrecognized date format {}, accept format is 'hh:mm [am/pm]'".format(string))
        result_dttm_naive = datetime.combine(date.today(), input_time)
        timezone = pytz.timezone(tzstring)
        return timezone.localize(result_dttm_naive)

    @classmethod
    def parse_interval(cls, amount, unit, tzstring):
        amount = int(amount)
        time_now = datetime.now()
        delta = None
        if unit in {"hours", "hour", "h"}:
            delta = timedelta(hours=amount)
        elif unit in {"mins", "min", "m"}:
            delta = timedelta(minutes=amount)
        elif unit in {"secs", "sec", "s"}:
            delta = timedelta(seconds=amount)
        else:
            raise ValueError("Unrecognized time unit format {}, accept format is [h]our(s)/[m]inute(s)/[s]econd(s)")

        result_dttm_naive = time_now + delta
        timezone = pytz.timezone(tzstring)
        return timezone.localize(result_dttm_naive)
