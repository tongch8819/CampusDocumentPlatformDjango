from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# FIX: Inherit from models.Model, not models.fields.CharField
class Tag(models.Model):
    CATEGORY_CHOICES = [
        ('SUBJECT', 'Subject'), # e.g., CS
        ('COURSE', 'Course'),   # e.g., Operating Systems
        ('TYPE', 'Type'),       # e.g., Notes, Lab Report
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"

class Material(models.Model):
    STATUS_CHOICES = [
        ('AUTO_FILED', 'Auto Filed'),
        ('PENDING', 'Pending Manual Review'),
    ]
    
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='materials/%Y/%m/')
    file_hash = models.CharField(max_length=64, unique=True, help_text="SHA-256 hash for duplicate detection")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_materials')
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    upload_time = models.DateTimeField(auto_now_add=True)
    
    # Store extracted text for ML classification later
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

# FIX: Inherit from models.Model, not models.fields.CharField
class Sharing(models.Model):
    PERMISSION_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('TARGETED', 'Targeted (Specific Class/Users)'),
    ]
    material = models.OneToOneField(Material, on_delete=models.CASCADE, related_name='sharing_settings')
    permission_type = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='PRIVATE')
    target_group = models.CharField(max_length=100, blank=True, help_text="Store class ID or department if TARGETED")

    def __str__(self):
        return f"{self.material.title} - {self.permission_type}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'material') # Prevent duplicate favorites

    def __str__(self):
        return f"{self.user.username} favorited {self.material.title}"

class Comment(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.material.title}"
    


# This listens for when a new Material is saved
@receiver(post_save, sender=Material)
def create_default_sharing_setting(sender, instance, created, **kwargs):
    if created:
        # Automatically create a Sharing profile linked to this material (defaults to PRIVATE)
        Sharing.objects.create(material=instance)