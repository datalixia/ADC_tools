# Base image
FROM node:16.16.0-alpine3.16

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy the rest of the application
COPY . .

# Expose the port Vue uses
ENV PORT=5010
EXPOSE 5010

# Default command (can be overridden by docker-compose)
CMD ["npm", "run", "dev"]
