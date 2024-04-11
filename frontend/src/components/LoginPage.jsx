import { Box, TextField, Button, Typography, Link } from "@mui/material";
import axios from "axios";
import { useContext, useState } from "react";
import { baseURL } from "../baseURL";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async () => {
    // Implement your login logic here
    console.log("Logging in user:", { username, password });
    const userDetails = {
      username: username,
      password: password,
    };
    try {
      const response = await axios.post(`${baseURL}/login`, userDetails);
      const token = await response.data.access_token;
      console.log(token)
      login(token);
      navigate("/");
    } catch (error) {
      alert("Error Logging " + error);
    }
  };

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
          Login
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
        <Button variant="contained" color="primary" onClick={handleLogin} sx={{ marginTop: "1rem", width: "100%" }}>
          Login
        </Button>
        <Box sx={{ textAlign: "center", marginTop: "1rem" }}>
          <Typography variant="body1">
            Don&apos;t have an account?{" "}
            <Link href="/register" color="primary">
              Register
            </Link>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};

export default LoginPage;
