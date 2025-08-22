from django.db import models


class Tenant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.tenant.name})"


class ServicePoint(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    meter_id = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.meter_id


class Bill(models.Model):
    service_point = models.ForeignKey(ServicePoint, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="EUR")
    status = models.CharField(max_length=20, default="pending")

    def __str__(self) -> str:
        return f"Bill {self.id} for {self.service_point.meter_id}"


class BillLine(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="lines")
    line_type = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class PaymentIntent(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    gateway = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="pending")
    pay_link_token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField(null=True, blank=True)


class Payment(models.Model):
    intent = models.ForeignKey(PaymentIntent, on_delete=models.CASCADE)
    gateway_charge_id = models.CharField(max_length=255)
    captured_at = models.DateTimeField()
    method = models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    net = models.DecimalField(max_digits=10, decimal_places=2)


class Notification(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    channel = models.CharField(max_length=20)
    template_id = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length=20, default="pending")
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)


class ReconciliationEntry(models.Model):
    payout_id = models.CharField(max_length=255)
    amount_gross = models.DecimalField(max_digits=10, decimal_places=2)
    amount_net = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    matched = models.BooleanField(default=False)
