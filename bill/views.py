from datetime import datetime
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from decimal import Decimal
from num2words import num2words


def demo(request):
    return render(request, 'demo.html')


def index(request):
    return render(request, 'index.html')


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login_page.html')


@login_required(login_url="/login_page/")
def logout_page(request):
    logout(request)
    return redirect('/')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        email = request.POST.get('email')

        if password != cpassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'register.html')

        User.objects.create_user(
            username=username, password=password, email=email)

        messages.success(
            request, "Registration successful. You can now log in.")

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('setup_profile')

    return render(request, 'register.html')


@login_required(login_url="/login_page/")
def delete_account(request, pk):
    user = User.objects.get(id=pk)
    profile = Profile.objects.get(id=1)
    user.delete()
    profile.delete()
    return redirect('login_page')


@login_required(login_url="/login_page/")
def setup_profile(request):
    if Profile.objects.filter(user=request.user).exists():
        return redirect('home')

    if request.method == "POST":
        name = request.POST.get('c_name').upper()
        gst = request.POST.get('gst').upper()
        adrs = request.POST.get('adrs')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        email = request.POST.get('c_email')

        bank_name = request.POST.get('bank_name').upper()
        acno = request.POST.get('acno')
        bank_branch = request.POST.get('bank_branch')
        bank_ifsc = request.POST.get('bank_ifsc').upper()

        bank_obj = Bank(
            user=request.user,
            name=bank_name,
            acno=acno,
            ifsc=bank_ifsc,
            branch=bank_branch,
            bal=0.00
        )
        bank_obj.save()

        # bank=Bank.objects.get(id=1)

        # Create the profile
        profile = Profile(
            user=request.user,
            name=name,
            gst=gst,
            adrs=adrs,
            city=city,
            state=state,
            phone=phone,
            email=email,
            bank=bank_obj,
            bal=Decimal(0.00)
        )
        profile.save()

        messages.success(request, "Profile setup successful.")
        return redirect('login_page')

    return render(request, 'setup_profile.html')


@login_required(login_url="/login_page/")
def view_profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'view_profile.html', {"profile": profile})


@login_required(login_url="/login_page/")
def update_profile(request):
    # Get the profile of the logged-in user
    profile = Profile.objects.get(user=request.user)
    bank = Bank.objects.filter(user=request.user)

    if request.method == 'POST':
        c_name = request.POST.get('c_name').upper()
        gst = request.POST.get('gst').upper()
        adrs = request.POST.get('adrs')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        c_email = request.POST.get('c_email')
        bill_count = request.POST.get('bill_count')
        bank_id = request.POST.get('bank')

        bank = Bank.objects.get(id=bank_id)

        profile.name = c_name
        profile.gst = gst
        profile.adrs = adrs
        profile.city = city
        profile.state = state
        profile.phone = phone
        profile.email = c_email
        profile.bill_count = bill_count
        profile.bank = bank
        profile.save()
        return redirect('view_profile')  # Redirect to home or another page

    return render(request, 'update_profile.html', {'profile': profile, "bank": bank})


@login_required(login_url="/login_page/")
def home(request):
    if not Profile.objects.filter(user=request.user).exists():
        return redirect('setup_profile')
    return render(request, 'home.html')


@login_required(login_url="/login_page/")
def customer_create(request):
    if request.method == "POST":
        name = request.POST.get('name').upper()
        gst = request.POST.get('gst').upper()
        adrs = request.POST.get('adrs')
        city = request.POST.get('city')
        state = request.POST.get('state').upper()
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        customer = Customer(
            user=request.user,
            name=name,
            gst=gst,
            adrs=adrs,
            city=city,
            state=state,
            phone=phone,
            email=email,
            bal=Decimal(0.00)
        )
        customer.save()
        return redirect('customer_read')

    return render(request, 'customer_create.html')


@login_required(login_url="/login_page/")
def customer_read(request):
    customer = Customer.objects.filter(user=request.user)
    if not customer.exists():
        messages.info(request, 'No Customer Found')
    return render(request, 'customer_read.html', {"customer": customer})


