# FLUX CDN Integration & Edge Optimization Guide

This guide outlines the CDN architecture, edge caching policies, SSL/TLS termination, and performance tuning for deploying FLUX to production.

---

## 1. CDN Architecture Overview

```
                      +---------------------------------------+
                      |             End User / Client         |
                      +---------------------------------------+
                                          |
                                          v
                      +---------------------------------------+
                      |   Cloudflare / CloudFront Edge CDN    |
                      |   - Anycast DNS & Edge SSL/TLS        |
                      |   - Brotli / Gzip Edge Compression    |
                      |   - DDoS Mitigation (Layer 3/4/7)     |
                      |   - Geo-Routing (Indian Edge PoPs)    |
                      +---------------------------------------+
                                    /           \
               (Static Assets: Cache Hit)   (API Requests: Pass-Through)
                                  /               \
                                 v                 v
            +-------------------------+     +-------------------------------+
            |  Cloud Storage / Origin |     |     FLUX Production Origin    |
            |  (S3 / Cloudflare Pages)|     |   - Nginx Reverse Proxy / K8s |
            |  Max-Age: 1 Year (Hash) |     |   - FastAPI ASGI Workers      |
            +-------------------------+     +-------------------------------+
```

---

## 2. Caching Strategy & Rules Matrix

FLUX uses a modern two-tier caching strategy designed specifically for Single Page Applications (SPAs) with hashed build artifacts:

| Path / Pattern | Target Content | Cache-Control Header | Edge Cache TTL | Browser Cache TTL | Revalidation |
|---|---|---|---|---|---|
| `/index.html`, `/` | HTML Entrypoint | `no-cache, no-store, must-revalidate` | 0s (Bypass) | 0s | Always revalidate |
| `/assets/*.js`, `/assets/*.css` | Hashed Vite Chunks | `public, max-age=31536000, immutable` | 1 Year (365d) | 1 Year (365d) | Never (immutable) |
| `/assets/*.woff2`, `/assets/*.ttf` | Web Fonts | `public, max-age=31536000, immutable` | 1 Year (365d) | 1 Year (365d) | Never |
| `/*.png`, `/*.svg`, `/*.ico` | Static Media & Favicons | `public, max-age=2592000` | 30 Days | 30 Days | On expiry |
| `/api/*` | Dynamic REST API | `no-store, private` | 0s (Bypass) | 0s | Direct Origin |
| `/api/schemes` | Static Scheme Catalog | `public, max-age=3600, s-maxage=86400` | 24 Hours | 1 Hour | Stale-while-revalidate |

---

## 3. Cloudflare Configuration Guide

### Step 1: DNS & Proxy Setup
1. Point your domain A / CNAME records to your origin load balancer or Cloudflare Pages.
2. Enable Orange Cloud (Proxied) for automatic SSL and CDN distribution.

### Step 2: Cloudflare Page Rules / Cache Rules

Create Cache Rules under **Caching > Cache Rules**:

**Rule 1: Bypass API from Edge Cache**
- **Expression:** `(http.request.uri.path starts_with "/api/")`
- **Action:** Cache Eligibility: *Bypass cache*

**Rule 2: Cache Hashed Assets Aggressively**
- **Expression:** `(http.request.uri.path starts_with "/assets/")`
- **Action:**
  - Cache Eligibility: *Eligible for cache*
  - Edge Cache TTL: *1 year*
  - Browser Cache TTL: *1 year*

**Rule 3: Revalidate HTML Entrypoint**
- **Expression:** `(http.request.uri.path eq "/" or http.request.uri.path eq "/index.html")`
- **Action:**
  - Cache Eligibility: *Bypass cache*
  - Browser Cache TTL: *Respect origin*

### Step 3: Edge Security Headers
Add Transform Rules under **Rules > Transform Rules > Modify Response Header**:
- `Strict-Transport-Security`: `max-age=63072000; includeSubDomains; preload`
- `X-Content-Type-Options`: `nosniff`
- `X-Frame-Options`: `DENY`
- `Referrer-Policy`: `strict-origin-when-cross-origin`

---

## 4. AWS CloudFront Configuration Guide

### Step 1: CloudFront Distribution Origins
Create a distribution with two origins:
1. **S3 Origin (`/`):** Hosting static frontend build artifacts.
2. **ALB / ECS Origin (`/api/*`):** Routing to FastAPI backend.

### Step 2: Cache Behaviors

#### Behavior 1: `/api/*` (API Gateway)
- **Origin:** ALB / Backend Service
- **Viewer Protocol Policy:** Redirect HTTP to HTTPS
- **Allowed HTTP Methods:** `GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`
- **Cache Policy:** `CachingDisabled`
- **Origin Request Policy:** `AllViewerExceptHostHeader`

#### Behavior 2: `/assets/*` (Static Bundles)
- **Origin:** S3 Frontend Bucket
- **Viewer Protocol Policy:** Redirect HTTP to HTTPS
- **Cache Policy:** `Managed-CachingOptimized` (TTL Min 31536000, Max 31536000)
- **Compression:** Enable Gzip & Brotli

#### Behavior 3: `Default (*)` (SPA Fallback)
- **Origin:** S3 Frontend Bucket
- **Error Pages:** Custom Error Response: `403` and `404` -> Response Code `200`, Path `/index.html`.
- **Cache Policy:** `CachingDisabled` or TTL = 0 to prevent caching stale HTML.

---

## 5. Indian Edge PoP Localization & Performance Optimization

Because FLUX is tailored for Indian street vendors and micro-retailers:
- Cloudflare and CloudFront have edge PoPs in **Mumbai (BOM)**, **Delhi (DEL)**, **Chennai (MAA)**, **Bengaluru (BLR)**, **Kolkata (CCU)**, and **Hyderabad (HYD)**.
- Edge Time-to-First-Byte (TTFB) for cached static assets across Indian 4G/5G mobile networks is typically `< 25ms`.
- Voice models and audio synthesizer scripts are pre-cached at the edge to ensure responsive Hindi/Hinglish speech output on low-bandwidth connections.

---

## 6. Cache Invalidation Runbook

When deploying a new frontend version:
```bash
# Cloudflare Pages / API Invalidation:
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
     -H "Authorization: Bearer $CF_API_TOKEN" \
     -H "Content-Type: application/json" \
     --data '{"files":["https://flux.example.com/index.html", "https://flux.example.com/"]}'

# AWS CloudFront Invalidation:
aws cloudfront create-invalidation \
    --distribution-id $DISTRIBUTION_ID \
    --paths "/index.html" "/"
```
*(Note: Because Vite generates distinct hash filenames for JavaScript and CSS bundles, purging `/index.html` instantly switches all users to the newest version without needing to purge `/assets/*`)*.
