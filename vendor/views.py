from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from . forms import VendorForm,OpeningHourForm
from accounts.forms import UserProfileForm
from . models import Vendor,OpeningHour
from accounts.models import UserProfile
from django.contrib import messages

from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.views import check_role_vendor
from menu.models import Category,FoodItem
from menu.forms import CategoryForm,FoodItemForm
from django.template.defaultfilters import slugify

import json
from django.db.utils import IntegrityError
from datetime import datetime
from json.decoder import JSONDecodeError

def get_vendor(request):
    vendor = Vendor.objects.get(user=request.user)
    return vendor


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    vendor = get_object_or_404(Vendor,user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form = VendorForm(request.POST,request.FILES,instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'Settings updated.')
            return redirect('vprofile')
        else:
            # messages.error(request,'')
            print(profile_form.errors)
            print(vendor_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)

    context = {
        "profile_form":profile_form,
        "vendor_form":vendor_form,
        "profile":profile,
        "vendor":vendor,
    }
    return render(request,'vendor/vprofile.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request,'vendor/menu_builder.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category,pk=pk)
    fooditems = FoodItem.objects.filter(vendor=vendor,category=category)
    context = {
        'fooditems': fooditems,
        'category' : category,
    }
    return render(request,'vendor/fooditems_by_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.save() #category id generated
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request,'Category added successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form' : form,
    }
    return render(request,'vendor/add_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('menu_builder')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form' : form,
        'category' : category,
    }
    return render(request,'vendor/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None):
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    messages.success(request,'Category has been deleted successfully!')
    return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.save() #food id generated
            food.slug = slugify(food_title)+'-'+str(food.id)
            food.save()
            messages.success(request,'Food item added successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
        #Modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form' : form,
    }
    return render(request,'vendor/add_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_food(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            food_title = form.cleaned_data['food_title']
            food = form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            form.save()
            messages.success(request,'Category updated successfully!')
            return redirect('fooditems_by_category',food.category.id)
        else:
            print(form.errors)
    else:
        form = FoodItemForm(instance=food)
        #Modify this form
        form.fields['category'].queryset = Category.objects.filter(vendor = get_vendor(request))
    context = {
        'form' : form,
        'food' : food,
    }
    return render(request,'vendor/edit_food.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_food(request,pk=None):
    food = get_object_or_404(FoodItem,pk=pk)
    food.delete()
    messages.success(request,'Food Item has been deleted successfully!')
    return redirect('fooditems_by_category',food.category.id)


def opening_hour(request):
    opening_hours = OpeningHour.objects.filter(vendor = get_vendor(request))
    form = OpeningHourForm()
    context = {
        'form':form,
        'opening_hours':opening_hours,
    }
    return render(request,'vendor/opening_hour.html',context)


def add_opening_hours(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if request.method == "POST":
                try:
                    data = json.loads(request.body)  # Parse JSON data
                    day = data.get('day')
                    from_hour = data.get('from_hour')
                    to_hour = data.get('to_hour')
                    is_closed = str(data.get('is_closed')).lower() == 'true'

                    hour = OpeningHour.objects.create(vendor=get_vendor(request),day=day,from_hour=from_hour,to_hour=to_hour,is_closed=is_closed)
                    if hour:
                        day = OpeningHour.objects.get(id=hour.id)
                        if day.is_closed:
                            return JsonResponse({"success":True, 'id':hour.id,'day':day.get_day_display(),'is_closed':'Closed'})
                        else:
                            return JsonResponse({"success":True, 'id':hour.id,'day':day.get_day_display(),'from_hour':hour.from_hour,'to_hour':hour.to_hour})
                    
                except IntegrityError:
                    return JsonResponse({"success": False, "error": from_hour+'-'+to_hour+' already exists for this day!'})
                except JSONDecodeError:
                    return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)
            else:
                return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
        else:
            return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
    else:
        return JsonResponse({"success": False, "error": "User is not authenticated"}, status=403)
    

def remove_opening_hours(request,pk=None):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            hour = get_object_or_404(OpeningHour,pk=pk)
            hour.delete()
            return JsonResponse({'status':'success','id':pk})