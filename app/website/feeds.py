from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Cat

class LatestEntriesFeed(Feed):
    title = "Latest Cats"
    link = "/feed/"
    description = "Updates on changes and additions to cats."

    def items(self):
        return Cat.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.biography

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('cat single', kwargs={'cat_slug': item.slug})
