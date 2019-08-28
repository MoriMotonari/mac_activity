from snapshot import AppSnapshot
import datetime

class ProcessNotOverError(ValueError):
    """Custom error for processes which are being serialized, but not over yet."""
    pass

class ProcessClosedError(ValueError):
    """Custom error for processes which are being closed, but already are closed."""
    pass

class Process:
    def __init__(self, name: str, url: str, is_frontmost: bool):
        # str(ns_app.localizedName())
        self.name = name
        # str(ns_app.bundleURL())
        self.url = url
        # ns_app.isActive()
        self.frontmost = is_frontmost
        # datetime instance of start time
        self.start = self.round_second(datetime.datetime.now())
        # duration in seconds
        self.duration = 0
        # if process is over
        self.over = False

    @classmethod
    def from_NSApp(cls, ns_app):
        return cls(str(ns_app.localizedName()), str(ns_app.bundleURL()), ns_app.isActive())

    @staticmethod
    def round_second(dt: datetime.datetime):
        if round(dt.microsecond / 1000000) == 1:
            return dt + datetime.timedelta(microseconds = 1000000 - dt.microsecond)
        else:
            return dt - datetime.timedelta(microseconds = dt.microsecond)
        
    @staticmethod
    def format_datetime(dt: datetime.datetime):
        datetime.datetime.strptime(data['analysis']['datetime'], "%Y-%m-%d %H:%M:%S")

    def close(self):
        if self.over():
            raise ProcessClosedError('This closed Process can not be closed again.')
        end_rounded = self.round_second(datetime.datetime.now())
        delta = end_rounded - self.start
        assert delta.microseconds == 0
        self.duration = delta.days * 24 * 3600 + delta.seconds
        self.over = True
    
    def calc_end(self):
        if not self.over:
            raise ProcessNotOverError('This Process has to be closed before calculation of end.')
        return self.start + datetime.timedelta(seconds=duration)

    def serialize(self):
        if not self.over:
            raise ProcessNotOverError('This Process has to be closed before serialization.')

        return json.dumps({
            'name': self.name,
            'url': self.url,
            'frontmost': self.frontmost,
            'start': self.format_datetime(self.start),
            'delta_seconds': self.duration
        })