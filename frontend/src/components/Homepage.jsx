import { Box, Button, TextField, Typography } from "@mui/material";
import Autocomplete from "@mui/material/Autocomplete";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
/* eslint-disable react/prop-types */
import { useContext, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { baseURL } from "../baseURL";
import { AuthContext } from "../context/AuthContext";

const top10Songs = [
  { label: "The Diary of Jane - Single Version" },
  { label: "99 Ways To Die" },
  { label: "This Is the House That Doubt BuiltTake It Off" },
  { label: "Take It Off" },
  { label: "Faceless" },
  { label: "Stay Away" },
];

const temp = "['Breaking Benjamin', ' Florida Georgia Line', ' Florida Georgia Line']";

const Homepage = () => {
  const [selectedDate, handleDateChange] = useState(null);
  const [songName, setSongName] = useState("");
  const [recommendedSongs, setRecommendedSongs] = useState([]);
  const [artist, setArtist] = useState("");
  const navigate = useNavigate();

  const { logout } = useContext(AuthContext);

  const handleSubmit = async () => {
    try {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken) {
        // If the access token is not found, redirect the user to the login page
        navigate("/login");
        return;
      }
      const song_details = {
        name: songName,
        year: selectedDate ? selectedDate.year() : null,
        artists: artist,
      };
      console.log(song_details);
      const response = await axios.post(`${baseURL}`, song_details, {
        headers: {
          "X-Access-Token": accessToken,
        },
      });
      console.log("Song recommendation submitted successfully");
      setRecommendedSongs(await response.data);
      console.log(await response.data);
    } catch (error) {
      // Handle error
      console.error("Error submitting song recommendation:", error);
      alert("Please try again");
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        width: "100%",
        marginTop: "2rem",
      }}>
      <Box
        sx={{
          display: "flex",
          width: "100%",
          justifyContent: "space-between",
          marginBottom: "3rem",
        }}>
        <Box sx={{ flex: 1, display: "flex", justifyContent: "center" }}>
          <Typography variant="h4">Song Recommendor</Typography>
        </Box>
        <Button variant="outlined" color="primary" sx={{ textTransform: "capitalize" }} onClick={handleLogout}>
          Logout
        </Button>
      </Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          width: "100%",
        }}>
        <Box
          sx={{
            marginRight: "1rem",
          }}>
          <Autocomplete
            disablePortal
            freeSolo
            id="combo-box-demo"
            options={top10Songs}
            inputValue={songName}
            onInputChange={(event, newInputValue) => {
              setSongName(newInputValue);
            }}
            sx={{ width: 300 }}
            renderInput={(params) => <TextField {...params} label="Search Song" />}
          />
        </Box>
        <Box
          sx={{
            marginRight: "1rem",
          }}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DatePicker
              views={["year"]}
              label="Select Year"
              value={selectedDate}
              onChange={handleDateChange}
              animateYearScrolling
            />
          </LocalizationProvider>
        </Box>
        <Box
          sx={{
            marginRight: "1rem",
          }}>
          <TextField
            label="Artist"
            placeholder="Choose Artist"
            value={artist}
            onChange={(event) => setArtist(event.target.value)}
            variant="outlined"
            fullWidth
          />
        </Box>
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
          }}>
          <Button variant="contained" onClick={handleSubmit}>
            Submit
          </Button>
        </Box>
      </Box>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          padding: "2rem",
          boxSizing: "border-box",
        }}>
        <Box
          sx={{
            display: "flex",
            flexWrap: "wrap",
            justifyContent: "space-around",
          }}>
          {recommendedSongs.map((song, index) => (
            <SongCard key={index} song={song} />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

const SongCard = ({ song }) => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        backgroundColor: "#f5f5f5",
        padding: "1.5rem",
        width: "30%",
        borderRadius: "8px",
        boxSizing: "border-box",
        boxShadow: "0 2px 6px rgba(0, 0, 0, 0.1)",
        marginBottom: "1rem",
      }}>
      <Box>
        <Typography variant="h5" gutterBottom>
          {song.name}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Artists:{" "}
          <Box
            sx={{
              display: "flex",
            }}>
            {eval(song.artists).map((element, index) => {
              console.log(element);
              return (
                <Typography variant="body1" color="text.secondary" key={index}>
                  {element}
                </Typography>
              );
            })}
          </Box>
        </Typography>
      </Box>
      <Typography variant="h6">{song.year}</Typography>
    </Box>
  );
};

export default Homepage;
