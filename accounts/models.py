from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SELLER', 'Seller'),
        ('BUYER', 'Buyer'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='BUYER'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

class SellerProfile(models.Model):

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='seller_profile'
    )

    business_name = models.CharField(max_length=150)

    business_description = models.TextField(
        blank=True
    )

    approval_status = models.CharField(
        max_length=20,
        choices=(
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
        ),
        default='PENDING'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
