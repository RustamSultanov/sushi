from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
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
    path(
        'request/new', views.form_request_view, name='form_request'),
    path(
        'review/new', views.feedback_form_view, name='form_review'),
    path(
        'task/new/<int:partner_id>', views.form_task_view, name='form_task'),
    path(
        'product-detail/<int:product_id>', views.product_detail_view, name='product_detail'),
    # path(
    #     'product-feedback/<int:product_id>', views.feedback_view, name='feedback'),
]
