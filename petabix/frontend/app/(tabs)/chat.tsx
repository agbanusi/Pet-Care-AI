import React, { useState, useEffect } from "react";
import {
  View,
  Text,
  TextInput,
  FlatList,
  TouchableOpacity,
  StyleSheet,
} from "react-native";
import axios from "axios";
import { FontAwesome } from "@expo/vector-icons";
import { useUser } from "@/contexts/userContext";

const ChatComponent = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [inputText, setInputText] = useState("");
  const { user } = useUser();

  useEffect(() => {
    fetchChatHistory();
  }, []);

  const fetchChatHistory = async () => {
    try {
      if (!user) {
        return;
      }
      const response = await axios.get(`/chat_history/${user.userId}`);
      setMessages(response.data);
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  const sendMessage = async () => {
    if (inputText.trim() === "") return;
    if (!user) {
      return;
    }

    const userMessage = { text: inputText, sender: "user" };
    setMessages([...messages, userMessage]);
    setInputText("");

    try {
      const response = await axios.post(
        "/chat",
        { message: inputText, userId: user.userId },
        { headers: { Authorization: `Bearer ${user.token}` } }
      );
      const botMessage = { text: response.data.answer, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  const renderMessage = ({ item }: { item: any }) => (
    <View
      style={[
        styles.messageBubble,
        item.sender === "user" ? styles.userBubble : styles.botBubble,
      ]}
    >
      {item.sender === "bot" && (
        <FontAwesome name="image" size={20} color="#000" style={styles.icon} />
      )}
      <Text style={styles.messageText}>{item.text}</Text>
      {item.sender === "user" && (
        <FontAwesome name="user" size={20} color="#000" style={styles.icon} />
      )}
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item, index) => index.toString()}
        style={styles.messageList}
      />
      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={setInputText}
          placeholder="Type a message..."
          placeholderTextColor="#999"
        />
        <TouchableOpacity style={styles.sendButton} onPress={sendMessage}>
          <FontAwesome name="send" size={20} color="#FFFFFF" />
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#1E1E1E",
  },
  messageList: {
    flex: 1,
  },
  messageBubble: {
    flexDirection: "row",
    alignItems: "center",
    maxWidth: "80%",
    padding: 10,
    borderRadius: 15,
    marginVertical: 5,
    marginHorizontal: 10,
  },
  userBubble: {
    alignSelf: "flex-end",
    backgroundColor: "#FF6B6B",
  },
  botBubble: {
    alignSelf: "flex-start",
    backgroundColor: "#FFD93D",
  },
  messageText: {
    color: "#000",
    flex: 1,
  },
  icon: {
    marginHorizontal: 5,
  },
  inputContainer: {
    flexDirection: "row",
    padding: 10,
  },
  input: {
    flex: 1,
    backgroundColor: "#2C2C2C",
    color: "#FFFFFF",
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginRight: 10,
  },
  sendButton: {
    backgroundColor: "#4CAF50",
    borderRadius: 20,
    width: 40,
    height: 40,
    justifyContent: "center",
    alignItems: "center",
  },
});

export default ChatComponent;
