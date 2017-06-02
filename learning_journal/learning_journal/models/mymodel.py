from sqlalchemy import (
    Column,
    Integer,
    Unicode
)

from .meta import Base


class JournalEntries(Base):
    """Journal entry."""
    
    __tablename__ = 'journal'
    id = Column(Integer, primary_key=True),
    title = Column(Unicode),
    text = Column(Unicode),
    author = Column(Unicode),
    date = Column(Unicode)
