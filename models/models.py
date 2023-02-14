from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from database.database import Base


class CreateUserDetails(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(45))
    lastname = Column(String(45))
    phone_no = Column(String(45))
    email = Column(String(45))
    dob = Column(Date)
    address = Column(String(45))

    def __repr__(self):
        return f"Record(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, phone_no={self.phone_no}, email={self.email}, dob={self.dob}, address={self.address})"
