# ==============================================================================
# FLUX Production Frontend Dockerfile
# Multi-stage build: Node 20 builder -> Nginx Alpine edge server
# ==============================================================================

# --- Stage 1: Build Static Bundle ---
FROM node:20-alpine AS builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
ARG VITE_API_BASE_URL=""
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# --- Stage 2: Serve with Nginx Alpine ---
FROM nginx:1.27-alpine AS runtime

# Remove default nginx html
RUN rm -rf /usr/share/nginx/html/*

# Copy built static artifacts from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost/healthz || exit 1

CMD ["nginx", "-g", "daemon off;"]
