/* eslint-disable react/prop-types */
// AuthContext.js
import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  //   const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);

  // Function to handle user login
  const login = (token) => {
    setAccessToken(token);
    // Store the token in local storage or cookies
    localStorage.setItem("accessToken", token);
  };

  // Function to handle user logout
  const logout = () => {
    // setUser(null);
    setAccessToken(null);
    // Remove the token from local storage or cookies
    localStorage.removeItem("accessToken");
  };

  // Fetch the access token from storage on component mount
  useEffect(() => {
    const storedToken = localStorage.getItem("accessToken");
    if (storedToken) {
      setAccessToken(storedToken);
    }
  }, []);

  return <AuthContext.Provider value={{ accessToken, login, logout }}>{children}</AuthContext.Provider>;
};
