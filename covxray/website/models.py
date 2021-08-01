from django.db import models

# Create your models here.
class XrayImages(models.Model):
    xray_scan_img = models.FileField(upload_to="images/")