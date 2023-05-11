from django.apps import AppConfig
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import psutil
import threading
import time
from django.template.loader import render_to_string


class WebsiteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.website"

    def ready(self):
        refresh_resources()

# DELETE THIS
# Example of how to send only from server to client.
# DEMO: Every 2 seconds send CPU and RAM.
def refresh_resources(cpu_history=[], ram_history=[]):
    time.sleep(1)
    my_channel_layer = get_channel_layer()
    cpu_history_limit = cpu_history
    if my_channel_layer:
        # CPU
        total_cpu = psutil.cpu_percent()
        cpu_history.append(
            {
                "label": total_cpu,
                "value": total_cpu / 100,
                "color": "red"
                if total_cpu > 80
                else "yellow"
                if total_cpu > 50
                else "green",
            }
        )
        cpu_history_limit = cpu_history if len(cpu_history) < 10 else cpu_history[1:10]
        cpu_html = render_to_string(
            "components/_cpu_bars.html", {"items": cpu_history_limit}
        )
        # Render
        data = {"action": "Update CPU", "selector": "#cpu", "html": cpu_html}
        async_to_sync(my_channel_layer.group_send)(
            "broadcast", {"type": "send_data_to_frontend", "data": data}
        )
    threading.Thread(target=refresh_resources, args=(cpu_history_limit, [])).start()
