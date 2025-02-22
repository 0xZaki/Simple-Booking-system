from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    """
    Custom login view that extends the default login view to
    - redirect to the home page if the user is already authenticated
    - change the template
    """
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bookings:home')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bookings:home')
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})
