FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production 2>/dev/null || npm install --only=production || npm install
COPY . .
ENV PORT=3000
ENV BRANCH=unknown
EXPOSE 3000
CMD ["npm", "start"]
