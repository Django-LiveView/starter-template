# Django template for creating a complete HTML over the Wire site

This template has an example of the most common cases.

- Navigation Real-time without loads similar to SPA.
- URL dynamic update in Browser (Front-End).
- Server-Side Rendering (SSR) of pages for SEO (Using `views.py`).
- Multilanguage.
- Real-time notification message or "flash message" (Feline notifications 🐈📢).
- Switch to a static page (Home).
- Switch to a dynamic page (List of cats 🐈🐈🐈🐈🐈🐈).
- Single page (Cat 🐈).
- Add a new item in the database (👶🏻🐈).
- Delete item from the database (🐈☠).
- Update item from the database (🐈👉🐕).
- Broadcast: Sending information to all customers in Real-time (🐈📢 🐈🐈🐈🐈🐈).
- Navigator whose active button changes dynamically.
- Contact form with validations.
- Get file from a client (🐈🖼️).
- Login.
- Private Page (🐈‍⬛).
- Get information from an API and render it (comments from [jsonplaceholder](https://jsonplaceholder.typicode.com/)).
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
- `/feed/` -> Cat Feed (RSS/Atom).
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

## Concepts

### Actions

Place where the functions and logic of the business logic are stored.

### Views

Where to generate URLs for Server-Side Rendering (SSR). It uses the same logic, and therefore resulting HTML, as dynamic views.

### Consumers

Controller between the frontend and the backend. It captures the frontend queries and their information, to execute the appropriate action. 

### Templates

HTML templates that will use the `views.py` for SSR and the actions for rendering the different elements or responses.

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

Below you can see an example of how to add a functionality.

## Add a feature 🪄

In the following example we are going to explain how to create the **"Get random number with HTML"** button functionality present in the **About us** page.

I strongly recommend that you first read the Stimulus documentation.

### 1. Include in the page the HTML button

We will also include the event definition following the [Stimulus documentation](https://stimulus.hotwired.dev/).

In `templates/pages/about_us.html`:

```jinja
<p>
	<button
		data-action="click->aboutUs#getRandomNumberHTML"
	>
		{% trans "Get random numberwith HTML" %}
	</button>
</p>
```

And a container, with a unique id, to indicate where the final result will be rendered.

```jinja
<div id="content-random-number-html"></div>
```

Let's not forget that all of this must be wrapped in an element with the appropriate *data-controller*.

```jinja
<div data-controller="aboutUs">
...
</div>
```

Everything together would be as follows:

```jinja
<div data-controller="aboutUs">
	<p>
		<button
		    data-action="click->aboutUs#getRandomNumberHTML"
		>
			{% trans "Get random numberwith HTML" %}
		</button>
	</p>
	<div id="content-random-number-html"></div>
</div>
```

### 2. Define the functionality of the JavaScript event

In `assets/js/controllers/about_us_controller.js`, we add the function `getRandomNumberHTML`. It will not send any information, it will only invoke the Action `update_random_number_html` on file `about_us` (`app/website/actions/about_us.py`).

```javascript
import { Controller } from "../vendors/stimulus.js";
import { sendData } from "../webSocketsCli.js";
import { getLang } from "../mixins/miscellaneous.js";

export default class extends Controller {

    static targets = [];

    getRandomNumberHTML(event) {
        sendData(
            {
                action: "about_us->update_random_number_html",
                data: {}
            }
        );
    }
}
```

### 3. Create functionality in the action

In `app/website/actions/about_us.py`, we add the function `update_random_number_html`.

```python
from random import randint

def update_random_number_html(consumer, client_data):
    """Update random number html"""
    data = {
        "action": client_data["action"],
        "selector": "#content-random-number-html",
        "html": render_to_string(
            "components/_random_number.html", {"number": randint(0, 100)}
        ),
    }
    consumer.send_html(data)
```

First we define the dictionary needed by the FrontEnd with the minimum information.

- `action`: It is optional. It is used in case you want to activate the cache system so that the client can continue navigating with connection errors or simply to avoid making requests to the Actions. The most common is to return the same string that comes from the FrontEnd.
- `selector`: Indicate the selector where the HTML will be rendered.
- `html`: The HTML to place inside the selector. It is rendered from the BackEnd using the `render_to_string` function. The first parameter indicates the template path (we will define it in the next step) and the second one the context. In our case a random number with the name `number`.
- `consumer.send_html(data)`: Sends the above dictionary to the client via WebSockets. When the FrontEnd receives the information, it will interpret the information and place the HTML in the appropriate sector.

### 4. Create HTML template for rendering

We create a HTML file in `templates/components/_random_number.html` with the following content:

```jinja2
<h3>{{ number }}</h3>
```

And we are done.

## Create a new page 🗒️➕

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
            }
        );
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

## More documentation

I have written a **book** where I explain all the concepts I have used in the template, explained step by step and some other mechanisms that are not present. If you are interested in further **increasing your knowledge about HTML over WebSockets in Python**, or creating **real-time SPAs using Django**, I recommend you to buy a copy. In addition, you will **indirectly support me** to continue working on the template.

- [Building SPAs with Django and HTML Over the Wire: Learn to build real-time single page applications with Python](https://www.amazon.com/Building-SPAs-Django-HTML-Over-ebook/dp/B0B3DV54ZT/ref=sr_1_1?crid=39E4BTNKDQ74I&keywords=andros+fenollosa&qid=1672045604&sprefix=andros+fenollos%2Caps%2C165&sr=8-1)

## Technology Stack 😍

- [Django](https://www.djangoproject.com/)
- [Channels](https://channels.readthedocs.io/en/stable/)
- [Stimulus](https://stimulus.hotwired.dev/)
