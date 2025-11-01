from datetime import datetime
from sqlalchemy.orm import Session, with_loader_criteria

from sqlalchemy import Boolean, Column, DateTime, event

class TimestampsMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
class ActiveMixin:
    is_active = Column(Boolean, server_default="1")


@event.listens_for(Session, "do_orm_execute")
def filtering_active_criteria(execute_state):
    skip_filter = execute_state.execution_options.get("skip_filter", False)
    if execute_state.is_select and not skip_filter:
        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                ActiveMixin,
                lambda cls: cls.is_active.is_(True),
                include_aliases=True,
            )
        )