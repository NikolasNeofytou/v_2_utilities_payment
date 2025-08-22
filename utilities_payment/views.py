from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser
import csv
from datetime import datetime
from decimal import Decimal
from io import TextIOWrapper
from uuid import uuid4
from django.db.models import Sum
from .models import Tenant, Customer, ServicePoint, Bill, PaymentIntent


class BillImportView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, tenant_id):
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        upload = request.FILES.get("file")
        if not upload:
            return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        wrapper = TextIOWrapper(upload.file, encoding="utf-8")
        reader = csv.DictReader(wrapper)
        created = 0
        errors = []

        for idx, row in enumerate(reader, start=2):
            required = [
                "customer_id",
                "meter_id",
                "period_start",
                "period_end",
                "due_date",
                "amount_due",
            ]
            missing = [f for f in required if not row.get(f)]
            if missing:
                errors.append({"row": idx, "error": f"Missing fields: {', '.join(missing)}"})
                continue

            try:
                period_start = datetime.strptime(row["period_start"], "%Y-%m-%d").date()
                period_end = datetime.strptime(row["period_end"], "%Y-%m-%d").date()
                due_date = datetime.strptime(row["due_date"], "%Y-%m-%d").date()
                amount_due = Decimal(row["amount_due"])
            except Exception as exc:
                errors.append({"row": idx, "error": str(exc)})
                continue

            try:
                customer = Customer.objects.get(id=row["customer_id"], tenant=tenant)
            except Customer.DoesNotExist:
                errors.append({"row": idx, "error": "Unknown customer"})
                continue

            sp, _ = ServicePoint.objects.get_or_create(
                tenant=tenant,
                customer=customer,
                meter_id=row["meter_id"],
                defaults={"address": row.get("address", "")},
            )
            bill = Bill.objects.create(
                service_point=sp,
                period_start=period_start,
                period_end=period_end,
                due_date=due_date,
                amount_due=amount_due,
                currency=row.get("currency", "EUR"),
            )
            PaymentIntent.objects.create(
                bill=bill,
                gateway=row.get("gateway", "stripe"),
                amount=amount_due,
                pay_link_token=str(uuid4()),
            )
            created += 1

        status_code = status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS
        return Response({"created": created, "errors": errors}, status=status_code)


class TenantMetricsView(APIView):
    """Basic collection metrics for a tenant."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, tenant_id):
        try:
            tenant = Tenant.objects.get(id=tenant_id)
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found"}, status=status.HTTP_404_NOT_FOUND)

        bills = Bill.objects.filter(service_point__tenant=tenant)
        total_bills = bills.count()
        total_amount = bills.aggregate(total=Sum("amount_due")) ["total"] or 0

        paid_bills = bills.filter(paymentintent__status="succeeded")
        paid_count = paid_bills.count()
        paid_amount = paid_bills.aggregate(total=Sum("amount_due")) ["total"] or 0

        return Response(
            {
                "total_bills": total_bills,
                "paid_bills": paid_count,
                "total_amount_due": str(total_amount),
                "paid_amount": str(paid_amount),
                "outstanding_amount": str(total_amount - paid_amount),
            }
        )


class CustomerBillsView(APIView):
    """List bills for a customer."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        bills = (
            Bill.objects.filter(service_point__customer=customer)
            .select_related("service_point")
            .order_by("-due_date")
        )

        data = [
            {
                "id": b.id,
                "service_point": b.service_point.meter_id,
                "period_start": b.period_start.isoformat(),
                "period_end": b.period_end.isoformat(),
                "due_date": b.due_date.isoformat(),
                "amount_due": str(b.amount_due),
                "status": b.status,
            }
            for b in bills
        ]

        return Response(data)
