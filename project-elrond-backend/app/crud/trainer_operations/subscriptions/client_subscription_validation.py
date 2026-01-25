from sqlalchemy.orm import Session
from sqlalchemy import select, exc
from uuid import UUID
from datetime import datetime, timezone
from app.db.models import ClientSubscription, PaymentStatus


def is_client_subscription_active(
    db: Session, client_id: UUID, trainer_id: UUID
) -> bool:
    try:
        current_time = datetime.now(timezone.utc)
        active_statuses = [PaymentStatus.MOCKED_PAID, PaymentStatus.MOCKED_FREE]

        statement = select(ClientSubscription).where(
            ClientSubscription.client_id == client_id,
            ClientSubscription.trainer_id == trainer_id,
            ClientSubscription.status.in_(active_statuses),
            ClientSubscription.end_date >= current_time,
        )

        return db.scalar(statement) is not None
        
    except exc.SQLAlchemyError as e:
        raise RuntimeError(f"Database error during subscription validation: {str(e)}")