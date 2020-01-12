from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # abstract=True 를 하면 데이터 베이스에 등록되지 않음
