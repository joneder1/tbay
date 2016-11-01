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

#Perform a query to find out which user placed the highest bid

def highest_bid(item_id):
    #query item name where item id equals bid item id
    item = session.query(Item.name).filter(Item.id == item_id).first()
    #query bidder id and their bid prices, sort by descending, return highest
    highest_bid = session.query(Bid.bidder_id, Bid.price).\
        filter(Bid.item_id == item_id).\
        order_by(Bid.price.desc()).first()
    #query user name where user id matches highest bidder user id
    winning_bidder = session.query(User.username).filter(User.id == highest_bid[0])
    template = "The '{0}' auction has been won by {1} with a bid of ${2}.".format(
        item[0], winning_bidder[0], highest_bid[1])
    return template

#get the highest item id #1
print(highest_bid(1))

#print("Found '{}' in these messages".format(arguments['string']))
#item[0], winning_bidder[0], highest_bid[1])