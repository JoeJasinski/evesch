from org.models import Organization
from django.contrib.syndication.feeds import Feed


class OrgFeed(Feed):
    title = "Org Test Title"
    link = "/admin/"
    description= "this is a description"
    
    def items(self):
        return Organization.objects.all()