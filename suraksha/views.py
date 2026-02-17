from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from service import heat, att, alert, wait, newface


def stream(gen):
    return StreamingHttpResponse(
        gen(),
        content_type="multipart/x-mixed-replace; boundary=frame"
    )


# ================= HOME =================
# ================= HOME =================
def home(request):
    context = {
        "heat_alerts": list(reversed(heat.alerts[-10:])),
        "noentry_alerts": list(reversed(alert.alerts[-10:])),
        "wait_alerts": list(reversed(wait.alerts[-10:])),
        "attendance": att.get_attendance()
    }
    return render(request, "home.html", context)

# ================= REPORT API =================
def report_data(request):
    return JsonResponse({
        "heat": list(reversed(heat.alerts[-10:])),
        "noentry": list(reversed(alert.alerts[-10:])),
        "wait": list(reversed(wait.alerts[-10:])),
        "attendance": att.get_attendance()
    })



# ================= HEATMAP =================
def heatmap_page(request):
    if request.method == "POST":
        heat.update_settings(
            request.POST.get("decay"),
            request.POST.get("gain"),
            request.POST.get("high"),
            request.POST.get("low"),
        )
        return redirect("heatmap")

    return render(request, "heatmap.html", {
        "alerts": heat.alerts,
        "decay": heat.DECAY,
        "gain": heat.GAIN,
        "high": heat.HIGH_THRESHOLD,
        "low": heat.LOW_THRESHOLD,
    })


def heatmap_stream(request):
    return stream(heat.generate_frames)


# ================= ATTENDANCE =================
def attendance_page(request):
    return render(request, "att.html")


def attendance_stream(request):
    return stream(att.generate_frames)


def register_face(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            newface.register(name)
    return redirect("attendance")


def attendance_data(request):
    return JsonResponse(att.get_attendance(), safe=False)


# ================= ALERT =================
def alert_page(request):
    return render(request, "noentry.html")


def alert_stream(request):
    return stream(alert.generate_frames)


def alert_data(request):
    return JsonResponse(alert.alerts, safe=False)


def alert_get_config(request):
    boxes, threshold, bw, bh = alert.load_config()
    return JsonResponse({
        "boxes": boxes,
        "threshold": threshold,
        "bw": bw,
        "bh": bh
    })


@csrf_exempt
def alert_set_mode(request):
    data = json.loads(request.body)
    alert.CONFIG_MODE = data.get("config", False)
    return JsonResponse({"status": "ok"})


@csrf_exempt
def alert_config(request):
    if request.method == "POST":
        data = json.loads(request.body)

        boxes = data.get("boxes", [])
        threshold = int(data.get("threshold", 50))
        bw = float(data.get("bw", 0.2))
        bh = float(data.get("bh", 0.2))

        alert.save_config(boxes, threshold, bw, bh)
        return JsonResponse({"status": "saved"})

    return JsonResponse({"error": "invalid"})


# ================= WAIT =================
def wait_page(request):
    return render(request, "wait.html")


def wait_stream(request):
    return stream(wait.generate_frames)


def wait_data(request):
    return JsonResponse(wait.alerts, safe=False)


def wait_get_config(request):
    boxes, threshold, wait_time, bw, bh = wait.load_config()
    return JsonResponse({
        "boxes": boxes,
        "threshold": threshold,
        "wait_time": wait_time,
        "bw": bw,
        "bh": bh
    })


@csrf_exempt
def wait_set_mode(request):
    data = json.loads(request.body)
    wait.CONFIG_MODE = data.get("config", False)
    return JsonResponse({"status": "ok"})


@csrf_exempt
def wait_config(request):
    if request.method == "POST":
        data = json.loads(request.body)

        boxes = data.get("boxes", [])
        threshold = int(data.get("threshold", 1500))
        wait_time = float(data.get("wait_time", 2))
        bw = float(data.get("bw", 0.2))
        bh = float(data.get("bh", 0.2))

        wait.save_config(boxes, threshold, wait_time, bw, bh)
        return JsonResponse({"status": "saved"})

    return JsonResponse({"error": "invalid"})
@csrf_exempt
def wait_reset(request):
    wait.RESET_TRIGGER = True
    return JsonResponse({"status": "reset"})
