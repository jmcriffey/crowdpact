from crowdpact.apps.event.models import EmailNotification, SiteNotification


def create_notifications_for_users(accounts, event):
    """
    Create any applicable notifications for the provided accounts and events.
    """
    # Create SiteNotifications for all users
    SiteNotification.objects.bulk_create([
        SiteNotification(account=act, event=event)
        for act in accounts
    ])

    # Create EmailNotifications for all users
    EmailNotification.objects.bulk_create([
        EmailNotification(account=act, event=event)
        for act in accounts
        if act.send_email_notifications
    ])


def send_notifications():
    """
    Send any unsent notifications.
    """
    # Send any email related tasks
    for note in EmailNotification.objects.select_related('event', 'account').filter(sent=False):
        note.send()
