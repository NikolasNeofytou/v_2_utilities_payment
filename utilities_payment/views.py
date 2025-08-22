from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser
import csv
from datetime import datetime
from decimal import Decimal
from io import TextIOWrapper
from uuid import uuid4
from .models import Tenant, ServicePoint, Bill, PaymentIntent


class BillImportView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [permissions.AllowAny]

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
            required = ["meter_id", "period_start", "period_end", "due_date", "amount_due"]
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

            sp, _ = ServicePoint.objects.get_or_create(
                tenant=tenant,
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
