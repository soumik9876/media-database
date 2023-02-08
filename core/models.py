from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """
        Base model for inheriting common fields
    """
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
