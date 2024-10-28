from django.http import JsonResponse
import psutil
from django.core.mail import send_mail
import json
from datetime import datetime

def send_alert_email():
    subject = "CPU Usage Alert"
    message = "Warning: CPU usage exceeded 20%."
    from_email = "askankit07@gmail.com"
    recipient_list = ["askankit07@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)

def get_system_info(request):
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    data = {
        "timestamp": datetime.now().isoformat(),
        "cpu_usage": cpu_usage,
        "ram_usage": memory_info.percent,
    }

    try:
        with open('config.json', 'r') as config_file:
            config_data = json.load(config_file)
            cpu_limit = config_data.get("cpu_limit", 10)  
    except (FileNotFoundError, json.JSONDecodeError):
        cpu_limit = 10  

    # Send an email if CPU usage exceeds the defined limit
    if cpu_usage > cpu_limit:

        # Send the alert email
        send_alert_email()
        
    return JsonResponse(data)