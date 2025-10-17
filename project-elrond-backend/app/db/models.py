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
    # Can have N clients
    clients_trained = relationship(
        "Client",
        secondary="client_trainer_association",
        back_populates="trainers"
    )

    custom_meals = relationship("Meal", back_populates="creator")
    custom_exercises = relationship("Exercise", back_populates="creator")
    
    meal_plans_created = relationship("MealPlan", back_populates="creator")
    exercise_plans_created = relationship("ExercisePlan", back_populates="creator") 



class Client(Base):
    __tablename__ = "clients"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="client_profile")
    #Can have M trainers
    trainers = relationship(
        "Trainer",
        secondary="client_trainer_association",
        back_populates="clients_trained"
    )
    meal_assignments = relationship("MealPlanAssignment", back_populates="client")
    exercise_assignments = relationship("ExercisePlanAssignment", back_populates="client") 


# M:N relationshiop between trainer and client
class ClientTrainerAssociation(Base):
    __tablename__ = "client_trainer_association"
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.user_id"), primary_key=True)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), primary_key=True)
    specialization_type = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint('client_id', 'trainer_id', name='uq_client_trainer_pair'),)

# Trainer Meals
# Flow: 
# 1. Trainer creates meal
# 2. Trainer creates plan
# 3. Trainer add meal
# 4. Trainer specifies meal details
# 5. BE creates MealPlanEntry so the meals stay clean and shiny    

class Meal(Base):
    __tablename__ = "meals"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), index=True, nullable=False)
    creator = relationship("Trainer", back_populates="custom_meals") 


class MealPlanEntry(Base):
    __tablename__ = "meal_plan_entries"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    meal_plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_plans.id"), index=True, nullable=False)
    base_meal_id = Column(UUID(as_uuid=True), ForeignKey("meals.id"), index=True, nullable=False)
    
    serving_size_grams = Column(Integer, nullable=False)
    time_slot = Column(String, nullable=False)          
    notes = Column(String, nullable=True)               
    
    carbohydrates_g = Column(Integer, nullable=False)
    fat_g = Column(Integer, nullable=False)
    protein_g = Column(Integer, nullable=False)
    
    meal_plan = relationship("MealPlan", back_populates="meal_entries")
    base_meal = relationship("Meal")


class MealPlan(Base):
    __tablename__ = "meal_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), index=True, nullable=False) 
    creator = relationship("Trainer", back_populates="meal_plans_created")
    assignments = relationship("MealPlanAssignment", back_populates="meal_plan")
    
    meal_entries = relationship("MealPlanEntry", back_populates="meal_plan")


class MealPlanAssignment(Base):
    __tablename__ = "meal_plan_assignments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.user_id"), nullable=False, index=True)
    meal_plan_id = Column(UUID(as_uuid=True), ForeignKey("meal_plans.id"), nullable=False, index=True)
    client = relationship("Client", back_populates="meal_assignments") 
    meal_plan = relationship("MealPlan", back_populates="assignments") 

# Trainer exercise
# Flow: 
# 1. Trainer creates exercise
# 2. Trainer creates plan
# 3. Trainer add exercise
# 4. Trainer specifies exercise details
# 5. BE creates ExercisePlanEntry so the exercises stay clean and shiny    

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), index=True, nullable=False)
    creator = relationship("Trainer", back_populates="custom_exercises")


class ExercisePlanEntry(Base):
    __tablename__ = "exercise_plan_entries"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    
    exercise_plan_id = Column(UUID(as_uuid=True), ForeignKey("exercise_plans.id"), index=True, nullable=False) 
    base_exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercises.id"), index=True, nullable=False)
    
    sets = Column(Integer, nullable=False)            
    repetitions = Column(String, nullable=False)         
    day_of_week = Column(String, nullable=False)
    order_in_session = Column(Integer, nullable=False) 
    notes = Column(String, nullable=True) 
    
    exercise_plan = relationship("ExercisePlan", back_populates="exercise_entries")
    base_exercise = relationship("Exercise")


class ExercisePlan(Base):
    __tablename__ = "exercise_plans"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    trainer_id = Column(UUID(as_uuid=True), ForeignKey("trainers.user_id"), index=True, nullable=False) 
    
    notes = Column(String, nullable=True) 
    
    creator = relationship("Trainer", back_populates="exercise_plans_created")
    assignments = relationship("ExercisePlanAssignment", back_populates="exercise_plan")
    exercise_entries = relationship("ExercisePlanEntry", back_populates="exercise_plan")


class ExercisePlanAssignment(Base):
    __tablename__ = "exercise_plan_assignments"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.user_id"), nullable=False, index=True)
    exercise_plan_id = Column(UUID(as_uuid=True), ForeignKey("exercise_plans.id"), nullable=False, index=True)
    client = relationship("Client", back_populates="exercise_assignments")
    exercise_plan = relationship("ExercisePlan", back_populates="assignments")