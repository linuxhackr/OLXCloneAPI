import urllib.request
import urllib.parse
from urllib.error import HTTPError

from django.conf import settings
from django.utils import timezone
import pytz
from pytz.exceptions import UnknownTimeZoneError
from django.core.mail import send_mail


def send_sms(number, otp):
    request = urllib.request.Request(
        "https://2factor.in/API/V1/9fe14c8c-c86e-11ea-9fa5-0200cd936042/SMS/+91" + number + "/" + otp + "/Gulloo")
    try:
        f = urllib.request.urlopen(request)
    except HTTPError:
        return False
    return True


def send_otp_email(email, otp):
    email_from = settings.EMAIL_HOST_USER
    subject = "Sauqna : OTP for password reset"
    message = f"""
Your one time OTP is {otp} , Please don't share with anyone.
"""
    send_mail(subject, message, email_from, [email, ])
    print("Email sent successfully!")


def get_local_datetime(datetime, tz: str = settings.TIME_ZONE):
    try:
        tz = pytz.timezone(tz)
    except UnknownTimeZoneError:
        tz = pytz.timezone(settings.TIME_ZONE)
    return datetime.astimezone(tz)


def get_time(time):
    if time is None:
        return ""

    now = get_local_datetime(timezone.now())
    time = get_local_datetime(time)

    diff = now - time

    if time.day == now.day:
        return time.strftime("%I:%M %p")

    if diff.days < 1:
        return time.strftime("%I:%M %p") + " YESTERDAY"

    if diff.days < 7:
        return time.strftime("%A")

    if diff.days >= 7 and diff.days < 365:
        return time.strftime("%d %B")

    if diff.days >= 365:
        return time.strftime("%m %b %Y")
