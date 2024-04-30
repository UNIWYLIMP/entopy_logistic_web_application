import random as ran
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
import django.core.mail as mailer
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.models import auth, User
from .models import *
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request, "index.html")


def login(request):
    return render(request, "login.html")


def login_authenticate(request):
    if request.method == 'GET':
        identity = request.GET.get('email')
        password = request.GET.get('password')
        message = ""
        print(identity)
        print(password)
        user = auth.authenticate(username=identity, password=password)
        print(user)
        print(CustomUser.objects.get(email=identity).password)
        if user is not None:
            user_con = CustomUser.objects.get(email=identity)
            auth.login(request, user_con)
            email_id = identity
            message = "success"
            request.session['userId'] = email_id
            request.session['userStatus'] = CustomUser.objects.get(email=email_id).status
            message = "success"
            return JsonResponse({"message": message})

        else:
            message = "Invalid Details"
            return JsonResponse({"message": message})
    else:
        return redirect("/login")


def user_register(request):
    return render(request, "register-user.html")


def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST["email"]
        fullname = request.POST["fullname"]
        password = request.POST["password"]
        password_one = request.POST["password_one"]
        status = "user"
        if CustomUser.objects.filter(email=email).exists():
            message = "Email Already In Use."
            return JsonResponse({"message": message})

        elif fullname == "" or fullname == " ":
            message = "Fill All Details"
            return JsonResponse({"message": message})

        elif password != password_one:
            message = "Password Does Not Match"
            return JsonResponse({"message": message})

        else:
            username = str(fullname).split(" ")[0] + str(ran.randint(0, 3784894303))
            user = CustomUser.objects.create_user(email=email, username=username, fullname=fullname, status=status,
                                                  password=password)
            user.save()
            auth.login(request, user)

            request.session['userId'] = email
            request.session['userStatus'] = status

            message = "success"
            return JsonResponse({"messages": message})
    else:
        return redirect("/")


def company_register(request):
    return render(request, "register-company.html")


def authenticate_company(request):
    if request.method == 'POST':
        email = request.POST["email"]
        fullname = request.POST["fullname"]
        password = request.POST["password"]
        password_one = request.POST["password_one"]
        company_location = request.POST["company_location"]
        working_days = request.POST["working_days"]
        policies = request.POST["policies"]
        status = "company"
        if CustomUser.objects.filter(email=email).exists():
            message = "Email Already In Use."
            return JsonResponse({"message": message})

        elif fullname == "" or fullname == " ":
            message = "Fill All Details"
            return JsonResponse({"message": message})

        elif password != password_one:
            message = "Password Does Not Match"
            return JsonResponse({"message": message})

        else:
            username = str(fullname).split(" ")[0] + str(ran.randint(0, 3784894303))
            user = CustomUser.objects.create_user(email=email, username=username, fullname=fullname, status=status,
                                                  password=password)
            user.save()
            auth.login(request, user)

            new_company = DeliveryCompany(profile=user, email=email, username=username, fullname=fullname,
                                          company_location=company_location, working_days=working_days,
                                          policies=policies)
            new_company.save()

            request.session['userId'] = email
            request.session['userStatus'] = status

            message = "success"
            return JsonResponse({"messages": message})
    else:
        return redirect("/")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/user_dashboard")
    elif request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")
    else:
        auth.logout(request)
        return redirect('/login')


def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    orders = Order.objects.filter(user=user)
    if len(orders) <= 5:
        pass
    else:
        orders = orders[:5]
    pending_orders = 0
    processing_orders = 0
    successful_orders = 0
    for x in orders:
        if x.status == "pending":
            pending_orders += 1
        elif x.status == "processing":
            processing_orders += 1
        elif x.status == "successful":
            successful_orders += 1

    print(user_email)
    return render(request, "dashboard-user.html", {"fullname": user.fullname, "email": user_email,
                                                   "status": request.session.get('userStatus'), "orders": orders,
                                                   "order_count": len(orders), "pending_orders": pending_orders,
                                                   "processing_orders": processing_orders, "successful_orders":
                                                       successful_orders})


def company_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/company_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    company = DeliveryCompany.objects.get(profile=user)
    orders = Order.objects.filter(company=company)
    if len(orders) <= 5:
        pass
    else:
        orders = orders[:5]
    pending_orders = 0
    processing_orders = 0
    successful_orders = 0
    for x in orders:
        if x.status == "pending":
            pending_orders += 1
        elif x.status == "processing":
            processing_orders += 1
        elif x.status == "successful":
            successful_orders += 1

    print(user_email)
    destinations = DeliveryDestination.objects.filter(company=company)
    return render(request, "dashboard-company.html", {"fullname": user.fullname, "email": user_email,
                                                      "status": request.session.get('userStatus'), "orders": orders,
                                                      "order_count": len(orders), "pending_orders": pending_orders,
                                                      "processing_orders": processing_orders, "successful_orders":
                                                          successful_orders, "company": company, "destinations":
                                                          destinations, "destination_count": len(destinations)})


