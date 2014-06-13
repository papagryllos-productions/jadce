from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

import area51.models as M

class LatestEntriesFeed(Feed):
    title = "Area 51 RSS feed"
    link = "/feed/"
    description = "Latest alien sightings in the wild"

    def items(self):
        return M.Event.objects.all().order_by('date_of_creation')[:20]

    def item_title(self, item):
        return "%s by %s" % (item.title, item.creator)

    def item_description(self, item):
        return item.description
