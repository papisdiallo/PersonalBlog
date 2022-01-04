from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from Users.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def createNewProfile(sender, instance, created, **kwargs):
    if created and not instance.is_developer_account:
        Profile.objects.create(user=instance)
    if created == False:
        instance.profile.save()
