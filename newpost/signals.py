from django.db.models.signals import post_save
from django.dispatch import receiver
from firebase_admin.messaging import Message, Notification
from .models import CustomDevice, UnregisteredAlert, EmergencyAlertByUser


# Common notification sender
def send_emergency_notification(title, body, data):
    devices = CustomDevice.objects.all()
    if devices.exists():
        devices.send_message(
            Message(
                notification=Notification(
                    title=title,
                    body=body
                ),
                data=data
            )
        )


@receiver(post_save, sender=UnregisteredAlert)
def notify_unregistered_alert_created(sender, instance, created, **kwargs):
    if created:
        send_emergency_notification(
            title="🚨 Unregistered Emergency Alert",
            body=f"Unknown person reported: {instance.description[:100]}...",
            data={
                "name": instance.name,
                "contact": instance.contact,
                "description": instance.description,
                "image": instance.image or "",
                "route": "/getUnregisteredAlert"
            }
        )

@receiver(post_save, sender=EmergencyAlertByUser)
def notify_registered_alert_created(sender, instance, created, **kwargs):
    if created:
        send_emergency_notification(
            title="🚨 Emergency Alert by User",
            body=f"{instance.user.full_name} reported: {instance.description[:100]}...",
            data={
                "user_id": str(instance.user.id),
                "description": instance.description,
                "image": instance.image or "",
                "route": "/getEmergencyAlert"
            }
        )
