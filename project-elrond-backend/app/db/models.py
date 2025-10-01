import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY, ENUM as PgEnum, UUID # Importujeme UUID
from sqlalchemy.schema import UniqueConstraint
from enum import Enum as PyEnum
from .database import Base 

class Role(PyEnum):
    CLIENT = "client"
    TRAINER = "trainer"
    PENDING = "pending"

role_enum = PgEnum(Role, name="role_enum", create_type=False)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(role_enum, default=Role.PENDING, nullable=False) 
    
    trainer_profile = relationship("Trainer", back_populates="user", uselist=False)
    client_profile = relationship("Client", back_populates="user", uselist=False)


class Trainer(Base):
    __tablename__ = "trainers"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    specialization = Column(String, nullable=True)
    user = relationship("User", back_populates="trainer_profile")
    #Can have N clients
    clients_trained = relationship(
        "Client",
        secondary="client_trainer_association",
        back_populates="trainers"
    )
    meal_plans_created = relationship("MealPlan", back_populates="creator")


class Client(Base):
    __tablename__ = "clients"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    fitness_goal = Column(String, nullable=True)
    user = relationship("User", back_populates="client_profile")
    #Can have M trainers
    trainers = relationship(
        "Trainer",
        secondary="client_trainer_association",
        back_populates="clients_trained"
    )
    assignments = relationship("MealPlanAssignment", back_populates="client")

#M:N relationshiop between trainer and client
class ClientTrainerAssociation(Base):
    """ Vazební tabulka N:M Klient k Trenérovi. """
    __tablename__ = "client_trainer_association"
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.user_id"), primary_key=True)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), primary_key=True)
    specialization_type = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint('client_id', 'trainer_id', name='uq_client_trainer_pair'),)


class Meal(Base):
    """ Základní definice jídla. """
    __tablename__ = "meals"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    

class Exercise(Base):
    """ Základní definice cvičení. """
    __tablename__ = "exercises"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)


class MealPlan(Base):
    """ Definice jídelního plánu. """
    __tablename__ = "meal_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), index=True, nullable=False) 
    meals = Column(ARRAY(UUID(as_uuid=True)), nullable=False) 
    creator = relationship("Trainer", back_populates="meal_plans_created")
    assignments = relationship("MealPlanAssignment", back_populates="meal_plan")


class MealPlanAssignment(Base):
    """ Vazební tabulka: Přiřazení plánu klientovi. """
    __tablename__ = "meal_plan_assignments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.user_id"), nullable=False, index=True)
    meal_plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_plans.id"), nullable=False, index=True)
    client = relationship("Client", back_populates="assignments")
    meal_plan = relationship("MealPlan", back_populates="meal_plan")
