from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart  # якщо у вас є кошик як клас Cart
from django.contrib import messages
from django.http import JsonResponse
from .nova_poshta_api import get_np_cities, get_np_warehouses
from .ukrposhta_api import get_up_cities, get_up_warehouses



def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Перевірка, які поля заповнювати в залежності від методу доставки
            method = form.cleaned_data['delivery_method']

            if method == 'pickup':
                order.city = ''
                order.address = ''
                order.postal_code = ''
                order.nova_poshta_city = ''
                order.nova_poshta_warehouse = ''
                order.ukrposhta_city = ''
                order.ukrposhta_warehouse = ''

            elif method == 'courier':
                if not (order.city and order.address and order.postal_code):
                    messages.error(request, "Для кур'єрської доставки потрібно заповнити адресу, місто та поштовий код.")
                    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})

                order.nova_poshta_city = ''
                order.nova_poshta_warehouse = ''
                order.ukrposhta_city = ''
                order.ukrposhta_warehouse = ''

            elif method == 'nova_poshta':
                if not (order.nova_poshta_city and order.nova_poshta_warehouse):
                    messages.error(request, "Оберіть місто та відділення Нової Пошти.")
                    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})

                order.city = ''
                order.address = ''
                order.postal_code = ''
                order.ukrposhta_city = ''
                order.ukrposhta_warehouse = ''

            elif method == 'ukrposhta':
                if not (order.ukrposhta_city and order.ukrposhta_warehouse):
                    messages.error(request, "Оберіть місто та відділення Укрпошти.")
                    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})

                order.city = ''
                order.address = ''
                order.postal_code = ''
                order.nova_poshta_city = ''
                order.nova_poshta_warehouse = ''

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_variant=item['variant'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()
            messages.success(request, "Ваше замовлення успішно створено!")
            return redirect('orders:order_success')  # додайте цю сторінку

    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})


def order_success(request):
    return render(request, 'orders/order_success.html')


def nova_poshta_cities(request):
    query = request.GET.get('q', '').lower()
    cities = get_np_cities()

    # Витягуємо тільки потрібні поля: Description і Ref
    result = [
        {'Description': city.get('Description'), 'Ref': city.get('Ref')}
        for city in cities
        if query in city.get('Description', '').lower()
    ]
    return JsonResponse(result, safe=False)


def nova_poshta_warehouses(request):
    city_ref = request.GET.get('city_ref')
    if not city_ref:
        return JsonResponse([], safe=False)

    warehouses = get_np_warehouses(city_ref)

    result = [
        {'Description': wh.get('Description'), 'Ref': wh.get('Ref')}
        for wh in warehouses
    ]
    return JsonResponse(result, safe=False)


def ukrposhta_cities(request):
    query = request.GET.get('q', '').lower()
    cities = get_up_cities()

    result = [
        {'city': city.get('city'), 'id': city.get('id')}
        for city in cities
        if query in city.get('city', '').lower()
    ]
    return JsonResponse(result, safe=False)


def ukrposhta_warehouses(request):
    city_id = request.GET.get('city_id')
    if not city_id:
        return JsonResponse([], safe=False)

    warehouses = get_up_warehouses(city_id)

    result = [
        {'name': wh.get('name') or wh.get('address'), 'id': wh.get('id')}
        for wh in warehouses
    ]
    return JsonResponse(result, safe=False)