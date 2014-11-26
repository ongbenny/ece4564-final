calendarId = 'teamdanier@gmail.com'

import google_calendar
from datetime import tzinfo, timedelta, datetime
import pprint
import time as _time

STDOFFSET = timedelta(seconds = -_time.timezone)
if _time.daylight:
    DSTOFFSET = timedelta(seconds = -_time.altzone)
else:
    DSTOFFSET = STDOFFSET

ZERO = timedelta(0)
DSTDIFF = DSTOFFSET - STDOFFSET

class LocalTimezone(tzinfo):
    def utcoffset(self, dt):
        if self._isdst(dt):
            return DSTOFFSET
        else:
            return STDOFFSET

    def dst(self, dt):
        if self._isdst(dt):
            return DSTDIFF
        else:
            return ZERO

    def tzname(self, dt):
        return _time.tzname[self._isdst(dt)]

    def _isdst(self, dt):
        tt = (dt.year, dt.month, dt.day,
              dt.hour, dt.minute, dt.second,
              dt.weekday(), 0, 0)
        stamp = _time.mktime(tt)
        tt = _time.localtime(stamp)
        return tt.tm_isdst > 0


def getEvents(pageToken=None):
    events = google_calendar.service.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin=str(datetime.now(LocalTimezone()).isoformat('T')),
        timeMax='2015-11-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
    return events

# def calendar_events():
#     print "Events: "
#     events = getEvents()
#     while True:
#         for event in events['items']:
#             pprint.pprint(event)
#         page_token = events.get('nextPageToken')
#         if page_token:
#             events = getEvents(page_token)
#             print events
#         else:
#             break

# if __name__ == '__calendar_events__':
#     calendar_events()

events = getEvents()
while True:
    for event in events['items']:
        pprint.pprint(event['summary'])
        pprint.pprint(event['start'])
        print ''
    page_token = events.get('nextPageToken')
    if page_token:
        events = getEvents(page_token)
        print events
    else:
        break