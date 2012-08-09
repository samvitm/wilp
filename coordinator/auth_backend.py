from django.contrib.auth.backends import ModelBackend
from wilp.coordinator.models import BitsCoordinator

class BitsCoordinatorModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = BitsCoordinator.objects.get(username=username)
            if user.check_password(password):
                return user
        except BitsCoordinator.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return BitsCoordinator.objects.get(pk=user_id)
        except BitsCoordinator.DoesNotExist:
            return None


  