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
- Get information from an API and render it.
- URL dynamic update in Browser (Front-End).
- Security: Cross-site request forgery protection over WebSockets.
- RSS feed.
- Sitemap.

## How does the information move?

When an event occurs in the frontend, **HTML generation is not JavaScript's job**. All logic, rendering, updating and any functionality is handled by the backend.

A simple case: a button that when clicked displays a modal. The flow of actions would be as follows:

1. Stimulus would capture the `click` event.
2. The Stimulus Controller function sends via WebSockets (using `sendData`), the action it needs together with the collected information. 
3. `consumers.py` would decide which functionality should be executed. They are hosted in the appropriate action views.
4. The `view.py` of the action is executed by rendering the new HTML from a template. Perhaps `modal.html`.
5. The HTML is sent via `consumer.send_html()` through WebSockets to the client that has requested to execute the action.
6. Frontend receives a JSON with the new HTML, along with other properties. Inside JSON is specified in which `id` the prerendered HTML should be inserted. In this case it will fill an empty element with `modal.html` contain.

Additionally, without the frontend having to intervene, the browser URL is updated or it is decided whether the HTML is to be replaced or added.

## Concepts

### Actions

### Views

### Consumers

### Templates

## Run 🏃

1. Up

```
docker-compose up
```

2. Add data. 

Run in Django container.

```
./manage.py shell < make_fake_data.py
```

## Thanks 😍

- [Django](https://www.djangoproject.com/)
- [Channels](https://channels.readthedocs.io/en/stable/)
