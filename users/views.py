# users/views.py

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm
from shop.models import Cart, SubscriptionList
from shop.views import subscribe, unsubscribe
from django.core.mail import send_mail
from django.template.loader import render_to_string
from shop.models import HtmlField, Logo
from django.template.loader import render_to_string, get_template





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
            login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
            if request.POST.get("subscribe"):
                SubscriptionList.objects.create(subscribe_user=request.user, subscribe_status=True)
            else:
                SubscriptionList.objects.create(subscribe_user=request.user, subscribe_status=False)
            logo = Logo.objects.filter(logo_text='logo').first()

            ctx = {
                'site':'https://www.iyraseshop.com',
                'username': user.username,
                'email': user.email,
                'logo':logo.logo_image,
            }


            message = get_template('app/account_created.html').render(ctx)
            send_mail(
                "Iyra's Eshop - Account Created",
                message,
                'iyraseshop@gmail.com',
                [user.email],
                fail_silently=False,
                html_message=message,)


            return redirect(reverse("dashboard"))
        else:
            print("Form is invalid")
            return render(request, "users/register.html", {'form': form})