@login_required(login_url="/login_page/")
def customer_update(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        name = request.POST.get('name').upper()
        gst = request.POST.get('gst').upper()
        adrs = request.POST.get('adrs')
        city = request.POST.get('city')
        state = request.POST.get('state').upper()
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if not all([name, gst, adrs, city, state, phone]):
            messages.error(request, 'All fields are required.')
        else:
            customer.name = name
            customer.gst = gst
            customer.adrs = adrs
            customer.city = city
            customer.state = state
            customer.phone = phone
            customer.email = email
            customer.save()
            return redirect('customer_read')

    return render(request, 'customer_update.html', {'customer': customer})


@login_required(login_url="/login_page/")
def customer_delete(request, pk):
    customer = Customer.objects.filter(id=pk)
    customer.delete()
    return redirect('customer_read')


@login_required(login_url="/login_page/")
def customer_statement(request, pk):
    invoice_s = Invoice.objects.filter(invoice_to=pk).order_by('-date')
    total_s = sum(i.grand_total for i in invoice_s)
    total_ssg = sum(i.sgst_amt for i in invoice_s)
    total_scg = sum(i.cgst_amt for i in invoice_s)
    total_sig = sum(i.igst_amt for i in invoice_s)
    total_stg = sum(i.tgst_amt for i in invoice_s)
    invoice_p = InvoicePurchase.objects.filter(invoice_to=pk).order_by('-date')
    total_p = sum(i.grand_total for i in invoice_p)
    total_psg = sum(i.sgst_amt for i in invoice_p)
    total_pcg = sum(i.cgst_amt for i in invoice_p)
    total_pig = sum(i.igst_amt for i in invoice_p)
    total_ptg = sum(i.tgst_amt for i in invoice_p)
    return render(request, 'customer_statement.html', {
        'invoice_s': invoice_s,
        'invoice_p': invoice_p,
        'total_p': total_p,
        'total_s': total_s,
        'total_ssg': total_ssg,
        'total_scg': total_scg,
        'total_sig': total_sig,
        'total_psg': total_psg,
        'total_pcg': total_pcg,
        'total_pig': total_pig,
        'total_stg': total_stg,
        'total_ptg': total_ptg,
    })


@login_required(login_url="/login_page/")
def item_create(request):
    if request.method == 'POST':
        name = request.POST.get('name').upper()
        hsn = request.POST.get('hsn')
        tax = Decimal(request.POST.get('tax'))
        bal = Decimal(request.POST.get('bal'))

        item = Item(
            user=request.user,
            name=name,
            hsn=hsn,
            tax=tax,
            bal=bal
        )
        item.save()

        return redirect('item_read')

    return render(request, 'item_create.html')


@login_required(login_url="/login_page/")
def item_read(request):
    item = Item.objects.filter(user=request.user)
    if not item.exists():
        messages.info(request, 'No Item Found')
    return render(request, 'item_read.html', {"item": item})


@login_required
def item_update(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST.get('name').upper()
        hsn = request.POST.get('hsn')
        tax = request.POST.get('tax')
        bal = request.POST.get('bal')

        item.name = name
        item.hsn = hsn
        item.tax = tax
        item.bal = bal

        item.save()

        return redirect('item_read')

    return render(request, 'item_update.html', {"item": item})


@login_required(login_url="/login_page/")
def item_delete(request, pk):
    item = Item.objects.filter(id=pk)
    item.delete()
    return redirect('item_read')


def amount_to_words(amount):
    amount_words = num2words(amount, lang='en_IN',
                             to='currency', currency='INR').replace(",", "")
    amount_words = amount_words.capitalize()
    amount_words += " only"
    return amount_words


@login_required(login_url="/login_page/")
def invoice_create(request):
    if request.method == "POST":
        invoice_to_id = request.POST.get('invoice_to')
        invoice_to = Customer.objects.get(id=invoice_to_id)
        ship_to_id = request.POST.get('ship_to')
        ship_to = Customer.objects.get(id=ship_to_id)
        invoice_no = int(request.POST.get('invoice_no'))
        # invoice_no = int(request.POST.get('invoice_no').zfill(3))
        date = request.POST.get('date')
        eway = request.POST.get('eway')
        transport = request.POST.get('transport').upper()
        vehicle_no = request.POST.get('vehicle_no').upper()
        no_of_items = int(request.POST.get('no_of_items'))
        other_charges = Decimal(request.POST.get('other_charges'))
        discount = Decimal(request.POST.get('discount'))
        profile = Profile.objects.get(user=request.user)

        taxable_before = Decimal(0.00)

        invoice_items_arr = []
        for i in range(1, no_of_items + 1):
            item_details_id = request.POST.get('item' + str(i))
            item_details = Item.objects.get(id=item_details_id)
            quantity = Decimal(request.POST.get('quantity' + str(i)))
            rate = Decimal(request.POST.get('rate' + str(i)))
            unit = request.POST.get('unit' + str(i))
            dis = Decimal(0.00)

            if profile.state == invoice_to.state:
                sgst = item_details.tax/Decimal(2)
                cgst = item_details.tax/Decimal(2)
                igst = Decimal(0.00)
            else:
                sgst = Decimal(0.00)
                cgst = Decimal(0.00)
                igst = Decimal(item_details.tax)

            amount = rate*quantity
            taxval = amount-dis
            taxable_before += amount

            billedItem_object = BilledItem(
                item_details=item_details,
                rate=rate,
                quantity=quantity,
                unit=unit,
                dis=dis,
                igst=igst,
                sgst=sgst,
                cgst=cgst,
                amount=amount,
                taxval=taxval,
                igst_amt=Decimal(0.00),
                sgst_amt=Decimal(0.00),
                cgst_amt=Decimal(0.00),
            )

            item_details.bal -= quantity
            item_details.save()

            billedItem_object.save()
            invoice_items_arr.append(billedItem_object)

        date_obj = datetime.strptime(date, '%Y-%m-%d')
        taxable_after = taxable_before - discount + other_charges
        tgst = Decimal(0.00)
        sgst_amt_f = Decimal(0.00)
        cgst_amt_f = Decimal(0.00)
        igst_amt_f = Decimal(0.00)
        for item in invoice_items_arr:
            sgst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.sgst/100)
            cgst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.cgst/100)
            igst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.igst/100)

            item.sgst_amt = sgst_amt
            item.cgst_amt = cgst_amt
            item.igst_amt = igst_amt

            sgst_amt_f += sgst_amt
            cgst_amt_f += cgst_amt
            igst_amt_f += igst_amt
            item.save()

            tgst += sgst_amt+cgst_amt+igst_amt
            discount += item.dis

        grand_total = taxable_after + tgst

        invoice_obj = Invoice(
            user=request.user,
            invoice_to=invoice_to,
            ship_to=ship_to,
            invoice_no=invoice_no,
            date=date_obj,
            eway=eway,
            transport=transport,
            vehicle_no=vehicle_no,
            no_of_items=no_of_items,
            taxable_before=taxable_before,
            other_charges=other_charges,
            discount=discount,
            taxable_after=taxable_after,
            sgst_amt=sgst_amt_f,
            igst_amt=igst_amt_f,
            cgst_amt=cgst_amt_f,
            tgst_amt=tgst,
            grand_total=grand_total,
            grand_total_words=amount_to_words(grand_total)
        )

        invoice_to.bal -= grand_total
        invoice_to.save()

        invoice_obj.save()
        invoice_obj.invoice_items.set(invoice_items_arr)

        profile.bill_count += 1
        profile.save()

        return redirect("invoice_read")
    else:
        customer = Customer.objects.filter(user=request.user).order_by("name")
        item = Item.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'invoice_create.html', {'customer': customer, 'items': item, 'profile': profile})


