import { Box, TextField, Button, Typography, Link } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { baseURL } from "../baseURL";
import axios from "axios";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    // Implement your registration logic here
    console.log("Registering user:", { username, password, confirmPassword });
    const userDetails = {
      username: username,
      password: password,
    };
    try {
      await axios.post(`${baseURL}/register`, userDetails);
    } catch (error) {
      alert("Error registering " + error);
    }
    navigate("/login");
  };

  const isPasswordsMatch = password === confirmPassword;

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "#f5f5f5",
      }}>
      <Box
        sx={{
          backgroundColor: "#fff",
          padding: "2rem",
          borderRadius: "8px",
          boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
          width: "400px",
          maxWidth: "90%",
        }}>
        <Typography variant="h4" gutterBottom>
          Register
        </Typography>
        <TextField
          label="Username"
          variant="outlined"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          margin="normal"
          fullWidth
        />
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          margin="normal"
          fullWidth
        />
        <TextField
          label="Confirm Password"
          type="password"
          variant="outlined"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          margin="normal"
          fullWidth
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleRegister}
          sx={{ marginTop: "1rem", width: "100%" }}
          disabled={!isPasswordsMatch}>
          Register
        </Button>
        <Box sx={{ textAlign: "center", marginTop: "1rem" }}>
          <Typography variant="body1">
            Already have an account?{" "}
            <Link href="/login" color="primary">
              Login
            </Link>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default RegisterPage;
