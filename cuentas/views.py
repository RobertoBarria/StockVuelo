from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

class LoginView(auth_views.LoginView):
    authentication_form = CustomAuthenticationForm

User = get_user_model()

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            avion = form.cleaned_data.get('avion')

            user = auth.authenticate(email=email, password=password)
            if user is not None:
                if not user.is_active:
                    messages.error(request, 'La cuenta está inactiva.')
                elif user.avion != avion:
                    messages.error(request, 'El avión seleccionado no corresponde con el usuario.')
                else:
                    auth.login(request, user)
                    request.session['avion_id'] = avion.id
                    messages.success(request, 'Acceso correcto.')
                    return redirect('tienda')
            else:
                messages.error(request, 'Las credenciales son incorrectas.')
        else:
            for field, error in form.errors.items():
                messages.error(request, f"{field}: {', '.join(error)}")
    else:
        form = LoginForm()
    return render(request, 'cuentas/login.html', {'form': form})

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    request.session.flush()
    messages.success(request, 'Has finalizado sesión.')
    return redirect('login')