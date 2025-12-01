from database import database
from fastapi import APIRouter, HTTPException
from schemas.payments import Payments, PaymentsRead
from crud.payments_crud import get_payment, get_payments_by_order, create_payment, delete_payment

router = APIRouter(prefix="/api/Payments", tags=["Payments"])

@router.get("/{payment_id}", response_model=PaymentsRead)
async def api_get_payment(payment_id: int):
    async with database:
        d = await get_payment(payment_id)
        if not d:
            raise HTTPException(status_code=404, detail="Payment not found")
        return PaymentsRead(**d)

@router.get("/payments/{order_id}", response_model=list[PaymentsRead])
async def api_get_payments_by_order(order_id: int):
    async with database:
        rows = await get_payments_by_order(order_id)
        return [PaymentsRead(**dict(r)) for r in rows]

@router.post("/", response_model=PaymentsRead)
async def api_create_payment(payment: Payments):
    async with database:
        try:
            payment_id = await create_payment(payment.order_id, payment.amount, payment.method)
            return PaymentsRead(payment_id=payment_id, **payment.dict())
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))

@router.delete("/{payment_id}")
async def api_delete_payment(payment_id: int):
    async with database:
        deleted = await delete_payment(payment_id)
        if not deleted:
            raise HTTPException(404, "Payment not found")
        return {"detail": "Payment deleted"}