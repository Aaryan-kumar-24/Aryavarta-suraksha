from django.apps import AppConfig
import threading


class ServiceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "service"

    def ready(self):
        from service.mailer import start_email_monitor

        threading.Thread(target=start_email_monitor, daemon=True).start()
