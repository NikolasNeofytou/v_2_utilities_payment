from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PaymentIntent, Payment


@api_view(["POST"])
def payment_webhook(request):
    """Handle payment gateway callbacks.

    Expected payload:
    {
        "intent_id": "token",
        "status": "succeeded" | "failed",
        "charge_id": "gw_123",
        "method": "card",
        "fee": "0.30",
        "net": "9.70"
    }
    """
    data = request.data
    intent_token = data.get("intent_id")
    status = data.get("status")

    if not intent_token or not status:
    missing_fields = []
    if not intent_token:
        missing_fields.append("intent_id")
    if not status:
        missing_fields.append("status")
    if missing_fields:
        return Response(
            {"detail": f"Missing required fields: {', '.join(missing_fields)}"},
            status=400
        )

    try:
        intent = PaymentIntent.objects.get(pay_link_token=intent_token)
    except PaymentIntent.DoesNotExist:
        return Response({"detail": "Payment intent not found"}, status=404)

    if status == "succeeded":
        Payment.objects.create(
            intent=intent,
            gateway_charge_id=data.get("charge_id", ""),
            captured_at=timezone.now(),
            method=data.get("method", ""),
            fee=data.get("fee", 0),
            net=data.get("net", 0),
        )

    intent.status = status
    intent.save(update_fields=["status"])

    return Response({"status": "ok"})
