from pony.orm import Required, Optional, Set
from .base import Base_Model
from datetime import datetime

class Appointment(Base_Model):
    _table_ = 'appointments'
    appointment_customer = Required('Customer')
    appointment_veterinarian = Required('Veterinarian')
    appointment_time = Required(datetime)
    appoinment_status = Required(str)  # e.g., 'scheduled', 'completed', 'cancelled'
    appointment_type = Required(str)  # e.g., 'online', 'in-house', 'home service'
    appointment_notes = Optional(str)