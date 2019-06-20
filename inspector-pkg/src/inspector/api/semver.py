class SemVer:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return "{}.{}.{}".format(self.major, self.minor, self.patch)

    def __eq__(self, other):
        if not isinstance(other, SemVer):
            return False

        return self.major == other.major and self.minor == other.minor and self.patch == other.patch
