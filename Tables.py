from sqlalchemy import Column, String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Page(Base):
    __tablename__ = 'Page'

    url = Column(String(256), primary_key=True)
    title = Column(String(256))
    date = Column(DateTime)

    def __repr__(self):
        return f"<Page(url='{self.url}', title='{self.title}', date='{self.date}')>"

class Content(Base):
    __tablename__ = 'Content'

    url = Column(String(256), ForeignKey('Page.url'), primary_key=True)
    start_paragraph = Column(Integer, primary_key=True)
    content = Column(String(1024))

    page = relationship("Page", foreign_keys=[url])

    def __repr__(self):
        return f"<Content(url='{self.url}', start_paragraph='{self.start_paragraph}', content='{self.content}')>"
