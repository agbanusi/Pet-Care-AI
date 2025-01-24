from pony.orm import db_session
from models.appointment import Appointment
from models.customer import Customer
from models.veterinarian import Veterinarian
from schemas.appointment import AppointmentCreate, AppointmentUpdate
from fastapi import HTTPException

class AppointmentService:
    @db_session
    async def create_appointment(self, appointment: AppointmentCreate, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        veterinarian = Veterinarian.get(id=appointment.veterinarian_id)
        
        if not customer or not veterinarian:
            raise HTTPException(status_code=400, detail="Invalid customer or veterinarian")
        
        new_appointment = Appointment(
            customer=customer,
            veterinarian=veterinarian,
            date_time=appointment.date_time,
            status=appointment.status,
            type=appointment.type,
            notes=appointment.notes
        )
        return new_appointment

    @db_session
    async def get_appointment(self, appointment_id: int, current_user: dict):
        appointment = Appointment.get(id=appointment_id)
        if not appointment or appointment.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return appointment

    @db_session
    async def list_appointments(self, current_user: dict):
        customer = Customer.get(user=current_user['id'])
        return list(customer.appointments)

    @db_session
    async def update_appointment(self, appointment_id: int, appointment_data: AppointmentUpdate, current_user: dict):
        appointment = Appointment.get(id=appointment_id)
        if not appointment or appointment.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        appointment.set(**appointment_data.dict(exclude_unset=True))
        return appointment

    @db_session
    async def delete_appointment(self, appointment_id: int, current_user: dict):
        appointment = Appointment.get(id=appointment_id)
        if not appointment or appointment.customer.user.id != current_user['id']:
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        appointment.delete()
        return True
