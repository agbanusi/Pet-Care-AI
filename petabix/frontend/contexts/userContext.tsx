import { User } from "@/types";
import React, { createContext, useState, useContext, ReactNode } from "react";

interface UserContextType {
  user: User | null;
  login: (userData: User) => void;
  logout: () => void;
}

const MainUserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<any>(null);

  const login = (userData: any) => {
    setUser(userData);
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <MainUserContext.Provider value={{ user, login, logout }}>
      {children}
    </MainUserContext.Provider>
  );
};

export const useUser = (): UserContextType => {
  const context = useContext(MainUserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
