import React, { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  Text,
  StyleSheet,
} from "react-native";
import axios from "axios";
import { useUser } from "@/contexts/userContext";
import { NativeStackNavigationProp } from "react-native-screens/lib/typescript/native-stack/types";

type LoginPageProps = {
  navigation: any;
};

export const LoginPage: React.FC<LoginPageProps> = ({ navigation }) => {
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const { login } = useUser();

  const handleLogin = async () => {
    try {
      const response = await axios.post("/login", { email, otp });
      const { userId, token, email: userEmail } = response.data;
      login({ userId, token, email: userEmail });
      navigation.navigate("Chat");
    } catch (error) {
      console.error("Login failed:", error);
      // Handle login error (show message to user)
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />
      <View style={styles.otpContainer}>
        {[...Array(6)].map((_, index) => (
          <TextInput
            key={index}
            style={styles.otpInput}
            maxLength={1}
            keyboardType="number-pad"
            onChangeText={(value) => {
              const newOtp = otp.split("");
              newOtp[index] = value;
              setOtp(newOtp.join(""));
            }}
          />
        ))}
      </View>
      <TouchableOpacity style={styles.button} onPress={handleLogin}>
        <Text style={styles.buttonText}>Login</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
    backgroundColor: "#1E1E1E",
  },
  input: {
    backgroundColor: "#2C2C2C",
    color: "#FFFFFF",
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
    color: "#FFFFFF",
  },
  button: {
    backgroundColor: "#4CAF50",
    padding: 10,
    borderRadius: 5,
    alignItems: "center",
  },
  buttonText: {
    color: "#FFFFFF",
    fontWeight: "bold",
  },
  // ... include styles from ChatComponent here as well
});
