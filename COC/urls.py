"""COC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from admin_page import views as admin_views
from users import views as user_views

urlpatterns = [
    url(r'user_site', user_views.user_site),
    url(r'view_complaint',admin_views.view_complaint),
    url(r'view_feedback',admin_views.view_feedback),
    url(r'view_news', admin_views.view_news),
    url(r'view_garbage', admin_views.view_report),
    url(r'view_user', admin_views.view_user),
    url(r'view_employee', admin_views.view_employee),
    url(r'view_zone', admin_views.view_zone),
    url(r'view_division',admin_views.view_division),
    url(r'view_news', admin_views.view_news),
    url(r'view_user', admin_views.view_user),
    url(r'update_employee_form', admin_views.update_employee_form),
    url(r'update_zone_form', admin_views.update_zone_form),
    url(r'update_division_form',admin_views.update_division_form),
    url(r'update_employee', admin_views.update_employee),
    url(r'update_zone', admin_views.update_zone),
    url(r'update_division',admin_views.update_division),
    url(r'delete_employee', admin_views.view_employee),
    url(r'delete_news', admin_views.view_news),
    url(r'add_employee_form', admin_views.add_employee_form),
    url(r'add_zone_form',admin_views.add_zone_form),
    url(r'add_division_form',admin_views.add_division_form),
    url(r'add_employee', admin_views.add_employee),
    url(r'add_zone', admin_views.add_zone),
    url(r'add_division',admin_views.add_division),
    url(r'admin_login_fill',admin_views.admin_login_fill),
    url(r'admin_login',admin_views.admin_login),
    url(r'admin_home',admin_views.admin_home),
    url(r'complaint_resolve',user_views.resolve),
    url(r'sign-in', user_views.sign_in),
    url(r'sign-up', user_views.sign_up),
    url(r'sign_up_form',user_views.sign_up_form),
    url(r'sign_in_form',user_views.sign_in_form),
    url(r'complaint_form',user_views.complaint_form),
    url(r'complaint',user_views.complaint),
    url(r'zone_fill', user_views.zone_fill),
    url(r'zone', user_views.zone),
    url(r'resubmit',user_views.resubmit),
    url(r'feedback_form',user_views.feedback_form),
    url(r'update_fill',user_views.update_fill),
    url(r'update',user_views.update),
    url(r'division_fill',user_views.division_fill),
    url(r'division', user_views.division),
    url(r'official_login_fill', user_views.official_login_form),
    url(r'official-login', user_views.official_login),
    url(r'employee_site', user_views.emp_site),
    url(r'garbage_fill',user_views.garbage_fill),
    url(r'garbage_form_fill',user_views.garbage_entries),
    url(r'garbage_form',user_views.garbage_form),
    url(r'garbage', user_views.garbage),
    url(r'reset_passwrd',user_views.reset_passwrd),
    url(r'feedback',user_views.feedback),
    url(r'signout',user_views.signout),
    url(r'delete_account',user_views.delete_account),
    url(r'home',user_views.home),
    url(r'',user_views.home),
    url(r'users/',include('users.urls')),
    url(r'admin_page/',include('admin_page.urls')),
]
