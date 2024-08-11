# user_management_service/app/services/subscription_service.py

from sqlalchemy.orm import Session
from app.models.subscription import Subscription
from app.schemas.subscription_schema import SubscriptionCreate, SubscriptionUpdate

class SubscriptionService:

    @staticmethod
    def create_subscription(db: Session, user_id: int, subscription: SubscriptionCreate):
        db_subscription = Subscription(user_id=user_id, **subscription.dict())
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription

    @staticmethod
    def get_user_subscriptions(db: Session, user_id: int):
        return db.query(Subscription).filter(Subscription.user_id == user_id).all()

    @staticmethod
    def update_subscription(db: Session, subscription_id: int, subscription: SubscriptionUpdate):
        db_subscription = db.query(Subscription).filter(Subscription.subscription_id == subscription_id).first()
        if db_subscription:
            for key, value in subscription.dict(exclude_unset=True).items():
                setattr(db_subscription, key, value)
            db.commit()
            db.refresh(db_subscription)
        return db_subscription
