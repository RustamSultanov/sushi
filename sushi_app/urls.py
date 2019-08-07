from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path(
        '', views.base, name='base'),
    path(
        'accounts/login/',
        auth_view.LoginView.as_view(
            template_name='authentication_login.html',
            authentication_form=LoginForm), name='login'),
    path(
        'logout',
        auth_view.LogoutView.as_view(next_page="login"),
        name='logout'),
    path('employee/<int:user_id>', views.employee_info, name='employee_info'),
    path('manager-lk', views.manager_lk_view, name='manager_lk'),
    path('partner-lk', views.partner_lk_view, name='partner_lk'),
    path('partner/new', views.create_partner_view, name='create_partner'),
    path('partner/edit/<int:user_id>', views.edit_partner_view, name='edit_partner'),
    path(
        'request/new', views.form_request_view, name='form_request'),
    path(
        'review/new', views.feedback_form_view, name='form_review'),
    path('shop/new', views.shop_form_view, name='shop_form'),
    path(
        'shop/<int:shop_id>',
        login_required(views.ShopListView.as_view()),
        name='shop'),
    path(
        'task/new/<int:partner_id>', views.form_task_view, name='form_task'),
    path(
        'product-detail/<int:product_id>', views.product_detail_view, name='product_detail'),
    path(
        'task/<int:task_id>-<int:user_id>', views.task_view, name='task'),
    path(
        'request/<int:requests_id>-<int:user_id>', views.requests_view, name='request'),
    path(
        'review/<int:feedback_id>-<int:user_id>', views.feedback_view, name='feedback'),
]
