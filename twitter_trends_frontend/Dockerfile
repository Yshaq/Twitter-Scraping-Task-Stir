# Use an official Node.js image as the base image
FROM node:18-alpine

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Install dependencies
RUN npm install

# Build the application
RUN npm run build

# Expose port 5173 (default Vite port)
EXPOSE 5173

# Start the application
CMD ["npm", "run", "dev", "--", "--host"]
