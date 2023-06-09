from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading
from core.models import Wallet, Currency
from django.utils.translation import gettext as _
from django.utils.translation import get_language


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': _('Username should only contain alphanumeric characters')}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': _('Username is already taken')}, status=409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': _('Email is invalid')}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': _('Email is already taken')}, status=409)
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        lang = get_language()

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, _('Password is too short'))
                    return render(request, 'authentication/register.html', context)

                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False  # set user inactive
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
                activate_url = f"http://{domain}{link}"

                if lang == 'cs':
                    email_text = f"Dobrý den {user.username}, pro aktivaci účtu klikněte na tento odkaz {activate_url}"
                    currency = Currency.objects.get(code='CZK')
                else:
                    email_text = f"Hi {user.username} Please use this link to activate your account {activate_url}"
                    currency = Currency.objects.get(code='USD')

                Wallet.objects.create(owner=user, currency=currency)

                email_subject = _('Activate your account')
                email_body = email_text
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@budgetapp.com',
                    [email]
                )
                EmailThread(email).start()
                messages.success(request, _('Account was created, we have sent you e-mail with activation link'))
                return render(request, 'authentication/register.html')

        return render(request, 'authentication/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, _('Account activated succesfully'))
            return redirect('login')

        except Exception as ex:
            pass
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return redirect('dashboard')
                messages.error(request, _('Account is not active, please check you email'))
                return render(request, 'authentication/login.html')

            messages.error(request, _('The user does not exist, please check your credentials'))
            return render(request, 'authentication/login.html')

        messages.error(request, _('Please fill all fields'))
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, _('You have been successfully logout'))
        return redirect('login')


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST['email']
        lang = get_language()
        context = {
            'values': request.POST
        }
        if not validate_email(email):
            messages.error(request, _('Please enter a valid email'))
            return render(request, 'authentication/reset-password.html', context)

        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])
            }
            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = _('Password reset Instructions')
            reset_url = f"http://{current_site.domain}{link}"

            if lang == 'cs':
                email_text = f'Dobrý den, pro nastavení nového hesla klikněte na tento odkaz {reset_url}'
            else:
                email_text = f'Hi, Please click the link below to reset your password {reset_url}'

            email = EmailMessage(
                email_subject,
                email_text,
                'noreply@expenses.com',
                [email]
            )
            EmailThread(email).start()
            messages.success(request, _('We have sent you an email to reset your password'))

        return render(request, 'authentication/reset-password.html')


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, _('Passwords do not match'))
            return render(request, 'authentication/set-new-password.html', context)

        if len(password) < 6:
            messages.error(request, _('Password is too short'))
            return render(request, 'authentication/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, _('Password link is invalid, please request a new one'))
                return render(request, 'authentication/set-new-password.html', context)

            user.set_password(password)
            user.save()
            messages.success(request, _('Password reset succesfully'))

            return redirect('login')

        except Exception as identifier:
            messages.info(request, _('Something went wrong'))
            return render(request, 'authentication/set-new-password.html', context)