@login_required(login_url="/login_page/")
def invoice_update(request, pk):
    return HttpResponse("<h1>!!!Work In Progress!!!<h1>")


@login_required(login_url="/login_page/")
def invoice_read(request):
    invoices = Invoice.objects.filter(
        user=request.user).order_by("-invoice_no")
    if len(invoices) == 0:
        messages.info(request, 'No invoice Found')
        return render(request, "invoice_read.html")
    return render(request, "invoice_read.html", {'invoices': invoices})


@login_required(login_url="/login_page/")
def invoice_delete(request, pk):
    profile = Profile.objects.get(user=request.user)

    if profile.bill_count > 0:
        profile.bill_count -= 1
        profile.save()

    invoice = Invoice.objects.get(id=pk)
    if invoice.invoice_to:
        invoice.invoice_to.bal += invoice.grand_total
        invoice.invoice_to.save()

    for item in invoice.invoice_items.all():
        item_details = item.item_details
        item_details.bal += item.quantity
        item_details.save()

    invoice.delete()

    return redirect('invoice_read')


@login_required(login_url="/login_page/")
def invoice_print_original(request, pk):
    profile = Profile.objects.get(user=request.user)
    invoice = Invoice.objects.get(id=pk)
    bill_of = "Original for Buyer"
    x = range(1, 17)
    return render(request, 'invoice_print.html', {'invoice': invoice, 'profile': profile, 'x': x, 'bill_of': bill_of})


