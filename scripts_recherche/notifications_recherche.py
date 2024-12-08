"notifications.py permet d'afficher des notifications système"
from platform import system # Importer la fonction system() depuis platform pour avoir connaissance du système d'exploitation
import plyer.platforms.win.notification as win_notif # Importer l'API de notifications Windows depuis Plyer
#import plyer.platforms.macosx.notification as mac_notif # Importer l'API de notifications Mac depuis Plyer
import plyer.platforms.linux.notification as linux_notif # Importer l'API de notifications Linux depuis Plyer

def afficher_notification(titre="", message=""):
    """Affiche une notification système avec le titre titre et le message message
    - titre : titre de la notification
    - message: message de la notification"""

    if system() == "Windows": # Si le système d'exploitation est de type Windows
        win_notif.WindowsNotification().notify(title=titre, message=message, timeout=20, toast=True) # Envoyer une notification Windows

    elif system() == "Linux": # Si le système d'exploitation est de type Linux
        linux_notif.NotifySendNotification.notify(title=titre, message=message, timeout=20, toast=True) # Envoyer une notification Linux          

    """elif system() == "Darwin": # Si le système d'exploitation est de type Mac
        mac_notif.Notification().notify(title=titre, message=message, timeout=20) # Envoyer une notification Mac"""

      