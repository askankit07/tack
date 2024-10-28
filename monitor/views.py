import threading
import time
from django.http import JsonResponse
import psutil
from django.core.mail import send_mail
import json
from datetime import datetime

def send_alert_email():
    subject = "CPU Usage Alert"
    message = "Warning: CPU usage exceeded 10%."
    from_email = "askankit07@gmail.com"
    recipient_list = ["askankit07@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)

def monitor_cpu_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)

        try:
            with open('config.json', 'r') as config_file:
                config_data = json.load(config_file)
                cpu_limit = config_data.get("cpu_limit", 10)  
        except (FileNotFoundError, json.JSONDecodeError):
            cpu_limit = 10  

        if cpu_usage > cpu_limit:
            send_alert_email()

        # Sleep for a while before checking again
        time.sleep(5) 

def get_system_info(request):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": cpu_usage,
        "ram_usage": memory_info.percent,
    }

    return JsonResponse(data)

#CPU monitoring thread when the application starts
threading.Thread(target=monitor_cpu_usage, daemon=True).start()
