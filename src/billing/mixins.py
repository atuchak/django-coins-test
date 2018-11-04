from django.db import models


class CreateUpdateMixin(models.Model):
    """
    Add time of creation and last update time to model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
