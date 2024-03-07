from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import CustomerInquiry

from .forms import RegistrationForm
from django.contrib import messages

def advise(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đăng ký thành công!')
            print('Đăng ký thành công')
            return redirect('advise')  # Redirect back to the form page
        else:
            print('Đăng ký ko thành công')
            messages.error(request, 'Đăng ký thất bại. Vui lòng thử lại.')
            
    else:
        form = RegistrationForm()
    return render(request, 'advise.html', {'form': form})


def advise(request):
    return render(request, "advise.html")