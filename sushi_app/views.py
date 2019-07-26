from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, MessegesForm, FeedbackForm
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from wagtail.admin.utils import user_passes_test

User = get_user_model()


# # Create your views here
def manager_check(user):
    return user.user_profile.is_manager


def partner_check(user):
    return user.user_profile.is_partner


@login_required
def base(request):
    employee_list = UserProfile.objects.prefetch_related('user', 'department') \
        .filter(head=request.user.user_profile)
    return render(request, 'index.html', {'employee_list': employee_list})


@login_required
@user_passes_test(manager_check)
def employee_info(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'employee.html', {'employee': user})


@login_required
@user_passes_test(manager_check)
def manager_lk_view(request):
    partner_list = UserProfile.objects.prefetch_related('user')\
        .filter(manager=request.user.user_profile)
    return render(request, 'dashboard_manager.html', {'partner_list': partner_list,
                                                      'breadcrumb': [{'title': 'Личный кабинет'}]})


@login_required
@user_passes_test(partner_check)
def partner_lk_view(request):
    shop_list = Shop.objects.prefetch_related('checks', 'docs')\
        .filter(partner=request.user)
    return render(request, 'dashboard_partner.html', {'shop_list': shop_list,
                                                      'breadcrumb': [{'title': 'Личный кабинет'}],
                                                      'manager': request.user.user_profile.manager})


def chat_view(request, product_id, user_id):
    product = Product.objects.get(id=product_id)
    qs1 = Messeges.objects.prefetch_related('user', 'accepter').filter(product=product, user=request.user.id)
    qs2 = Messeges.objects.prefetch_related('user', 'accepter').filter(product=product, accepter=request.user.id)
    messeges = qs1.union(qs2).order_by('date_create')
    form = MessegesForm(request.POST or None)
    if form.is_valid():
        new_disput = form.save(commit=False)
        text = form.cleaned_data['text']
        new_disput.text = text
        new_disput.user = request.user
        if request.user == product.user:
            new_disput.accepter = messeges.first().user
        else:
            new_disput.accepter = product.user
        new_disput.product = product
        new_disput.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'chat-2.html', {'product': product, 'messeges': messeges, 'form': form})


def product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product.html', {'product': product})


def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'details.html', {'product': product})


def feedback_view(request, product_id):
    form = FeedbackForm(request.POST or None, request.FILES or None)
    product = get_object_or_404(Product, id=product_id)
    if form.is_valid():
        new_feed = form.save(commit=False)
        text = form.cleaned_data['text']
        adv = form.cleaned_data['adv']
        disadv = form.cleaned_data['disadv']
        files = form.cleaned_data['files']
        rating = form.cleaned_data['rating']
        user = User.objects.get(id=request.user.id)
        new_feed.user = user
        new_feed.text = text
        new_feed.adv = adv
        new_feed.files = files
        new_feed.rating = rating
        new_feed.product = product
        new_feed.save()
        return HttpResponseRedirect(f'../product/{product_id}')
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'review.html', context)