def all_orders(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    orders = Order.objects.filter(user=user)
    print(user_email)
    return render(request, "dashboard-user-deliveries.html", {"fullname": user.fullname, "email": user_email,
                                                              "status": request.session.get('userStatus'),
                                                              "orders": orders,
                                                              "order_count": len(orders)})


def user_book(request):
    request.session['book_status'] = "not_booked"
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")

    if request.method == "POST":
        pass
    else:
        request.session['book_status'] = "not_booked"
        user_email = request.session.get("userId")
        user = CustomUser.objects.get(email=user_email)
        return render(request, "user-book.html", {"fullname": user.fullname, "email": user_email,
                                                  "status": request.session.get('userStatus')})


def company_search(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")

    if request.method == "POST":
        if request.session['book_status'] != "not_booked":
            return redirect("/book")

        request.session['book_status'] = "not_booked"
        user_email = request.session.get("userId")
        user = CustomUser.objects.get(email=user_email)
        request.session['fullname'] = str(request.POST['first_name']) + " " + str(request.POST['last_name'])
        request.session['delivery_address'] = request.POST['delivery_address']
        request.session['delivery_city'] = str(request.POST['delivery_city'])
        request.session['delivery_country'] = str(request.POST['delivery_country']).lower()
        request.session['current_address'] = request.POST['current_address']
        request.session['current_city'] = str(request.POST['current_city']).lower()
        request.session['current_country'] = str(request.POST['current_country']).lower()
        request.session['package_weight'] = request.POST['package_weight']
        request.session['delivery_nature'] = request.POST['delivery_nature']
        request.session['product_summary'] = request.POST['product_summary']
        request.session['product_name'] = request.POST['product_name']

        # Search for companies
        available_logistics = DeliveryDestination.objects.filter(Q(one_country=request.POST['delivery_country'],
                                                                   two_country=request.POST['current_country'])
                                                                 | Q(one_country=request.POST['current_country'],
                                                                     two_country=request.POST[
                                                                         'delivery_country'])).exists()
        logistics_company = DeliveryDestination.objects.filter(Q(one_country=request.POST['delivery_country'],
                                                                 two_country=request.POST['current_country'])
                                                               | Q(one_country=request.POST['current_country'],
                                                                   two_country=request.POST['delivery_country']))
        print(logistics_company)
        print(available_logistics)
        company_list = []
        water = 0
        land = 0
        air = 0
        if available_logistics:
            print("I got here")
            for x in logistics_company:
                if (str(request.POST['current_city']).lower() in x.one_cities and str(
                        request.POST['delivery_city']).lower() in x.two_cities) or (
                        str(request.POST['current_city']).lower() in x.two_cities and str(
                        request.POST['delivery_city']).lower() in x.one_cities):
                    data = {
                        "company_name": x.company.fullname,
                        "company_id": x.id,
                        "Cost": float(x.rate) * float(request.POST['package_weight']),
                        "package_weight": request.POST['package_weight'],
                        "delivery_country": request.POST['delivery_country'],
                        "delivery_city": request.POST['delivery_city'],
                        "current_city": request.POST['current_city'],
                        "current_country": request.POST['current_country'],
                        "mod": x.mode_of_delivery
                    }
                    company_list.append(data)
                    if x.mode_of_delivery == "water":
                        water += 1
                    elif x.mode_of_delivery == "land":
                        land += 1
                    elif x.mode_of_delivery == "air":
                        air += 1
                    else:
                        pass
                elif (x.one_cities == "all" and str(request.POST['delivery_city']).lower() in x.two_cities) or (
                        x.one_cities == "all" and str(request.POST['current_city']).lower() in x.two_cities):
                    data = {
                        "company_name": x.company.fullname,
                        "company_id": x.id,
                        "Cost": float(x.rate) * float(request.POST['package_weight']),
                        "package_weight": request.POST['package_weight'],
                        "delivery_country": request.POST['delivery_country'],
                        "delivery_city": request.POST['delivery_city'],
                        "current_city": request.POST['current_city'],
                        "current_country": request.POST['current_country'],
                        "mod": x.mode_of_delivery
                    }
                    company_list.append(data)
                    if x.mode_of_delivery == "water":
                        water += 1
                    elif x.mode_of_delivery == "land":
                        land += 1
                    elif x.mode_of_delivery == "air":
                        air += 1
                    else:
                        pass

                elif (x.two_cities == "all" and str(request.POST['delivery_city']).lower() in x.one_cities) or (
                        x.two_cities == "all" and str(request.POST['current_city']).lower() in x.one_cities):
                    data = {
                        "company_name": x.company.fullname,
                        "company_id": x.id,
                        "cost": float(x.rate) * float(request.POST['package_weight']),
                        "package_weight": request.POST['package_weight'],
                        "delivery_country": request.POST['delivery_country'],
                        "delivery_city": request.POST['delivery_city'],
                        "current_city": request.POST['current_city'],
                        "current_country": request.POST['current_country'],
                        "mod": x.mode_of_delivery
                    }
                    company_list.append(data)
                    if x.mode_of_delivery == "water":
                        water += 1
                    elif x.mode_of_delivery == "land":
                        land += 1
                    elif x.mode_of_delivery == "air":
                        air += 1
                    else:
                        pass

                elif x.two_cities == "all" and x.one_cities == "all":
                    data = {
                        "company_name": x.company.fullname,
                        "company_id": x.id,
                        "cost": float(x.rate) * float(request.POST['package_weight']),
                        "package_weight": request.POST['package_weight'],
                        "delivery_country": request.POST['delivery_country'],
                        "delivery_city": request.POST['delivery_city'],
                        "current_city": request.POST['current_city'],
                        "current_country": request.POST['current_country'],
                        "mod": x.mode_of_delivery
                    }
                    company_list.append(data)
                    if x.mode_of_delivery == "water":
                        water += 1
                    elif x.mode_of_delivery == "land":
                        land += 1
                    elif x.mode_of_delivery == "air":
                        air += 1
                    else:
                        pass

                else:
                    pass

        else:
            pass
        return render(request, "user-search.html",
                      {"fullname": user.fullname, "company_count": len(company_list), "companies": company_list,
                       "air": air, "water": water, "land": land})
    else:
        pass


def successfully_booked(request, company_id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "company":
        return redirect("/company_dashboard")
    email = request.session.get("userId")
    user = CustomUser.objects.get(email=email)

    delivery = DeliveryDestination.objects.get(id=company_id)
    new_order = Order(product_name=request.session.get('product_name'),
                      product_description=request.session.get('product_summary'),
                      amount_paid=(delivery.rate * float(request.session.get('package_weight'))),
                      weight=request.session.get('package_weight'), status="pending", company=delivery.company,
                      user=user)
    new_order.save()
    request.session['book_status'] = "booked"
    return render(request, "user-booked.html", {"fullname": user.fullname, "order_id": f"#ENTOPY-{new_order.id}"})


def new_location(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    email = request.session.get("userId")
    user = CustomUser.objects.get(email=email)

    if request.method == "POST":
        cities_one = str(request.POST['cities_one']).lower()
        country_one = str(request.POST['country_one']).lower()
        cities_two = str(request.POST['cities_two']).lower()
        country_two = str(request.POST['country_two']).lower()
        rate = request.POST['rate']
        mod = request.POST['delivery_nature']

        company = DeliveryCompany.objects.get(profile=user)
        orders = Order.objects.filter(company=company)

        new_dest = DeliveryDestination(company=company, one_cities=cities_one, one_country=country_one, two_cities=cities_two,
                            two_country=country_two, mode_of_delivery=mod, rate=rate)
        new_dest.save()

        return redirect("/dashboard")
    else:
        return render(request, "company-location.html", {"fullname": user.fullname})


def delete_destination(request, dest_id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    destination = DeliveryDestination.objects.get(id=dest_id)
    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)

    company = DeliveryCompany.objects.get(profile=user)
    if destination.company == company:
        destination.delete()
    else:
        pass
    return redirect("/dashboard")


def pending_orders(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    company = DeliveryCompany.objects.get(profile=user)

    orders = Order.objects.filter(company=company, status="pending")
    return render(request, "company-pending.html", {"orders": orders, "order_count": len(orders)})


def process_pending(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    company = DeliveryCompany.objects.get(profile=user)

    order = Order.objects.get(id=order_id)

    if order.status == "pending":
        if order.company == company:
            order.status = "processing"
            order.save()
        else:
            pass
    else:
        pass
    return redirect("/pending_orders")


def processing_orders(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    company = DeliveryCompany.objects.get(profile=user)

    orders = Order.objects.filter(company=company, status="processing")
    return render(request, "company-processing.html", {"orders": orders, "order_count": len(orders)})


def processed_orders(request):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    company = DeliveryCompany.objects.get(profile=user)

    orders = Order.objects.filter(company=company, status="successful")
    return render(request, "company-processed.html", {"orders": orders, "order_count": len(orders)})


def process_processing(request, order_id):
    if not request.user.is_authenticated:
        return redirect("/")

    if not request.session.get('userId', None):
        auth.logout(request)
        return redirect('/login')

    if request.session.get('userStatus') == "user":
        return redirect("/dashboard")

    user_email = request.session.get("userId")
    user = CustomUser.objects.get(email=user_email)
    company = DeliveryCompany.objects.get(profile=user)

    order = Order.objects.get(id=order_id)

    if order.status == "processing":
        if order.company == company:
            order.status = "successful"
            order.save()
        else:
            pass
    else:
        pass
    return redirect("/processing_orders")


def logout(request):
    auth.logout(request)
    return redirect('/login')


def error_404(request, exception):
    return render(request, "error-404.html", {"error_code": "404"})


def error_505(request, exception):
    return render(request, "error-404.html", {"error_code": "505"})


def error_500(request):
    return render(request, "error-404.html", {"error_code": "500"})


def error_403(request):
    return render(request, "error-404.html", {"error_code": "403"})
