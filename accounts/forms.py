from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users.
    extends UserCreationForm to change the model
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
