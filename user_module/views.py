from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import TemplateView
from utils.email_service import send_email
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, EditProfileModelForm, \
    ChangePasswordForm
from .models import User
from django.utils.decorators import method_decorator

# Create your views here.


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'user_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            user: bool = User.objects.filter(email__iexact=email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    email_active_code=get_random_string(length=72),
                    is_active=False
                )
                new_user.set_password(password)
                new_user.save()

                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'emails/active_account.html')
                return redirect(reverse('home_page'))

        context = {
            'register_form': register_form,
        }

        return render(request, 'user_module/register.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))

        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }

        return render(request, 'user_module/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(email__iexact=email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده')
                else:
                    check_pass = user.check_password(password)
                    if check_pass:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password', 'ایمیل یا رمز عبور اشتباه میباشد')

            else:
                login_form.add_error('password', 'ایمیل یا رمز عبور اشتباه میباشد')

        context = {
            'login_form': login_form,
        }

        return render(request, 'user_module/login.html', context)



class ActiveAccountView(View):
    def get(self, request, email_active_code):
        user = User.objects.get(email_active_code__iexact=email_active_code)
        if user is not None:
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        raise Http404


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardPageView(TemplateView):
    template_name = 'user_module/user_panel_dashboard.html'


@method_decorator(login_required, name='dispatch')
class EditUserProfilePageView(View):
    def get(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'edit_form': edit_form,
            'current_user': current_user,
        }

        return render(request, 'user_module/edit_user_profile_page.html', context)

    def post(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileModelForm(request.POST, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'edit_form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_module/edit_user_profile_page.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request):
        change_pass_form = ChangePasswordForm()
        context = {
            'form': change_pass_form,
        }
        return render(request, 'user_module/change_password_page.html', context)

    def post(self, request):
        change_pass_form = ChangePasswordForm(request.POST)
        current_user = User.objects.get(id=request.user.id)
        if change_pass_form.is_valid():
            if current_user.check_password(change_pass_form.cleaned_data['current_password']):
                current_user.set_password(change_pass_form.cleaned_data['new_password'])
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                change_pass_form.add_error('current_password', 'رمز اشتباه است!')

        context = {
            'form': change_pass_form,
        }
        return render(request, 'user_module/change_password_page.html', context)



class ForgotPasswordView(View):
    def get(self, request):
        forgot_password_form = ForgotPasswordForm()
        context = {
            'forgot_password_form': forgot_password_form,
        }

        return render(request, 'user_module/forgot_password_page.html', context)

    def post(self, request):
        forgot_password_form = ForgotPasswordForm(request.POST)
        if forgot_password_form.is_valid():
            email = forgot_password_form.cleaned_data['email']
            user = User.objects.filter(email__iexact=email).first()
            if user is not None:
                send_email('فراموشی رمز عبور', user.email, {'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('home_page'))

            else:
                forgot_password_form.add_error('email', 'این کاربر موجود نیست')

        return redirect(reverse('forgot_password_page'))


class ResetPasswordView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            reset_password_form = ResetPasswordForm()
            context = {
                'reset_password_form': reset_password_form,
                'user': user,
            }
            return render(request, 'user_module/reset_password_page.html', context)

        return redirect(reverse('forgot_password_page'))

    def post(self, request, email_active_code):
        reset_password_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if reset_password_form.is_valid():
            if user is not None:
                new_password = reset_password_form.cleaned_data['new_password']
                user.set_password(new_password)
                user.email_active_code = get_random_string(length=72)
                user.save()
                return redirect(reverse('login_page'))

            return redirect(reverse('forgot_password_page'))

        return render(request, 'user_module/reset_password_page.html', {
            'reset_pass_form': reset_password_form,
            'user': user
        })

@login_required
def user_panel_menu(request):
    return render(request, 'user_module/components/user_panel_menu_component.html')