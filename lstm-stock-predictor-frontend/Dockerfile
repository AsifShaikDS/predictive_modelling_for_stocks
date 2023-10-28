# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./

# Install the app's dependencies
RUN npm install

# Copy the entire application source code to the container
COPY . .

# Build the React app
RUN npm run build

# Expose port
EXPOSE 3000

# Start the React app
CMD ["npm", "start"]
