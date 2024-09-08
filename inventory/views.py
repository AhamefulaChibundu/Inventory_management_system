from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category, Sale
from .forms import ItemForm, UserRegistrationForm, UserLoginForm, SaleForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from django.db.models import Sum, F

@login_required
def total_inventory_value(request):
    total_value = Item.objects.filter(user=request.user, is_deleted=False).aggregate(
        total_value=Sum(F('price'))
    )['total_value'] or 0
    return render(request, 'inventory/total_inventory_value.html', {'total_value': total_value})

@login_required
def inventory_by_category(request):
    category_totals = Item.objects.filter(user=request.user, is_deleted=False).values('category__name').annotate(
        total_quantity=Sum('quantity'),
        total_value=Sum(F('price') * F('quantity'))
    )
    return render(request, 'inventory/inventory_by_category.html', {'category_totals': category_totals})

@login_required
def low_stock_notifications(request):
    items = Item.objects.filter(
        user=request.user,
        is_deleted=False,
        quantity__lte=6
    )
    return render(request, 'inventory/low_stock_notifications.html', {'items': items})

@login_required
def expiry_notifications(request):
    today = timezone.now().date()
    items = Item.objects.filter(
        user=request.user,
        is_deleted=False,
        expiry_date__lte=today
    )
    return render(request, 'inventory/expiry_notifications.html', {'items': items})

@login_required
def item_list(request):
    # Get search query and category filter from the request
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    # Filter items by the logged-in user, search query, and category filter
    items = Item.objects.filter(user=request.user, is_deleted=False)

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_filter:
        items = items.filter(category__name=category_filter)

    # Get all categories for filtering dropdown
    categories = Category.objects.all()

    return render(request, 'inventory/item_list.html', {
        'items': items,
        'query': query,
        'category_filter': category_filter,
        'categories': categories,
    })

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user, is_deleted=False)  # Ensure item belongs to the user
    return render(request, 'inventory/item_detail.html', {'item': item})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()  # Total price is calculated in the model's save() method
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_update(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user, is_deleted=False)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()  # Total price is recalculated in the model's save() method
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form})


@login_required
def item_delete(request, item_id):
    item = get_object_or_404(Item, id=item_id, user=request.user)  # Ensure item belongs to the user
    if request.method == 'POST':
        item.is_deleted = True  # Mark as deleted
        item.save()
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def record_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user  # Assign the sale to the logged-in user
            sale.sale_date = timezone.now()  # Set the current date and time
            sale.total_price = sale.quantity * sale.item.unit_price  # Calculate the total price

            # Reduce the quantity of the item in stock
            item = sale.item
            if item.quantity >= sale.quantity:
                item.quantity -= sale.quantity
                item.save()
                sale.save()  # Save the sale after adjusting the item's quantity
                return redirect('sales_history')
            else:
                form.add_error('quantity', 'Not enough stock to complete the sale')
    else:
        form = SaleForm()

    return render(request, 'inventory/record_sale.html', {'form': form})

@login_required
def sales_history(request):
    sales = Sale.objects.filter(user=request.user).order_by('-sale_date')
    return render(request, 'inventory/sales_history.html', {'sales': sales})

