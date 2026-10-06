from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import BuyerRegistrationForm, SellerRegistrationForm
from .models import SellerProfile

from products.models import Product


def buyer_register(request):

    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.role = 'BUYER'
            user.save()

            return redirect('login')

    else:
        form = BuyerRegistrationForm()

    return render(
        request,
        'accounts/buyer_register.html',
        {'form': form}
    )


def seller_register(request):

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.role = 'SELLER'
            user.save()

            SellerProfile.objects.create(
                user=user,
                business_name=form.cleaned_data['business_name'],
                business_description=form.cleaned_data['business_description']
            )

            return redirect('login')

    else:
        form = SellerRegistrationForm()

    return render(
        request,
        'accounts/seller_register.html',
        {'form': form}
    )


def register(request):

    form = None
    error = None
    account_type = ''

    if request.method == 'POST':

        account_type = request.POST.get('accountType')

        if account_type == 'buyer':

            form = BuyerRegistrationForm(request.POST)
            role = 'BUYER'

        elif account_type == 'seller':

            form = SellerRegistrationForm(request.POST)
            role = 'SELLER'

        else:

            error = 'Please select an account type.'

        if form and form.is_valid():

            user = form.save(commit=False)
            user.role = role
            user.save()

            if role == 'SELLER':

                SellerProfile.objects.create(
                    user=user,
                    business_name=form.cleaned_data['business_name'],
                    business_description=form.cleaned_data['business_description']
                )

            return redirect('login')

    return render(
        request,
        'accounts/Register.html',
        {
            'form': form,
            'error': error,
            'account_type': account_type,
        }
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Seller approval check
            if user.role == 'SELLER':

                seller_profile = getattr(
                    user,
                    'seller_profile',
                    None
                )

                if (
                    not seller_profile
                    or seller_profile.approval_status != 'APPROVED'
                ):

                    return render(
                        request,
                        'accounts/login.html',
                        {
                            'error':
                            'Your seller account is waiting for admin approval.'
                        }
                    )

            # Login user
            login(request, user)

            # Admin
            if user.role == 'ADMIN':
                return redirect('/admin/')

            # Buyer and approved Seller
            return redirect('/')

        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )


def home(request):

    products = Product.objects.filter(
        status='ACTIVE'
    )

    return render(
        request,
        'home.html',
        {
            'products': products
        }
    )