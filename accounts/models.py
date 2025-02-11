from django.db import models
from django.contrib.auth.hashers import make_password

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def save(self, *args, **kwargs):
        # ✅ Ensure password is hashed before saving
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