@login_required(login_url="/login_page/")
def invoice_print_duplicate(request, pk):
    profile = Profile.objects.get(user=request.user)
    invoice = Invoice.objects.get(id=pk)
    bill_of = "Duplicate for Transporter"
    x = range(1, 17)
    return render(request, 'invoice_print.html', {'invoice': invoice, 'profile': profile, 'x': x, 'bill_of': bill_of})


@login_required(login_url="/login_page/")
def invoice_print_triplicate(request, pk):
    profile = Profile.objects.get(user=request.user)
    invoice = Invoice.objects.get(id=pk)
    bill_of = "Triplicate for Assessee"
    x = range(1, 17)
    return render(request, 'invoice_print.html', {'invoice': invoice, 'profile': profile, 'x': x, 'bill_of': bill_of})


@login_required(login_url="/login_page/")
def invoice_billbook(request):
    invoice = Invoice.objects.filter(user=request.user).order_by('invoice_no')
    profile = Profile.objects.get(user=request.user)
    x = range(1, 20)
    return render(request, 'invoice_billbook.html', {"invoices": invoice, "profile": profile, 'x': x})


@login_required(login_url="/login_page/")
def bank_create(request):
    if request.method == "POST":
        name = request.POST.get('name').upper()
        acno = request.POST.get('acno')
        ifsc = request.POST.get('ifsc').upper()
        branch = request.POST.get('branch').upper()
        bal = Decimal(request.POST.get('bal'))

        bank = Bank(
            user=request.user,
            name=name,
            acno=acno,
            ifsc=ifsc,
            branch=branch,
            bal=bal
        )

        bank.save()

        return redirect('bank_read')

    return render(request, 'bank_create.html')


@login_required(login_url="/login_page/")
def bank_read(request):
    bank = Bank.objects.filter(user=request.user)
    if not bank.exists():
        messages.info(request, 'No Bank Account Found')
    return render(request, 'bank_read.html', {"bank": bank})


@login_required(login_url="/login_page/")
def bank_update(request, pk):
    bank = Bank.objects.get(id=pk)

    if request.method == "POST":
        name = request.POST.get('name').upper()
        acno = request.POST.get('acno')
        ifsc = request.POST.get('ifsc').upper()
        branch = request.POST.get('branch').upper()
        bal = Decimal(request.POST.get('bal'))

        bank.name = name
        bank.acno = acno
        bank.ifsc = ifsc
        bank.branch = branch
        bank.bal = bal

        bank.save()
        return redirect('bank_read')

    return render(request, 'bank_update.html', {'bank': bank})


@login_required(login_url="/login_page/")
def bank_delete(request, pk):
    bank = Bank.objects.filter(id=pk)
    bank.delete()
    return redirect('bank_read')


@login_required(login_url="/login_page/")
def bank_statement(request, pk):
    payment = Payment.objects.filter(bank=pk)
    if not payment.exists():
        messages.info(request, 'No Item Found')
    return render(request, 'bank_statement.html', {"payment": payment})


