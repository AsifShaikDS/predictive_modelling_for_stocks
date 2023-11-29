# Build the Docker image using the commmand
docker build -t app .

# Run the Docker Container
docker run -p 4000:80 app

# Streamlit app will run on port 80 inside the container, and you are exposing it on port 4000 on your host machine.

# Created a v1.0.0 tag, run the following command. This puts the repository in a "detached HEAD" state
git checkout tags/v1.0.0


