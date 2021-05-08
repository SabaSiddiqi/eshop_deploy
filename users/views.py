# users/views.py

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from shop.models import Cart, SubscriptionList
from shop.views import subscribe, unsubscribe
from django.core.mail import send_mail
from django.template.loader import render_to_string




def dashboard(request):
    return redirect(reverse("shop:ShopHome"))


def register(request):

    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, "users/register.html", context={"form": form})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        #create subscription list
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save()
            Cart.objects.create(author=user)
            login(request, user)
            if request.POST.get("subscribe"):
                SubscriptionList.objects.create(subscribe_user=request.user, subscribe_status=True)
            else:
                SubscriptionList.objects.create(subscribe_user=request.user, subscribe_status=False)

            msg_plain = render_to_string('users/account_created.txt', {'username': user.username})
            msg_html = render_to_string('users/account_created.html', {'username': user.username})

            send_mail(
                'email title',
                msg_plain,
                'iyraseshop@gmail.com', ['saba.siddiqui.2010@gmail.com'], fail_silently=False,
                html_message=msg_html,
                )

            return redirect(reverse("dashboard"))
        else:
            print("Form is invalid")
            return render(request, "users/register.html", {'form': form})
