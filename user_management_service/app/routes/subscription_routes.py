# user_management_service/app/routes/subscription_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.subscription_schema import SubscriptionCreate, SubscriptionUpdate, Subscription
from app.services.subscription_service import SubscriptionService

router = APIRouter()

@router.post("/subscriptions/", response_model=Subscription)
def create_subscription(user_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    return SubscriptionService.create_subscription(db=db, user_id=user_id, subscription=subscription)

@router.get("/subscriptions/{user_id}/", response_model=list[Subscription])
def get_subscriptions(user_id: int, db: Session = Depends(get_db)):
    return SubscriptionService.get_user_subscriptions(db=db, user_id=user_id)

@router.put("/subscriptions/{subscription_id}/", response_model=Subscription)
def update_subscription(subscription_id: int, subscription: SubscriptionUpdate, db: Session = Depends(get_db)):
    db_subscription = SubscriptionService.update_subscription(db=db, subscription_id=subscription_id, subscription=subscription)
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return db_subscription
