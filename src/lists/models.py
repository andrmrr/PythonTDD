from django.db import models
from django.urls import reverse
from django.conf import settings

class List(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lists",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="shared_with_me")

    @property
    def name(self):
        return self.item_set.first().text

    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])
    

class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ("id",)
        unique_together = ("list", "text")
