class InvalidURLError(ValueError):
    """Custom Error for invalid Application bundleURLs"""
    pass

class AppSnapshot:
    def __init__(self, name: str, url: str, is_frontmost: bool):
        self.name = name
        self.url = url
        self.frontmost = is_frontmost
        if not self.has_file_url():
            raise InvalidURLError("URL doesn't start with 'file:///'")

    @staticmethod
    def from_NSApp(ns_app):
        return AppSnapshot(str(ns_app.localizedName()), str(ns_app.bundleURL()), ns_app.isActive())

    def is_finder(self):
        return self.url == "file:///System/Library/CoreServices/Finder.app/"

    def has_file_url(self):
        return self.url.startswith('file:///')

    def location_type(self):
        if self.url.startswith('file:///System/Library/'):
            return 'Library'
        elif self.url.startswith('file:///Applications/'):
            return 'Applications'
        else:
            return None

    def app_type(self):
        if '.app' in self.url:
            first_dotapp = self.url.index('.app')
            if '.app' in self.url[first_dotapp + len('.app'):]:
                return 'sub.app'
            else:
                return '.app'
        else:
            # '.app' not included in self.url
            return None

    def serialize(self):
        return json.dumps({
                 'name': self.name,
                  'url': self.url,
            'frontmost': self.frontmost
        })