@login_required(login_url="/login_page/")
def invoicepurchase_create(request):
    if request.method == "POST":
        invoice_to_id = request.POST.get('invoice_to')
        invoice_to = Customer.objects.get(id=invoice_to_id)
        date = request.POST.get('date')
        invoice_no = request.POST.get('invoice_no')
        no_of_items = int(request.POST.get('no_of_items'))
        other_charges = Decimal(request.POST.get('other_charges'))
        discount = Decimal(request.POST.get('discount'))
        profile = Profile.objects.get(user=request.user)

        taxable_before = Decimal(0.00)

        invoice_items_arr = []
        for i in range(1, no_of_items + 1):
            item_details_id = request.POST.get('item' + str(i))
            item_details = Item.objects.get(id=item_details_id)
            quantity = Decimal(request.POST.get('quantity' + str(i)))
            rate = Decimal(request.POST.get('rate' + str(i)))
            unit = request.POST.get('unit' + str(i))
            dis = Decimal(request.POST.get('dis' + str(i)))

            if profile.state == invoice_to.state:
                sgst = item_details.tax/Decimal(2)
                cgst = item_details.tax/Decimal(2)
                igst = Decimal(0.00)
            else:
                sgst = Decimal(0.00)
                cgst = Decimal(0.00)
                igst = Decimal(item_details.tax)

            amount = rate*quantity
            taxval = amount-dis
            taxable_before += taxval

            billedItem_object = BilledItem(
                item_details=item_details,
                rate=rate,
                quantity=quantity,
                unit=unit,
                dis=dis,
                igst=igst,
                sgst=sgst,
                cgst=cgst,
                amount=amount,
                taxval=taxval,
                igst_amt=Decimal(0.00),
                sgst_amt=Decimal(0.00),
                cgst_amt=Decimal(0.00),
            )

            item_details.bal += quantity
            item_details.save()

            billedItem_object.save()
            invoice_items_arr.append(billedItem_object)

        date_obj = datetime.strptime(date, '%Y-%m-%d')
        taxable_after = taxable_before - discount + other_charges
        tgst = Decimal(0.00)
        sgst_amt_f = Decimal(0.00)
        cgst_amt_f = Decimal(0.00)
        igst_amt_f = Decimal(0.00)
        for item in invoice_items_arr:
            sgst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.sgst/100)
            cgst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.cgst/100)
            igst_amt = (item.taxval/taxable_before) * \
                taxable_after*(item.igst/100)

            item.sgst_amt = sgst_amt
            item.cgst_amt = cgst_amt
            item.igst_amt = igst_amt

            sgst_amt_f += sgst_amt
            cgst_amt_f += cgst_amt
            igst_amt_f += igst_amt
            item.save()

            tgst += sgst_amt+cgst_amt+igst_amt

        grand_total = taxable_after + tgst

        invoice_obj = InvoicePurchase(
            user=request.user,
            invoice_to=invoice_to,
            date=date_obj,
            invoice_no=invoice_no,
            no_of_items=no_of_items,
            taxable_before=taxable_before,
            other_charges=other_charges,
            discount=discount,
            taxable_after=taxable_after,
            sgst_amt=sgst_amt_f,
            igst_amt=igst_amt_f,
            cgst_amt=cgst_amt_f,
            tgst_amt=tgst,
            grand_total=grand_total
        )

        invoice_to.bal += grand_total
        invoice_to.save()

        invoice_obj.save()
        invoice_obj.invoice_items.set(invoice_items_arr)

        profile.save()

        return redirect("invoicepurchase_read")
    else:
        customer = Customer.objects.filter(user=request.user)
        item = Item.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'invoicepurchase_create.html', {'customer': customer, 'items': item, 'profile': profile})


@login_required(login_url="/login_page/")
def invoicepurchase_update(request, pk):
    return HttpResponse("<h1>!!!Work In Progress!!!<h1>")


@login_required(login_url="/login_page/")
def invoicepurchase_read(request):
    invoices = InvoicePurchase.objects.filter(
        user=request.user).order_by('-id')
    if len(invoices) == 0:
        messages.info(request, 'No invoice Found')
        return render(request, "invoicepurchase_read.html")
    return render(request, "invoicepurchase_read.html", {'invoices': invoices})


@login_required(login_url="/login_page/")
def invoicepurchase_delete(request, pk):
    invoice = InvoicePurchase.objects.get(id=pk)
    if invoice.invoice_to:
        invoice.invoice_to.bal -= invoice.grand_total
        invoice.invoice_to.save()

    for item in invoice.invoice_items.all():
        item_details = item.item_details
        item_details.bal -= item.quantity
        item_details.save()

    invoice.delete()

    return redirect('invoicepurchase_read')


@login_required(login_url="/login_page/")
def invoicepurchase_print(request, pk):
    profile = Profile.objects.get(user=request.user)
    invoice = InvoicePurchase.objects.get(id=pk)
    bill_of = ["Original for Buyer",
               "Duplicate for Transporter", "Triplicate for Assessee"]
    x = range(1, 19)
    return render(request, 'invoicepurchase_print.html', {'invoice': invoice, 'profile': profile, 'x': x, 'bill_of': bill_of})


@login_required(login_url="/login_page/")
def invoicepurchase_billbook(request):
    invoice = InvoicePurchase.objects.filter(
        user=request.user).order_by('invoice_no')
    profile = Profile.objects.get(user=request.user)
    x = range(1, 20)
    return render(request, 'invoicepurchase_billbook.html', {"invoices": invoice, "profile": profile, 'x': x})


