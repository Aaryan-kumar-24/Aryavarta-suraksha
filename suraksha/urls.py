from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # HOME
    path("", views.home, name="home"),

    # HEATMAP
    path("heatmap/", views.heatmap_page, name="heatmap"),
    path("heatmap/stream/", views.heatmap_stream, name="heatmap_stream"),

    # ATTENDANCE
    path("attendance/", views.attendance_page, name="attendance"),
    path("attendance/stream/", views.attendance_stream, name="attendance_stream"),
    path("attendance/data/", views.attendance_data, name="attendance_data"),
    path("register-face/", views.register_face, name="register_face"),

    # ALERT
    path("alert/", views.alert_page, name="alert"),
    path("alert/stream/", views.alert_stream),
    path("alert/data/", views.alert_data),
    path("alert/config/", views.alert_config),
    path("alert/get-config/", views.alert_get_config),
    path("alert/set-mode/", views.alert_set_mode),

    # WAIT
    path("wait/", views.wait_page, name="wait"),
    path("wait/stream/", views.wait_stream, name="wait_stream"),
    path("wait/data/", views.wait_data),
    path("wait/config/", views.wait_config),
    path("wait/get-config/", views.wait_get_config),
    path("wait/set-mode/", views.wait_set_mode),
    path("wait/reset/", views.wait_reset),

]
