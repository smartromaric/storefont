from django.shortcuts import render
from django.db.models import Q, F, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Max, Count, Sum, Min, Avg, Value, Func
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Product, Customer, Collection, Order, OrderItem
from tags.models import Tagged_Item


# Create your views here.
def say_hello(request):
    orders = Order.objects.prefetch_related("orderitem_set__product").select_related("customer")[:5]
    products = Product.objects.filter(id__in=OrderItem.objects.values("product_id")).distinct().order_by("title")
    # products = Product.objects.filter(Q(unit_price__gt = 10) | Q(inventory__lt=20)).latest("title")
    # produit = OrderItem.objects.filter(order__payment_status = "C").values("product__title").order_by("product__title")
    # produit = Product.objects.only("title","id").filter(id__in=OrderItem.objects.values("product__id").distinct()).order_by("title")
    # only() != refer() mean eject
    # customer = Customer.objects.annotate(full_name = Concat("first_name",Value(" "),"last_name"))
    customer = Customer.objects.annotate(full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT"))
    # produit = Product.objects.filter(inventory__lt = 10).latest("title")
    # produit = Product.objects.filter(Q(inventory__lt = 10) | ~Q(unit_price__lt=20)) #~ mean not eq
    # produit = Product.objects.filter(Q(id = F("collection_id")) & Q(title__icontains="Sh")) #F for commparin two field
    # customers = Customer.objects.filter(email__icontains='.com')
    # collections = Collection.objects.filter(featured_product_id__isnull =True )
    orders = Order.objects.select_related("customer").prefetch_related("orderitem_set__product").order_by("-placed_at")[
             :5]
    # nbr_ord = Order.objects.filter(payment_status="C").aggregate(Sum("orderitem__quantity"))
    # nbr_ord = OrderItem.objects.filter(product__id=1).aggregate(Sum("quantity"))
    # nbr_ord = Order.objects.filter(customer__id=1).aggregate(Count("id"))
    # nbr_ord = Product.objects.filter(collection__id=3).annotate(new_id=F("id")+1).aggregate(Min("unit_price"),Avg("unit_price"),Max("unit_price"))
    # nbr_ord = Product.objects.filter(collection__id=3).aggregate(Min("unit_price"),Avg("unit_price"),Max("unit_price"))
    nbr_ord = Customer.objects.annotate(
        count_order=Count("order")
    )
    discount = ExpressionWrapper(F("unit_price") * 0.5, output_field=DecimalField())
    Discount_prod = Product.objects.annotate(
        discount=discount
    )
    # prod = ContentType.objects.get_for_model(Product) # takin product table raw from content_type
    tag_items = Tagged_Item.objects.get_tag_for(Product,1)
    # c1 = Collection()
    # c1.title ="Video game"
    # c1.save()
    # print(c1.id,"is create")
    # c2 = Collection.object.create(title = )

    Collection.objects.filter(pk=1).update(featured_product=1)

    # orderItems = OrderItem.objects.filter(product__collection__id = 3)
    return render(request, "hello.html",
                  context={"produit": list(orders), "customer": list(customer), "nbr_ord": nbr_ord,
                           "discount": list(tag_items),"prod":orders})
