import React, { useState } from "react";
import { View, Text, TouchableOpacity, StyleSheet } from "react-native";
import { Calendar } from "react-native-calendars";
import axios from "axios";
import { useUser } from "@/contexts/userContext";
import { Appointment, AppointmentType } from "@/types";

export const AppointmentPage: React.FC = () => {
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedType, setSelectedType] = useState<AppointmentType | null>(
    null
  );
  const [selectedTime, setSelectedTime] = useState("");
  const { user } = useUser();

  const handleDateSelect = (date: string) => {
    setSelectedDate(date);
  };

  const handleTypeSelect = (type: AppointmentType) => {
    setSelectedType(type);
  };

  const handleTimeSelect = (time: string) => {
    setSelectedTime(time);
  };

  const bookAppointment = async () => {
    if (!selectedDate || !selectedType || !selectedTime) {
      console.error("Please select all appointment details");
      return;
    }

    try {
      const appointmentData: Omit<Appointment, "id"> = {
        type: selectedType,
        date: selectedDate,
        time: selectedTime,
        duration:
          selectedType === "online"
            ? 60
            : selectedType === "inPerson"
            ? 120
            : 60,
      };

      const response = await axios.post<Appointment>(
        "/book_appointment",
        appointmentData,
        {
          headers: { Authorization: `Bearer ${user?.token}` },
        }
      );

      console.log("Appointment booked:", response.data);
      // Handle successful booking (show confirmation, navigate back, etc.)
    } catch (error) {
      console.error("Error booking appointment:", error);
      // Handle booking error (show error message to user)
    }
  };

  const renderTimeSlots = () => {
    // Generate time slots based on appointment type
    const slots = [];
    const startHour = 9; // 9 AM
    const endHour = 17; // 5 PM

    for (let hour = startHour; hour < endHour; hour++) {
      if (selectedType === "online" || selectedType === "fullConsultation") {
        slots.push(`${hour}:00`);
      }
      if (selectedType === "inPerson" && hour % 2 === 0) {
        slots.push(`${hour}:00`);
      }
    }

    return slots.map((time) => (
      <TouchableOpacity
        key={time}
        style={[
          styles.timeSlot,
          selectedTime === time && styles.selectedTimeSlot,
        ]}
        onPress={() => handleTimeSelect(time)}
      >
        <Text style={styles.timeSlotText}>{time}</Text>
      </TouchableOpacity>
    ));
  };

  return (
    <View style={styles.container}>
      <Calendar
        onDayPress={(day: any) => handleDateSelect(day.dateString)}
        markedDates={{
          [selectedDate]: { selected: true, selectedColor: "blue" },
        }}
      />
      <View style={styles.typeContainer}>
        <TouchableOpacity
          style={[
            styles.typeButton,
            selectedType === "online" && styles.selectedTypeButton,
          ]}
          onPress={() => handleTypeSelect("online")}
        >
          <Text>Online (1 hour)</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.typeButton,
            selectedType === "inPerson" && styles.selectedTypeButton,
          ]}
          onPress={() => handleTypeSelect("inPerson")}
        >
          <Text>In Person (2 hours)</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.typeButton,
            selectedType === "fullConsultation" && styles.selectedTypeButton,
          ]}
          onPress={() => handleTypeSelect("fullConsultation")}
        >
          <Text>Full Consultation</Text>
        </TouchableOpacity>
      </View>
      {selectedType && (
        <View style={styles.timeContainer}>{renderTimeSlots()}</View>
      )}
      <TouchableOpacity style={styles.bookButton} onPress={bookAppointment}>
        <Text style={styles.bookButtonText}>Book Appointment</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#f5f5f5",
  },
  input: {
    backgroundColor: "#ffffff",
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  otpContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 20,
  },
  otpInput: {
    width: 40,
    height: 40,
    borderWidth: 1,
    borderColor: "#4CAF50",
    borderRadius: 5,
    textAlign: "center",
  },
  button: {
    backgroundColor: "#4CAF50",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
  },
  buttonText: {
    color: "#ffffff",
    fontWeight: "bold",
  },
  typeContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 20,
  },
  typeButton: {
    padding: 10,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: "#4CAF50",
  },
  selectedTypeButton: {
    backgroundColor: "#4CAF50",
  },
  timeContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginTop: 20,
  },
  timeSlot: {
    padding: 10,
    margin: 5,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: "#4CAF50",
  },
  selectedTimeSlot: {
    backgroundColor: "#4CAF50",
  },
  timeSlotText: {
    color: "#000000",
  },
  bookButton: {
    backgroundColor: "#4CAF50",
    padding: 15,
    borderRadius: 5,
    alignItems: "center",
    marginTop: 20,
  },
  bookButtonText: {
    color: "#ffffff",
    fontWeight: "bold",
  },
});
