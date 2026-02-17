from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
import time

from service import heat, alert, wait

LAST_EMAIL_TIME = 0


def get_latest_alert():
    """
    Return ONLY alert type + time
    """
    current_time = datetime.now().strftime('%H:%M:%S')

    if heat.alerts:
        return f"🔥 Heatmap Crowd Alert detected at {current_time}"

    if alert.alerts:
        return f"🚫 Restricted Entry Alert detected at {current_time}"

    if wait.alerts:
        return f"⏳ Long Waiting Alert detected at {current_time}"

    return None


def send_alert_email(message):
    send_mail(
        subject="🚨 Farm Security Alert",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["skilldevelopnment@gmail.com"],
        fail_silently=False,
    )


def start_email_monitor():
    """
    Send email immediately on alert,
    then wait 60 seconds before next email.
    """
    global LAST_EMAIL_TIME

    while True:
        alert_message = get_latest_alert()
        current_time = time.time()

        if alert_message and (current_time - LAST_EMAIL_TIME > 60):
            print("🚨 Sending alert email:", alert_message)
            send_alert_email(alert_message)
            LAST_EMAIL_TIME = current_time

        time.sleep(2)
