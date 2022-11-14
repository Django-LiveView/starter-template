# Django template for creating a complete HTML over the Wire site

This template has an example of the most common cases.

- Navigation Real-time without loads similar to SPA.
- Server-Side Rendering (SSR) of pages for SEO (Using `views.py`).
- Switch to a static page (Home).
- Switch to a dynamic page (List of cats 🐈🐈🐈🐈🐈🐈).
- Single page (Cat 🐈).
- Delete item from the database (🐈☠).
- Update item from the database (🐈👉🐕)
- Navigator whose active changes dynamically.
- Contact form with validations.
- RSS feed.
- URL dynamic update.
- Cross-site request forgery protection over WebSockets.

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
