from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm   #

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            # AUTO LOGIN
            login(request, user)

            # ALERT
            messages.success(request, "Registrasi berhasil! Anda sudah login.")

            return redirect('home')
        else:
            messages.error(request, "Registrasi gagal, cek input!")

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})