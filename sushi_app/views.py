from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import RequestsForm, MessegesForm, TaskForm
from .models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from wagtail.admin.utils import user_passes_test

User = get_user_model()


# # Create your views here
def manager_check(user):
    return user.user_profile.is_manager


def partner_check(user):
    return user.user_profile.is_partner


@login_required
def base(request):
    employee_list = UserProfile.objects.prefetch_related('user', 'wagtail_profile', 'department') \
        .filter(head=request.user.user_profile)
    return render(request, 'index.html', {'employee_list': employee_list})


@login_required
@user_passes_test(manager_check)
def employee_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'employee.html', {'employee': user})


@login_required
@user_passes_test(manager_check)
def manager_lk_view(request):
    partner_list = UserProfile.objects.prefetch_related('user', 'wagtail_profile') \
        .filter(manager=request.user.user_profile)
    request_list = Requests.objects.prefetch_related('responsible') \
        .filter(manager=request.user.user_profile)
    task_list = Task.objects.prefetch_related('responsible') \
        .filter(manager=request.user.user_profile)
    feedback_list = Feedback.objects.prefetch_related('responsible', 'shop') \
        .filter(manager=request.user.user_profile)
    return render(request, 'dashboard_manager.html', {'partner_list': partner_list,
                                                      'request_list': request_list,
                                                      'task_list': task_list,
                                                      'feedback_list': feedback_list,
                                                      'breadcrumb': [{'title': 'Личный кабинет'}]})


@login_required
@user_passes_test(partner_check)
def partner_lk_view(request):
    shop_list = Shop.objects.prefetch_related('checks', 'docs') \
        .filter(partner=request.user)
    request_list = Requests.objects.prefetch_related('responsible') \
        .filter(responsible=request.user)
    task_list = Task.objects.prefetch_related('responsible') \
        .filter(responsible=request.user)
    feedback_list = Feedback.objects.prefetch_related('responsible', 'shop') \
        .filter(responsible=request.user.user_profile)
    return render(request, 'dashboard_partner.html', {'shop_list': shop_list,
                                                      'request_list': request_list,
                                                      'task_list': task_list,
                                                      'feedback_list': feedback_list,
                                                      'breadcrumb': [{'title': 'Личный кабинет'}],
                                                      'manager': request.user.user_profile.manager})


@login_required
@user_passes_test(partner_check)
def form_request_view(request):
    form = RequestsForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = request.user
        form.manager = request.user.user_profile.manager
        form.save()
        return HttpResponseRedirect(reverse_lazy('partner_lk'))
    return render(request, 'request_new.html', {'manager': request.user.user_profile.manager,
                                                'form': form, 'breadcrumb': [{'title': 'Личный кабинет',
                                                                              'url': reverse_lazy('partner_lk')},
                                                                             {'title': 'Добавить запрос'}]})


@login_required
@user_passes_test(manager_check)
def form_task_view(request, partner_id):
    partner = get_object_or_404(UserProfile, id=partner_id)
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = partner
        form.manager = request.user.user_profile
        form.save()
        return HttpResponseRedirect(reverse_lazy('manager_lk'))
    return render(request, 'task_new.html', {'partner': partner,
                                             'form': form, 'breadcrumb': [{'title': partner.user.get_full_name,
                                                                           'url': reverse('employee_info', partner.user.id)},
                                                                          {'title': 'Добавить задачу'}]})


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

# def feedback_view(request, product_id):
#     form = FeedbackForm(request.POST or None, request.FILES or None)
#     product = get_object_or_404(Product, id=product_id)
#     if form.is_valid():
#         new_feed = form.save(commit=False)
#         text = form.cleaned_data['text']
#         adv = form.cleaned_data['adv']
#         disadv = form.cleaned_data['disadv']
#         files = form.cleaned_data['files']
#         rating = form.cleaned_data['rating']
#         user = User.objects.get(id=request.user.id)
#         new_feed.user = user
#         new_feed.text = text
#         new_feed.adv = adv
#         new_feed.files = files
#         new_feed.rating = rating
#         new_feed.product = product
#         new_feed.save()
#         return HttpResponseRedirect(f'../product/{product_id}')
#     context = {
#         'form': form,
#         'product': product
#     }
#     return render(request, 'review.html', context)