@login_required(login_url="/login_page/")
def company_statement(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    invoice_s = Invoice.objects.filter(
        user=request.user).order_by('-invoice_no')
    invoice_p = InvoicePurchase.objects.filter(
        user=request.user).order_by('-date')

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            invoice_s = invoice_s.filter(date__range=(start, end))
            invoice_p = invoice_p.filter(date__range=(start, end))
        except:
            pass  # optionally add error handling

    context = {
        'invoice_s': invoice_s,
        'invoice_p': invoice_p,
        'total_s': sum(i.grand_total for i in invoice_s),
        'total_p': sum(i.grand_total for i in invoice_p),
        'total_ssg': sum(i.sgst_amt for i in invoice_s),
        'total_scg': sum(i.cgst_amt for i in invoice_s),
        'total_sig': sum(i.igst_amt for i in invoice_s),
        'total_stg': sum(i.tgst_amt for i in invoice_s),
        'total_psg': sum(i.sgst_amt for i in invoice_p),
        'total_pcg': sum(i.cgst_amt for i in invoice_p),
        'total_pig': sum(i.igst_amt for i in invoice_p),
        'total_ptg': sum(i.tgst_amt for i in invoice_p),
        'total_tax': (
            sum(i.tgst_amt for i in invoice_s) -
            sum(i.tgst_amt for i in invoice_p)
        )
    }
    return render(request, 'company_statement.html', context)


import pandas as pd
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .models import Invoice, BilledItem, Item
import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
import pandas as pd
from datetime import datetime
import os

@login_required(login_url="/login_page/")
def invoice_excel_report(request):
    if request.method == 'POST':
        # Get dates from POST data
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        
        # Debug: Print received values
        print(f"Received - Start Date: {start_date_str}, End Date: {end_date_str}")
        
        # Validate dates
        if not start_date_str or not end_date_str:
            return render(request, 'generate_excel.html', {
                'error': 'Please provide both start and end dates'
            })
        
        try:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            # Debug: Print converted dates
            print(f"Converted - Start Date: {start_date}, End Date: {end_date}")
            
            # Filter invoices for the current user only (add this for security)
            invoices = Invoice.objects.filter(
                user=request.user,  # Filter by current user
                date__gte=start_date,
                date__lte=end_date
            ).select_related('invoice_to').order_by('date')
            
            print(f"Found {invoices.count()} invoices for user {request.user}")
            
            # Create Excel writer
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="GST_Report_{start_date}_to_{end_date}.xlsx"'
            
            # Create DataFrame
            data = []
            
            for invoice in invoices:
                # Get all billed items for this invoice
                billed_items = invoice.invoice_items.all()
                
                # Calculate total quantity in KG
                total_quantity_kg = billed_items.aggregate(
                    total_qty=Sum('quantity')
                )['total_qty'] or 0
                
                # Get unique HSN codes from items
                hsn_codes = []
                for billed_item in billed_items:
                    if billed_item.item_details:
                        hsn = billed_item.item_details.hsn
                        if hsn and hsn not in hsn_codes:
                            hsn_codes.append(hsn)
                
                # Join HSN codes if multiple, otherwise single
                hsn_display = ', '.join(hsn_codes) if hsn_codes else "N/A"
                
                # Calculate tax percentage
                taxable_amount = float(invoice.taxable_after) if invoice.taxable_after else 0
                total_tax = float(invoice.tgst_amt) if invoice.tgst_amt else 0
                tax_percentage = (total_tax / taxable_amount * 100) if taxable_amount > 0 else 0
                
                # Prepare row data
                row = {
                    'DATE': invoice.date.strftime('%d-%m-%Y') if invoice.date else '',
                    'BILL NO': invoice.invoice_no,
                    'GOODS/Kg': float(total_quantity_kg),
                    'HSN Code': hsn_display,
                    'AMOUNT': float(invoice.taxable_after) if invoice.taxable_after else 0,
                    'TAX%': round(tax_percentage, 2),
                    'SGST': float(invoice.sgst_amt) if invoice.sgst_amt else 0,
                    'CGST': float(invoice.cgst_amt) if invoice.cgst_amt else 0,
                    'IGST': float(invoice.igst_amt) if invoice.igst_amt else 0,
                    'TOTAL AMOUNT': float(invoice.grand_total) if invoice.grand_total else 0,
                    'GSTIN': invoice.invoice_to.gst if invoice.invoice_to and invoice.invoice_to.gst else '',
                    'CUSTOMER NAME': invoice.invoice_to.name if invoice.invoice_to else ''
                }
                data.append(row)
            
            # Create DataFrame
            df = pd.DataFrame(data)
            
            # Add totals row if there's data
            if not df.empty:
                totals = {
                    'DATE': 'TOTAL',
                    'BILL NO': '',
                    'GOODS/Kg': df['GOODS/Kg'].sum(),
                    'HSN Code': '',
                    'AMOUNT': df['AMOUNT'].sum(),
                    'TAX%': '',
                    'SGST': df['SGST'].sum(),
                    'CGST': df['CGST'].sum(),
                    'IGST': df['IGST'].sum(),
                    'TOTAL AMOUNT': df['TOTAL AMOUNT'].sum(),
                    'GSTIN': '',
                    'CUSTOMER NAME': ''
                }
                df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
            
            # Write to Excel using pandas ExcelWriter
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='GST Report', index=False, startrow=3)
                
                # Get workbook and worksheet
                workbook = writer.book
                worksheet = writer.sheets['GST Report']
                
                # Get company details from Profile (assuming you have a Profile model)
                try:
                    from .models import Profile
                    profile = Profile.objects.get(user=request.user)
                    company_name = profile.name or "YOUR COMPANY NAME"
                    company_gstin = profile.gst or "YOUR GSTIN"
                except:
                    company_name = "YOUR COMPANY NAME"
                    company_gstin = "YOUR GSTIN"
                
                # Add headers at the top
                worksheet['A1'] = company_name

                
                
                worksheet['A2'] = f"GSTIN: {company_gstin}"
                
                
                worksheet.merge_cells('A3:L3')
                worksheet['A3'] = f"Report Period: {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')}"
                
                # Adjust column widths
                column_widths = {
                    'A': 12,  # DATE
                    'B': 10,  # BILL NO
                    'C': 12,  # GOODS/Kg
                    'D': 15,  # HSN Code
                    'E': 12,  # AMOUNT
                    'F': 8,   # TAX%
                    'G': 10,  # SGST
                    'H': 10,  # CGST
                    'I': 10,  # IGST
                    'J': 15,  # TOTAL AMOUNT
                    'K': 20,  # GSTIN
                    'L': 25   # CUSTOMER NAME
                }
                
                for col, width in column_widths.items():
                    worksheet.column_dimensions[col].width = width
                
                # Format number columns
                from openpyxl.styles import numbers
                for row in range(5, len(df) + 4):  # Start from row 5 (after headers)
                    # Format numeric columns
                    numeric_cols = ['C', 'E', 'G', 'H', 'I', 'J']
                    for col in numeric_cols:
                        cell = worksheet[f'{col}{row}']
                        cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
                    
                    # Format percentage column
                    cell = worksheet[f'F{row}']
                    cell.number_format = '0.00%' if row < len(df) + 3 else ''  # Don't format total row
                
                # Format totals row
                # if not df.empty:
                #     last_row = len(df) + 3
                #     worksheet[f'A{last_row}'].font = Font(bold=True)
                #     for col in ['C', 'E', 'G', 'H', 'I', 'J']:
                #         worksheet[f'{col}{last_row}'].font = Font(bold=True)
                #         worksheet[f'{col}{last_row}'].number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
            
            return response
            
        except ValueError as e:
            print(f"ValueError: {e}")
            return render(request, 'generate_excel.html', {
                'error': 'Invalid date format. Please use YYYY-MM-DD format.'
            })
        except Exception as e:
            print(f"Exception: {e}")
            return render(request, 'generate_excel.html', {
                'error': f'An error occurred: {str(e)}'
            })
    
    # GET request - show the form
    return render(request, 'generate_excel.html')

