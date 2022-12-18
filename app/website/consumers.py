import os
from channels.generic.websocket import JsonWebsocketConsumer
from app.website.models import Client

# Load all actions
path = os.getcwd()
for entry in os.scandir(os.path.join(path, "app", "website", "actions")):
    if entry.is_file():
        name = entry.name.split(".")[0]
        exec(f"from app.website.actions import {name} as {name}")


class WebsiteConsumer(JsonWebsocketConsumer):
    def connect(self):
        """Event when client connects"""
        # Accept the connection
        self.accept()
        # Save the client
        Client.objects.create(channel_name=self.channel_name)

    def disconnect(self, close_code):
        """Event when client disconnects"""
        # Delete the client
        Client.objects.filter(channel_name=self.channel_name).delete()

    def receive_json(self, data_received):
        """
        Event when data is received
        All information will arrive in 2 variables:
        "action", with the action to be taken
        "data" with the information
        """
        # Get the data
        data = data_received if "data" in data_received else None
        # Depending on the action we will do one task or another.
        # Example: If the action is "home->search", we will call the function "actions.home.search" with the data
        if data and "action" in data:
            action_data = data["action"].split("->")
            if len(action_data) == 2:
                action = action_data[0].lower()
                function = action_data[1].lower()
                try:
                    eval(f"{action}.{function}(self, data)")
                except Exception as e:
                    print(f"Bad action: {data['action']}")
                    print(e)

    def send_html(self, data):
        """Event: Send html to client

        Example minimum data:
        {
            "action": "home->search",
            "selector": "#search-results",
            "html": "<h1>Example</h1>"
        }

        Example with optional data:
        {
            "action": "home->search",
            "selector": "#search-results",
            "html": "<h1>Example</h1>",
            "append": true, # Optional, default: false. If true, the html will be added, not replaced
            "url": "/search/results", # Optional, default: None. If set, the url will be changed
            "title": "Search results", # Optional, default: None. If set, the title will be changed
            "scroll": true # Optional, default: false. If true, the page will be scrolled to the selector
        }
        """
        if "selector" in data and "html" in data:
            # Required data
            my_data = {
                "action": data["action"],
                "selector": data["selector"],
                "html": data["html"],
            }
            # Optional data
            if "append" in data:
                my_data.update({"append": data["append"]})
            else:
                my_data.update({"append": False})
            if "url" in data:
                my_data.update({"url": data["url"]})
            if "title" in data:
                my_data.update({"title": data["title"]})
            if "scroll" in data:
                my_data.update({"scroll": data["scroll"]})
            # Send the data
            self.send_json(my_data)
