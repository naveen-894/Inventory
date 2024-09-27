from django.db import models

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # This makes the model abstract, so no database table will be created

class Item(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class AdminUser(BaseModel):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"