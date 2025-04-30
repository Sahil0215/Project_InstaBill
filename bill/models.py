from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    acno = models.CharField(max_length=20, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    branch = models.CharField(max_length=25, blank=True, null=True)
    bal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gst = models.CharField(max_length=20)
    adrs = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    bal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    bill_count = models.IntegerField(blank=True, null=True, default=0)
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, blank=True, null=True, default=0)
    cash = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)


class FinancialYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_fy = models.CharField(max_length=5, null=True, blank=True)
    from_to = models.CharField(max_length=5, null=True, blank=True)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gst = models.CharField(max_length=20, blank=True, null=True)
    adrs = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    bal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    hsn = models.CharField(max_length=10)
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    bal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)


class BilledItem(models.Model):
    item_details = models.ForeignKey(
        Item, on_delete=models.CASCADE, blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=5, blank=True, null=True)
    dis = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    igst = models.DecimalField(max_digits=10, decimal_places=2)
    sgst = models.DecimalField(max_digits=10, decimal_places=2)
    cgst = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    taxval = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    igst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_amt = models.DecimalField(max_digits=10, decimal_places=2)


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_to = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='billto')
    ship_to = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='shipto')
    invoice_no = models.PositiveIntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    eway = models.CharField(max_length=25)
    transport = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=15)
    no_of_items = models.PositiveIntegerField(default=0)
    invoice_items = models.ManyToManyField(BilledItem)
    taxable_before = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_after = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    igst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    tgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total_words = models.CharField(max_length=150, null=True)


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    bal = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=0.00)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InvoicePurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_to = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='billtopurchase')
    invoice_no = models.PositiveIntegerField(default=0)
    date = models.DateField(blank=True, null=True)
    no_of_items = models.PositiveIntegerField(default=0)
    invoice_items = models.ManyToManyField(BilledItem)
    taxable_before = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_after = models.DecimalField(max_digits=10, decimal_places=2)
    sgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    igst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    cgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    tgst_amt = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    payment_of = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mode = models.CharField(max_length=10, blank=True, null=True)
    p_type = models.CharField(max_length=10, blank=True, null=True)
    bank = models.ForeignKey(
        Bank, on_delete=models.CASCADE, blank=True, null=True)


class ProcessingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='source_processes')
    output_item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='output_processes')
    quantity_out = models.DecimalField(max_digits=10, decimal_places=2)
    wastage_percent = models.DecimalField(max_digits=5, decimal_places=2)
    employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_item} ➜ {self.output_item} ({self.processed_at.date()})"
