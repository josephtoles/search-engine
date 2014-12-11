from datetime import timedelta, tzinfo

#####################
# TIMEZONE HANDLING #
#####################

DELTA_ZERO = timedelta(0)


class UTC(tzinfo):

    def utcoffset(self, dt):
        return DELTA_ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return DELTA_ZERO
