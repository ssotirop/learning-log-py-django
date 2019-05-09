from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Define a model for the topics users will create and store
class Topic(models.Model):
    """A topic the user is learning about"""
    text = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of the model."""
        return self.text


# Define a model for the kinds of entries users can make
# in their learning logs.
class Entry(models.Model):
    """Something specific learned about a topic"""
    # Since Django v2.0 ForeignKey() expects two arguments
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    # Meta class holds extra information for managing a model; here it
    # allows us to set a special attribute telling Django to use Entries
    # when it needs to refer to more than one entry. Without this, Django
    # would refer to multiple entries as Entrys.
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Return a string representation of the model."""
        return self.text[:80] + "..."
