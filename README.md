# Django template for creating a complete HTML over the Wire site

This template has an example of the most common cases.

- Navigation Real-time without loads similar to SPA.
- Server-Side Rendering (SSR) of pages for SEO (Using `views.py`).
- Multilanguage.
- Switch to a static page (Home).
- Switch to a dynamic page (List of cats 🐈🐈🐈🐈🐈🐈).
- Single page (Cat 🐈).
- Add a new item in the database (👶🏻🐈).
- Delete item from the database (🐈☠).
- Update item from the database (🐈👉🐕).
- Broadcast: Sending information to all customers in Real-time (Feline notifications 🐈📢).
- Navigator whose active button changes dynamically.
- Contact form with validations.
- Get file from a client (🐈🖼️).
- Login.
- Private Page (🐈‍⬛).
- Get information from an API and render it (comments from [jsonplaceholder](https://jsonplaceholder.typicode.com/)).
- URL dynamic update in Browser (Front-End).
- Security: Cross-site request forgery protection over WebSockets.
- RSS feed.
- TXT files.
- Sitemap.

## URLs

- `/` -> Home.
- `/about-us/` -> Static page.
- `/cats/` -> List of cats. 
- `/cats/felix/` -> Single cat.
- `/cats/felix/new/` -> Add new cat.
- `/cats/felix/update/` -> Update cat.
- `/contact/` -> Contact.
- `/login/` -> Login.
- `/profile/` -> Private page.
- `/comments/` -> List API commets.
- `/rss.xml` -> Feed cat.
- `/sitemap.txt` -> Sitemap (Yes, a Sitemap can also be in txt).
- `/robots.txt` -> Tells search engine crawlers which URLs on your site they can access.
- `/humans.txt` -> The people behind a website.
- `/security.txt` -> Security information that is meant to allow security researchers to easily report security vulnerabilities.
- `/admin/` -> Django admin. (User: `admin`, Password: `admin`)

## Requirements

- Docker 🐋
- Make ⚙️

## Run 🏃

```shell
docker compose up
```

Make fake data.

```shell
make run.fake
```

## How does the information move?

When an event occurs in the frontend, **HTML generation is not JavaScript's job**. All logic, rendering, updating and any functionality is handled by the backend.

A simple case: a button that when clicked displays a modal. The flow of actions would be as follows:

1. Stimulus would capture the `click` event, maybe a button.
2. The Stimulus **Controller** (`home_controller.js`) function sends via WebSockets (using `sendData`), the **action** it needs together with the collected information.
3. `consumers.py` would decide which functionality should be executed. They are hosted in the appropriate action. Depending on the action we will do one task or another. Example: If the action is `home->open_modal`, we will call the function `actions.home.open_modal` in Django.
4. Action (`actions` directory) is executed by rendering the new HTML from a template. Perhaps `modal.html`.
5. The HTML is sent via `consumer.send_html()` through WebSockets to the client that has requested to execute the action.
6. Frontend receives a JSON with the new HTML, along with other properties. Inside JSON is specified in which `id` the prerendered HTML should be inserted. In this case it will fill an empty element with `modal.html` contain.

Additionally, without the frontend having to intervene, the browser URL is updated or it is decided whether the HTML is to be replaced or added.

## Concepts

### Actions

Place where the functions and logic of the business logic are stored.

### Views

Where to generate URLs for Server-Side Rendering (SSR). It uses the same logic, and therefore resulting HTML, as dynamic views.

### Consumers

Controller between the frontend and the backend. It captures the frontend queries and their information, to execute the appropriate action. 

### Templates

HTML templates that will use the `views.py` for SSR and the actions for rendering the different elements or responses.

## Create a new page 📰➕

When we create a page we must enable the possibility for Django to generate a static page, in case it enters by URL, in addition to preparing a new Action for its dynamic generation. Therefore we must follow the following steps.

In the following example we are going to create the About us page.

### 1. Define the route

In `urls.py` we add the path and point to the future view.

```python
urlpatterns = i18n_patterns(
	...
    path(_("about-us/"), views.about_us, name="about us"),
	...
)
```

### 2. Define the view

In `app/website/views.py` we add the view.

```python
def about_us(request):
    return render(request, "base.html", get_about_us_context())
```

Where does `get_about_us_context()` come from? It will be loaded automatically. It will look for an Action called `about_us.py` and inside it will get the `get_context` function which in the view will have the alias `get_about_us_context()`. That there are no conflicts with other contexts.

### 3. Add new Action

We create the `about_us.py` file inside `app/website/actions` with the following content.

```python
from django.template.loader import render_to_string
from django.templatetags.static import static
from app.website.context_processors import get_global_context
from django.urls import reverse
from django.utils.translation import gettext as _
from app.website.utils import (
    update_active_nav,
    enable_lang,
    loading,
)
from core import settings


template = "pages/about_us.html"


def get_context():
    context = get_global_context()
    # Update context
    context.update(
        {
            "url": settings.DOMAIN_URL + reverse("about us"),
            "title": _("About us") + " | " + settings.SITE_NAME,
            "meta": {
                "description": _("About us page of the website"),
                "image": f"{settings.DOMAIN_URL}{static('img/seo/cat.jpg')}",
            },
            "active_nav": "about us",
            "page": template,
        }
    )
    return context


def get_html(lang=None):
    return render_to_string(template, get_context())


@enable_lang
@loading
def send_page(consumer, client_data, lang=None):
    # Nav
    update_active_nav(consumer, "about us")
    # Main
    data = {
        "action": client_data["action"],
        "selector": "#main",
        "html": get_html(lang=lang),
    }
    data.update(get_context())
    consumer.send_html(data)
```

### 4. Add template

We create the `about_us.html` file inside `templates/pages` with the following content.

```jinja
{% load i18n %}
<h1>{% trans "About us page" %}</h1>
```

### 5. Add event handler in JavaScript

Using Stimulus, we will create the controller. To do this we create a file called `about_us_controller.js` in `assets/js/controllers` with the following content.

```javascript
import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = [];

    foo(event) {
		sendData(
			{
			action: "foo->boo",
			data: {}
		});
	}
}
```

And we register it in `assets/js/main.js`.

```javascript
import { connect, startEvents } from './webSocketsCli.js';
import { Application } from "./vendors/stimulus.js";
import contactController from "./controllers/contact_controller.js"; // New line

/*
   INITIALIZATION
 */

// WebSocket connection
connect();
startEvents();

// Stimulus
window.Stimulus = Application.start();

// Register all controllers
Stimulus.register("contact", contactController); // New line
```

## Technology Stack 😍

- [Django](https://www.djangoproject.com/)
- [Channels](https://channels.readthedocs.io/en/stable/)
- [Stimulus](https://stimulus.hotwired.dev/)
