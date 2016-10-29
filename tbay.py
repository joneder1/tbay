from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    #The foreign key constraint specifies that a matching value must exist in a specified column of a different table
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    #item to bids -> one to many
    bids = relationship('Bid', backref='Item')
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    #user to items -> one to many - users can have multiple auction items
    auction_item = relationship('Item', backref='user')
    #user to bids -> one to many - users can bid on multiple items
    bid = relationship('Bid', backref='bidder')
    
class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    #users can have multiple bids
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    #items can have multiple bids
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)

Base.metadata.create_all(engine)

beyonce = User(username="bknowles", password="uhohuhohuhohohnana")
session.add(beyonce)
session.commit()

jon = User(username="joneder", password="lalala")
session.add(jon)
session.commit()

mike = User(username="mikehauer", password="lol")
session.add(mike)
session.commit()

ryan = User(username="ryantempest", password="wow")
session.add(ryan)
session.commit()

baseball = Item(name="Autographed baseball", description="Baseball signed by Barry Bonds", user=beyonce)
session.add(baseball)
session.commit()

#is this the best way to add all of these bids?

bid1 = Bid(price="50.00", bidder=jon, Item=baseball)
session.add(bid1)
session.commit()

bid2 = Bid(price="75.00", bidder=jon, Item=baseball)
session.add(bid2)
session.commit()

bid3 = Bid(price="55.00", bidder=mike, Item=baseball)
session.add(bid3)
session.commit()

bid4 = Bid(price="85.00", bidder=mike, Item=baseball)
session.add(bid4)
session.commit()

bid5 = Bid(price="40.00", bidder=ryan, Item=baseball)
session.add(bid5)
session.commit()

bid6 = Bid(price="60.00", bidder=ryan, Item=baseball)
session.add(bid6)
session.commit()



