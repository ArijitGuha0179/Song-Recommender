# Song Recommender AI

This is a web application that recommends song to users based on inputs that the users give like the genre of the song they want to listen, they year around which the song was released and the artist they want to listen. The frontend is built with React while the backend is built using Flask. An ML model is built which is the core of our application and the application is also containerized using docker. 

## Working and Features 

#### Data and Model

The core of the recommendation engine is a machine learning model trained on a dataset obtained from Kaggle. The dataset contains various features related to songs, including artist names, song titles, release years, and numerical audio features such as acousticness, duration, energy, loudness, and more. Through extensive analysis, it was observed that songs within the same genre tend to exhibit similar numerical audio feature patterns. Thus, I have made clusters of songs exhibiting similar property using K-means.

To leverage this insight, the project utilizes the spotipy Python client to interact with the Spotify Web API. For a given song input, the system fetches the corresponding audio features from Spotify. Subsequently, it employs cosine similarity to compare these features against the project's database, identifying the top 12 most similar songs based on their numerical audio characteristics. This approach enables the recommendation engine to suggest songs that are likely to resonate with the user's musical preferences.

#### Backend and Frontend

The backend of the application is built using Flask, a popular Python web framework. It incorporates user authentication and registration functionalities, allowing users to create accounts and securely access the recommendation system. The backend also handles the integration with the recommendation model, processing user inputs, and storing user details and recommended songs in a SQLite database. The backend contains 3 APIs:
- POST /  : [{"name": "", "artists":"","year":}]
- POST /login : {"username":"","password":""}
- POST /register:{"username":"","password":""}
The frontend of the application is developed using React, a powerful JavaScript library for building user interfaces. It provides an intuitive and responsive user experience, enabling users to seamlessly interact with the recommendation system, search for songs, view recommendations, and manage their preferences.

#### Containerization with Docker

To ensure consistent deployment and scalability, the project is containerized using Docker. Separate dockerfiles are created for the frontend and backend components, enabling efficient and isolated builds. Docker Compose is employed to integrate and orchestrate the containers, streamlining the deployment process and ensuring seamless communication between the various components of the application.

## Getting Started

### Prerequisites

Before running the application make sure the following applications are installed

- Docker : [docker](https://docs.docker.com/engine/install/)
- Docker Compose: [docker-compose](https://docs.docker.com/compose/install/)
- Git: [git ](https://github.com/git-guides/install-git)
### Installing and Running the application

To install and run the application, follow the steps based on your operating system:
#### Windows

1. Open a command prompt or PowerShell window
2. Clone the project repo using the command
   ```git clone https://github.com/ArijitGuha0179/Song-Recommender.git ```
3. Navigate to the project directory:
	```cd Song-Recommender```
4. Start the application using Docker Compose:
	```docker-compose up --build```
5. Wait for the Containers to build and start. Once the process is complete, you can access the application in your web browser at http://localhost:8080

#### Linux

1. Open a terminal
2. Clone the project repo using the command
   ```git clone https://github.com/ArijitGuha0179/Song-Recommender.git ```
3. Navigate to the project directory:
	```cd Song-Recommender```
4. Start the application using Docker Compose:
	```docker-compose up --build```
5. Wait for the Containers to build and start. Once the process is complete, you can access the application in your web browser at http://localhost:8080

## TechStack

- Flask
- React Js
- Python3
- SQLite db
- Docker
- Numpy
- Pandas
- Scikit-Learn