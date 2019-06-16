class SemVer:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return "{}.{}.{}".format(self.major, self.minor, self.patch)
