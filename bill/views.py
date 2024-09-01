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
        
        User.objects.create_user(username=username, password=password, email=email)
        
        messages.success(request, "Registration successful. You can now log in.")

        user = authenticate(request, username=username, password=password)
        login(request, user)
        return redirect('setup_profile') 
    
    return render(request, 'register.html')


@login_required(login_url="/login_page/")
def delete_account(request,pk):
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
        
        bank_obj= Bank(
            user = request.user,
            name = bank_name,
            acno = acno,
            ifsc = bank_ifsc,
            branch = bank_branch,
            bal = 0.00
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
            bank = bank_obj,
            bal=Decimal(0.00)
        )
        profile.save()

        messages.success(request, "Profile setup successful.")
        return redirect('login_page')
    
    return render(request, 'setup_profile.html')



@login_required(login_url="/login_page/")
def view_profile(request):
    profile= Profile.objects.filter(user=request.user)
    return render(request, 'view_profile.html',{"profile":profile})

@login_required(login_url="/login_page/")
def update_profile(request):
    profile = Profile.objects.get(user=request.user)  # Get the profile of the logged-in user
    bank = Bank.objects.all()

    if request.method == 'POST':
        c_name = request.POST.get('c_name').upper()
        gst = request.POST.get('gst').upper()
        adrs = request.POST.get('adrs')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone = request.POST.get('phone')
        c_email = request.POST.get('c_email')
        bill_count = request.POST.get('bill_count')
        bank_id= request.POST.get('bank')

        bank= Bank.objects.get(id=bank_id)

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
    if request.method=="POST":
        name= request.POST.get('name').upper()
        gst= request.POST.get('gst').upper()
        adrs= request.POST.get('adrs')
        city= request.POST.get('city')
        state= request.POST.get('state').upper()
        phone= request.POST.get('phone')
        email= request.POST.get('email')

        customer=Customer(
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
    customer=Customer.objects.filter(user=request.user)
    if not customer.exists():
        messages.info(request, 'No Customer Found')
    return render(request, 'customer_read.html', {"customer":customer})

@login_required(login_url="/login_page/")
def customer_update(request,pk):
    customer = Customer.objects.get(id=pk)

    if request.method=="POST":
        name= request.POST.get('name').upper()
        gst= request.POST.get('gst').upper()
        adrs= request.POST.get('adrs')
        city= request.POST.get('city')
        state= request.POST.get('state').upper()
        phone= request.POST.get('phone')
        email= request.POST.get('email')

        if not all([name,gst,adrs,city,state,phone]):
            messages.error(request, 'All fields are required.')
        else:
            customer.name=name
            customer.gst=gst
            customer.adrs=adrs
            customer.city=city
            customer.state=state
            customer.phone=phone
            customer.email=email
            customer.save()
            return redirect('customer_read')
        
    return render(request, 'customer_update.html', {'customer':customer})

@login_required(login_url="/login_page/")
def customer_delete(request,pk):
    customer=Customer.objects.filter(id=pk)
    customer.delete()
    return redirect('customer_read')

@login_required(login_url="/login_page/")
def supplier_create(request):
    if request.method=="POST":
        name= request.POST.get('name').upper()
        gst= request.POST.get('gst').upper()
        adrs= request.POST.get('adrs')
        city= request.POST.get('city')
        state= request.POST.get('state').upper()
        phone= request.POST.get('phone')
        email= request.POST.get('email')

        supplier=Supplier(
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
        supplier.save()
        return redirect('supplier_read')
    
    return render(request, 'supplier_create.html')

@login_required(login_url="/login_page/")
def supplier_read(request):
    supplier=Supplier.objects.filter(user=request.user)
    if not supplier.exists():
        messages.info(request, 'No supplier Found')
    return render(request, 'supplier_read.html', {"supplier":supplier})

@login_required(login_url="/login_page/")
def supplier_update(request,pk):
    supplier = Supplier.objects.get(id=pk)

    if request.method=="POST":
        name= request.POST.get('name').upper()
        gst= request.POST.get('gst').upper()
        adrs= request.POST.get('adrs')
        city= request.POST.get('city')
        state= request.POST.get('state').upper()
        phone= request.POST.get('phone')
        email= request.POST.get('email')

        if not all([name,gst,adrs,city,state,phone]):
            messages.error(request, 'All fields are required.')
        else:
            supplier.name=name
            supplier.gst=gst
            supplier.adrs=adrs
            supplier.city=city
            supplier.state=state
            supplier.phone=phone
            supplier.email=email
            supplier.save()
            return redirect('supplier_read')
        
    return render(request, 'supplier_update.html', {'supplier':supplier})


@login_required(login_url="/login_page/")
def supplier_delete(request,pk):
    supplier=Supplier.objects.filter(id=pk)
    supplier.delete()
    return redirect('supplier_read')


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
    item=Item.objects.filter(user=request.user)
    if not item.exists():
        messages.info(request, 'No Item Found')
    return render(request, 'item_read.html', {"item":item})


@login_required
def item_update(request,pk):
    item = Item.objects.get(id=pk)
    if request.method=="POST":
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

    return render(request, 'item_update.html', {"item" : item})

@login_required(login_url="/login_page/")
def item_delete(request, pk):
    item=Item.objects.filter(id=pk)
    item.delete()
    return redirect('item_read')

from datetime import datetime
def amount_to_words(amount):
    amount_words = num2words(amount, lang='en_IN', to='currency', currency='INR').replace(",", "")
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
        date = request.POST.get('date')
        eway = request.POST.get('eway')
        transport = request.POST.get('transport').upper()
        vehicle_no = request.POST.get('vehicle_no').upper()
        no_of_items = int(request.POST.get('no_of_items'))
        other_charges = Decimal(request.POST.get('other_charges'))
        discount = Decimal(request.POST.get('discount'))
        profile=Profile.objects.get(user=request.user)

        taxable_before = Decimal(0.00)

        invoice_items_arr = []
        for i in range(1, no_of_items + 1):
            item_details_id = request.POST.get('item' + str(i))
            item_details = Item.objects.get(id=item_details_id)
            quantity = Decimal(request.POST.get('quantity' + str(i)))
            rate = Decimal(request.POST.get('rate' + str(i)))
            unit = request.POST.get('unit' + str(i))
            dis = Decimal(request.POST.get('dis' + str(i)))

            if profile.state==invoice_to.state:
                sgst = item_details.tax/Decimal(2)
                cgst = item_details.tax/Decimal(2)
                igst = Decimal(0.00)
            else:
                sgst = Decimal(0.00)
                cgst = Decimal(0.00)
                igst = Decimal(item_details.tax)
                
            amount=rate*quantity
            taxval = amount-dis
            taxable_before += taxval

            billedItem_object = BilledItem(
                item_details= item_details,
                rate= rate,
                quantity= quantity,
                unit= unit,
                dis= dis,
                igst= igst,
                sgst= sgst,
                cgst= cgst,
                amount= amount,
                taxval= taxval,
                igst_amt= Decimal(0.00),
                sgst_amt= Decimal(0.00),
                cgst_amt= Decimal(0.00),
            )

            item_details.bal-=quantity
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
            sgst_amt = (item.taxval/taxable_before)*taxable_after*(item.sgst/100) 
            cgst_amt = (item.taxval/taxable_before)*taxable_after*(item.cgst/100) 
            igst_amt = (item.taxval/taxable_before)*taxable_after*(item.igst/100) 
            
            item.sgst_amt=sgst_amt
            item.cgst_amt=cgst_amt
            item.igst_amt=igst_amt

            sgst_amt_f += sgst_amt 
            cgst_amt_f += cgst_amt
            igst_amt_f += igst_amt
            item.save()

            tgst += sgst_amt+cgst_amt+igst_amt

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

        invoice_to.bal-=grand_total
        invoice_to.save()

        invoice_obj.save()
        invoice_obj.invoice_items.set(invoice_items_arr)

        profile.bill_count+=1
        profile.save()
        
        return redirect("invoice_read")
    else:
        customer = Customer.objects.filter(user=request.user)
        item = Item.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'invoice_create.html', {'customer': customer, 'items': item, 'profile':profile})



@login_required(login_url="/login_page/")
def invoice_update(request,pk):
    return HttpResponse("<h1>!!!Work In Progress!!!<h1>")

@login_required(login_url="/login_page/")
def invoice_read(request):
    invoices=Invoice.objects.filter(user=request.user).order_by("-invoice_no")
    if len(invoices)==0:
        messages.info(request, 'No invoice Found')
        return render(request, "invoice_read.html")
    return render(request, "invoice_read.html", {'invoices':invoices})


@login_required(login_url="/login_page/")
def invoice_delete(request,pk):
    profile = Profile.objects.get(user=request.user)
    profile.bill_count-=1
    profile.save()
    invoice=Invoice.objects.get(id=pk)
    invoice.delete()
    return redirect('invoice_read')

@login_required(login_url="/login_page/")
def invoice_print(request,pk):
    profile = Profile.objects.get(user=request.user)
    invoice=Invoice.objects.get(id=pk)
    x=range(1,19)
    return render(request, 'invoice_print.html', {'invoice':invoice, 'profile':profile, 'x':x})

@login_required(login_url="/login_page/")
def invoice_billbook(request):
    invoice = Invoice.objects.filter(user=request.user).order_by('invoice_no')
    profile = Profile.objects.get(user=request.user)
    x=range(1,20)
    return render(request, 'invoice_billbook.html', {"invoices":invoice, "profile":profile, 'x':x})

@login_required(login_url="/login_page/")
def bank_create(request):
    if request.method=="POST":
        name = request.POST.get('name').upper()
        acno = request.POST.get('acno')
        ifsc = request.POST.get('ifsc').upper()
        branch = request.POST.get('branch').upper()
        bal = Decimal(request.POST.get('bal'))

        bank=Bank(
            user=request.user,
            name = name,
            acno = acno,
            ifsc = ifsc,
            branch = branch,
            bal = bal
        )

        bank.save()

        return redirect('bank_read')
    
    return render(request, 'bank_create.html')

@login_required(login_url="/login_page/")
def bank_read(request):
    bank=Bank.objects.filter(user=request.user)
    if not bank.exists():
        messages.info(request, 'No Bank Account Found')
    return render(request, 'bank_read.html', {"bank":bank})

@login_required(login_url="/login_page/")
def bank_update(request,pk):
    bank = Bank.objects.get(id=pk)

    if request.method=="POST":
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
        
    return render(request, 'bank_update.html', {'bank':bank})

@login_required(login_url="/login_page/")
def bank_delete(request,pk):
    bank=Bank.objects.filter(id=pk)
    bank.delete()
    return redirect('bank_read')