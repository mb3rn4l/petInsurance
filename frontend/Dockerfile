# Use a lightweight Node image
FROM node:20-alpine

# Working directory
WORKDIR /app

# Copy package and cache for optimal installation
COPY package*.json ./

# Install all dependencies
RUN npm install

# Copy the VueJS project code into the image
COPY . .

# Vite usually uses port 5173
EXPOSE 5173

# Run Vite binding to the virtual machine environment using --host
CMD ["npm", "run", "dev", "--", "--host"]
