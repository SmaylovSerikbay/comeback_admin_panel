"""
API для эквайринга (Payment Gateway) — доступ по Token, для новой админки.
"""
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import models

from payment_gateway.models import PaymentTransaction, PaymentCallback
from payment_gateway.views import get_base_url, generate_signature, MERCHANT_ID, _create_milliy_transaction
from payment_gateway import milliy_service
from admin_api.permissions import IsAdminOrCashier


def _serialize_transaction(t):
    return {
        "order_id": t.order_id,
        "gateway": t.gateway,
        "amount": t.amount,
        "currency": t.currency,
        "status": t.status,
        "status_display": t.get_status_display(),
        "description": t.description or "",
        "unity_user_id": t.unity_user_id or "",
        "unity_session_id": t.unity_session_id or "",
        "payment_id": t.payment_id,
        "merchant_id": t.merchant_id,
        "milliy_transaction_id": t.milliy_transaction_id,
        "created_at": t.created_at.isoformat(),
        "updated_at": t.updated_at.isoformat(),
        "paid_at": t.paid_at.isoformat() if t.paid_at else None,
    }


class PaymentGatewayDashboardView(APIView):
    """Список транзакций и статистика эквайринга."""
    permission_classes = [IsAdminOrCashier]

    def get(self, request):
        transactions = PaymentTransaction.objects.all().order_by("-created_at")
        stats = {
            "total": transactions.count(),
            "pending": transactions.filter(status="pending").count(),
            "success": transactions.filter(status="success").count(),
            "failed": transactions.filter(status="failed").count(),
            "total_amount": transactions.filter(status="success").aggregate(
                total=models.Sum("amount")
            )["total"]
            or 0,
        }
        page = int(request.GET.get("page", 1))
        per_page = min(int(request.GET.get("per_page", 50)), 100)
        start = (page - 1) * per_page
        end = start + per_page
        page_qs = transactions[start:end]
        list_data = [_serialize_transaction(t) for t in page_qs]
        return Response(
            {
                "stats": stats,
                "transactions": list_data,
                "total": transactions.count(),
                "page": page,
                "per_page": per_page,
            }
        )


class PaymentGatewayTransactionDetailView(APIView):
    """Детали одной транзакции и коллбэки."""
    permission_classes = [IsAdminOrCashier]

    def get(self, request, order_id):
        try:
            transaction = PaymentTransaction.objects.get(order_id=order_id)
        except PaymentTransaction.DoesNotExist:
            return Response(
                {"error": "Транзакция не найдена"},
                status=status.HTTP_404_NOT_FOUND,
            )
        callbacks = transaction.callbacks.all().order_by("-created_at")
        callbacks_data = [
            {
                "callback_type": c.callback_type,
                "raw_data": c.raw_data,
                "processed": c.processed,
                "created_at": c.created_at.isoformat(),
            }
            for c in callbacks
        ]
        return Response(
            {
                "transaction": _serialize_transaction(transaction),
                "callbacks": callbacks_data,
            }
        )


class PaymentGatewayTestPaymentView(APIView):
    """Создание тестового платежа. gateway=freedom (по умолчанию) или gateway=milliy."""
    permission_classes = [IsAdminOrCashier]

    def post(self, request):
        gateway = request.data.get("gateway", "freedom")
        amount = request.data.get("amount", 1000)
        description = request.data.get("description", "Test Payment")
        try:
            amount = int(amount)
        except (TypeError, ValueError):
            amount = 1000
        if amount <= 0:
            amount = 1000

        if gateway == "milliy":
            return self._create_milliy(amount, description)
        return self._create_freedom(amount, description)

    def _create_freedom(self, amount, description):
        transaction = PaymentTransaction.objects.create(
            order_id=f"test_{uuid.uuid4().hex[:16]}",
            amount=amount,
            currency="UZS",
            description=str(description)[:500],
            salt=uuid.uuid4().hex[:16],
            merchant_id=MERCHANT_ID,
            gateway="freedom",
        )
        base_url = get_base_url()
        params = {
            "pg_merchant_id": MERCHANT_ID,
            "pg_amount": str(amount),
            "pg_currency": "UZS",
            "pg_description": str(description)[:500],
            "pg_salt": transaction.salt,
            "pg_language": "ru",
            "pg_order_id": transaction.order_id,
            "payment_origin": "test_form",
            "pg_success_url": f"{base_url}/payment-gateway/freedompay/success/",
            "pg_fail_url": f"{base_url}/payment-gateway/freedompay/fail/",
        }
        signature, _ = generate_signature(params)
        transaction.signature = signature
        transaction.save()
        query_parts = [f"{k}={params[k]}" for k in sorted(params.keys())]
        query_parts.append(f"pg_sig={signature}")
        payment_url = f"https://api.freedompay.uz/payment.php?{'&'.join(query_parts)}"
        return Response({"payment_url": payment_url, "order_id": transaction.order_id, "gateway": "freedom"})

    def _create_milliy(self, amount, description):
        try:
            transaction, payment_url = _create_milliy_transaction(
                amount=amount,
                description=str(description)[:500],
                unity_user_id="admin_test",
                source="admin_test",
            )
        except milliy_service.MilliyError as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        return Response(
            {
                "payment_url": payment_url,
                "order_id": transaction.order_id,
                "milliy_transaction_id": transaction.milliy_transaction_id,
                "gateway": "milliy",
            }
        )