@login_required(login_url="/login_page/")
def payment_create(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST.get('date')
        payment_of_id = request.POST.get('payment_of')
        payment_of = Customer.objects.get(id=payment_of_id)
        amount = Decimal(request.POST.get('amount'))
        mode = request.POST.get('mode')
        p_type = request.POST.get('p_type')

        if mode == "BANK":
            bank_id = request.POST.get('bank_id')
            bank = Bank.objects.get(id=bank_id)
        else:
            bank = None

        payment = Payment(
            user=user,
            date=date,
            payment_of=payment_of,
            amount=amount,
            mode=mode,
            p_type=p_type,
            bank=bank,
        )
        payment.save()
        profile = Profile.objects.get(user=request.user)

        if p_type == "CREDIT":
            if mode == "BANK":
                bank.bal += amount
            elif mode == "CASH":
                profile.cash += amount
            payment_of.bal += amount
        elif p_type == "DEBIT":
            if mode == "BANK":
                bank.bal -= amount
            elif mode == "CASH":
                profile.cash -= amount
            payment_of.bal -= amount

        payment_of.save()
        bank.save()
        profile.save()
        return redirect('payment_read')

    payment = Payment.objects.filter(user=request.user)
    bank = Bank.objects.filter(user=request.user)
    customer = Customer.objects.filter(user=request.user)

    return render(request, 'payment_create.html', {'payment': payment, 'bank': bank, 'customer': customer})


@login_required(login_url="/login_page/")
def payment_read(request):
    payment = Payment.objects.filter(user=request.user)
    if not payment.exists():
        messages.info(request, 'No Item Found')
    return render(request, 'payment_read.html', {"payment": payment})


@login_required
def payment_update(request, pk):
    item = Item.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST.get('name').upper()
        hsn = request.POST.get('hsn')
        tax = request.POST.get('tax')
        bal = request.POST.get('bal')

        item.name = name
        item.hsn = hsn
        item.tax = tax
        item.bal = bal

        item.save()

        return redirect('item_read')

    return render(request, 'item_update.html', {"item": item})


@login_required(login_url="/login_page/")
def payment_delete(request, pk):
    payment = Payment.objects.get(id=pk)
    if payment.p_type == "CREDIT":
        if payment.mode == "BANK":
            payment.bank.bal -= payment.amount
        elif payment.mode == "CASH":
            payment.profile.cash -= payment.amount
        payment.payment_of.bal -= payment.amount
    elif payment.p_type == "DEBIT":
        if payment.mode == "BANK":
            payment.bank.bal += payment.amount
        elif payment.mode == "CASH":
            payment.profile.cash += payment.amount
        payment.payment_of.bal += payment.amount

    payment.payment_of.save()
    payment.bank.save()
    payment.delete()
    return redirect('payment_read')


# View to create a new employee

def employee_create(request):
    if request.method == 'POST':
        # Extract data from the request
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        role = request.POST.get('role')
        bal = request.POST.get('bal')

        # Create and save the new employee object
        try:
            employee = Employee(
                user=request.user,
                name=name,
                email=email,
                phone=phone,
                gender=gender,
                role=role,
                bal=bal if bal else 0.00  # Default to 0 if balance is not provided
            )
            employee.save()

            # Provide success feedback
            messages.success(
                request, f'Employee {employee.name} added successfully.')
            # Assuming you have a list page for employees
            return redirect('employee_read')

        except Exception as e:
            messages.error(request, f'Error creating employee: {e}')
            return redirect('employee_create')

    return render(request, 'employee_create.html')


@login_required(login_url="/login_page/")
def employee_read(request):
    employee = Employee.objects.filter(user=request.user)
    if not employee.exists():
        messages.info(request, 'No Employee Found')
    return render(request, 'employee_read.html', {"employee": employee})


@login_required(login_url="/login_page/")
def employee_delete(request, pk):
    employee = Employee.objects.filter(id=pk)
    employee.delete()
    return redirect('employee_read')


@login_required(login_url="/login_page/")
def process_create(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST.get('date')
        source_item_id = request.POST.get('source_item_id')
        output_item_id = request.POST.get('output_item_id')
        employee_id = request.POST.get('employee_id')
        source_item = Item.objects.get(id=source_item_id)
        output_item = Item.objects.get(id=output_item_id)
        employee = Employee.objects.get(id=employee_id)
        quantity = Decimal(request.POST.get('quantity'))
        wastage = Decimal(request.POST.get('wastage'))

        expected_input = round(quantity*Decimal(100.00) /
                               (Decimal(100.00)-wastage))
        source_item.bal -= expected_input
        source_item.save()

        output_item.bal += quantity
        output_item.save()

        record = ProcessingRecord(
            user=user,
            source_item=source_item,
            output_item=output_item,
            quantity_out=quantity,
            wastage_percent=wastage,
            employee=employee,
            processed_at=date,
        )
        record.save()

        return redirect('process_read')

    employee = Employee.objects.filter(user=request.user)
    item = Item.objects.filter(user=request.user)

    return render(request, 'process_create.html', {'item': item, 'employee': employee})


@login_required(login_url="/login_page/")
def process_read(request):
    process = ProcessingRecord.objects.filter(user=request.user)
    if not process.exists():
        messages.info(request, 'No process Found')
    return render(request, 'process_read.html', {"process": process})


@login_required(login_url="/login_page/")
def process_delete(request, pk):
    process = ProcessingRecord.objects.filter(id=pk)
    process.delete()
    return redirect('process_read')
