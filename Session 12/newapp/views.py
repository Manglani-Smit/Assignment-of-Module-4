from django.shortcuts import render, redirect, get_object_or_404
from .models import Product


def product_create(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST.get('name'),
            price=request.POST.get('price'),
            category=request.POST.get('category'),
        )
        return redirect('product_list')
    return render(request, 'product_add.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_edit(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category')
        product.save()
        return redirect('product_list')

    return render(request, 'product_form.html', {'product': product})


def product_delete(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'product_confirm_delete.html', {'product': product})