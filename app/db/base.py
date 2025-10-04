from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

holiday_work_shop = Table(
    "holidays_work_shops",
    Base.metadata,
    Column("holidays_id", Integer, ForeignKey("work_shop.holidays.id")),
    Column("work_shop_id", Integer, ForeignKey("work_shop.work_shop.id")),
    schema="work_shop"
)

working_hour_work_shop= Table(
   "working_hour_work_shop",
    Base.metadata,
    Column("working_hour_id", Integer, ForeignKey("work_shop.working_hours.id")),
    Column("work_shop_id", Integer, ForeignKey("work_shop.work_shop.id")),
    schema="work_shop"
)

appointments_work_type_children= Table(
    "appointments_work_type_children",
    Base.metadata,
    Column("appointments_id", Integer, ForeignKey("participants.appointments.id")),
    Column("work_type_children_id", Integer, ForeignKey("cars.type_work_children.id")),
    schema="participants"
)

appointments_work_shop= Table(
    "appointments_work_shop",
    Base.metadata,
    Column("appointments_id", Integer, ForeignKey("participants.appointments.id")),
    Column("work_shop_id", Integer, ForeignKey("work_shop.work_shop.id")),
    schema="participants"
)

appointments_cars= Table(
    "appointments_cars",
    Base.metadata,
    Column("appointments_id", Integer, ForeignKey("participants.appointments.id")),
    Column("cars_id", Integer, ForeignKey("cars.cars.id")),
    schema="participants"
)