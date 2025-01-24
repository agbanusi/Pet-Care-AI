export interface User {
  userId: string;
  token: string;
  email: string;
}

export interface Message {
  text: string;
  sender: "user" | "bot";
}

export type AppointmentType = "online" | "inPerson" | "fullConsultation";

export interface Appointment {
  id: string;
  type: AppointmentType;
  date: string;
  time: string;
  duration: number;
}
