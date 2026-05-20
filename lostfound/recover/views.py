

from django.shortcuts import  get_object_or_404, render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get("confirm_password")
        if password != confirm_password:
            messages.error(request,'password doesnt match')
            return render(request,'signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already taken')
            return redirect('signup')
        user=User.objects.create_user(username=name,email=email,password=password)
        user.save()
        messages.success(request,"Registration Successful")
        return redirect('login')
    return render(request,"signup.html")
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'error':'Invalid username or password'})
    return render(request,'login.html')

def home(request):
    recent_found_items = Item.objects.filter(status='FOUND',is_approved=True).order_by('-created_at')[:4]

    recent_lost_items = Item.objects.filter(status='LOST',is_approved=True).order_by('-created_at')[:4]

    context = {'recent_found_items': recent_found_items,
              'recent_lost_items': recent_lost_items}
    return render(request, 'home.html', context)

@login_required

def reportfound(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date_found = request.POST.get('date_found')
        image = request.FILES.get('image')

        Item.objects.create(
            title=title,
            description=description,
            location=location,
            found_date=date_found,
            image=image,
            user=request.user,
            status='FOUND')
        return redirect('found_items')

    return render(request,'reportfound.html')
@login_required
def reportlost(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        date_lost= request.POST.get('date_lost')
        image = request.FILES.get('image')

        Item.objects.create(
            title=title,
            description=description,
            location=location,
            image=image,
            lost_date=date_lost,
            status='LOST',
            user=request.user  ) # ✅ important
        
        return redirect('lost_items')
    return render(request,'reportlost.html')

@login_required
def claim_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == "POST":
        message = request.POST.get('message')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')
        Claim.objects.create(
            item=item,
            user=request.user,
            message=message,
            contact=contact,
            image=image
        )
        
        return redirect('home')

    return render(request, 'claim_item.html', {'item': item})
def user_logout(request):
    if request.method=="POST":
      logout(request)
      return redirect('home')
    context={'message':'Are you sure you want to logout?',
            'button_text':'yes,logout',
            'cancel_url':reverse('home')}
    return render(request,'confirm_item.html',context)


def lost_items(request):
     
    location_query = request.GET.get('location')
    items = Item.objects.filter(status='LOST', is_approved=True).order_by('-id')
    newitems = None
    if location_query:
        newitems = items.filter(location__icontains=location_query)
    else:
        newitems=Item.objects.none()
    items=items.exclude(id__in=newitems.values_list('id', flat=True))
    context = {
        'items': items,
        'newitems':newitems}
    return render(request, 'lost_items.html', context)

def found_items(request):
    location_query = request.GET.get('location')
    items = Item.objects.filter(status='FOUND', is_approved=True).order_by('-id')
    newitems = None
    if location_query:
        newitems = items.filter(location__icontains=location_query)
    else:
        newitems=Item.objects.none()
    items=items.exclude(id__in=newitems.values_list('id', flat=True))
    context = {
        'items': items,
        'newitems':newitems}
    return render(request, 'found_items.html', context)
# DETAIL VIEW
def item_detail(request, id):
    items = get_object_or_404(Item, id=id)
    approve_claim= Claim.objects.filter(item=items, is_approved=True).exists()
    context= {'item': items ,
             'approve_claim':approve_claim}
    return render(request, 'item_detail.html', context)
# EDIT VIEW
@login_required
def edit_item(request, id ,type):
    item = get_object_or_404(Item, id=id,)

    if request.user != item.user:
        return redirect('home')

    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.location = request.POST.get('location')
        if type == 'LOST':
            item.lost_date= request.POST.get('lost_date')
        elif type == 'FOUND':
             item.found_date= request.POST.get('found_date') 
             if request.FILES.get('image'):
                 item.image=request.FILES.get('image')
        item.save()
        return redirect('lostitem_detail', id=item.id)

    return render(request, 'edit_item.html', {'item': item,'type':type})


# DELETE VIEW
@login_required
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)

    if request.user != item.user:
        return redirect('home')

    if request.method == 'POST':
        item.delete()
        return redirect('home')
    context={'message':'Are you sure you want to delete?',
            'button_text':'yes,Delete',
            'cancel_url':reverse('item_detail',args=[item.id]),
            'item':item}
    return render(request, 'confirm_item.html', context)
def mydetails(request):
    user = request.user

    # User added lost items
    lost_items = Item.objects.filter(user=user, status='LOST')

    # User added found items
    found_items = Item.objects.filter(user=user, status='FOUND')

    # User claims
    claims = Claim.objects.filter(user=user)

    context = {
        'lost_items': lost_items,
        'found_items': found_items,
        'claims': claims
    }
    return render(request,'mydetails.html',context)

@staff_member_required
def admin_items(request):
    items = Item.objects.all().order_by('-created_at')
    claimed_items=Claim.objects.all().order_by('-created_at')
    return render(request, 'admin_items.html', {'items': items,'claimed_items':claimed_items})
@staff_member_required
def approve_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.is_approved = True
    item.save()
    return redirect('admin_items')


@staff_member_required
def reject_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.is_approved = False
    item.save()
    return redirect('admin_items')


@staff_member_required
def delete_item(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    return redirect('admin_items')


@staff_member_required
def approve_claim(request, id):
    claim = get_object_or_404(Claim, id=id)
    claim.is_approved = True
    claim.save()
    return redirect('admin_items')


@staff_member_required
def reject_claim(request, id):
    claim = get_object_or_404(Claim, id=id)
    claim.is_approved = False
    claim.save()
    return redirect('admin_items')


@staff_member_required
def delete_claim(request, id):
    claim= get_object_or_404(Claim, id=id)
    claim.delete()
    return redirect('admin_items')