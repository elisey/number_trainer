// Service Worker for Number Trainer PWA
// Provides caching strategies for offline functionality

const CACHE_NAME = 'number-trainer-v1.0.0';
const STATIC_CACHE_NAME = 'number-trainer-static-v1.0.0';
const API_CACHE_NAME = 'number-trainer-api-v1.0.0';

// Files to cache immediately when SW installs
const STATIC_ASSETS = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/icons/math_training_icon.svg',
  '/static/icons/icon-72.png',
  '/static/icons/icon-96.png',
  '/static/icons/icon-128.png',
  '/static/icons/icon-144.png',
  '/static/icons/icon-152.png',
  '/static/icons/icon-192.png',
  '/static/icons/icon-384.png',
  '/static/icons/icon-512.png',
  '/static/manifest.json'
];

// API endpoints to cache
const API_ENDPOINTS = [
  '/api/health'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  console.log('[SW] Installing service worker...');

  event.waitUntil(
    Promise.all([
      // Cache static assets
      caches.open(STATIC_CACHE_NAME).then(cache => {
        console.log('[SW] Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      }),
      // Cache API endpoints
      caches.open(API_CACHE_NAME).then(cache => {
        console.log('[SW] Pre-caching API endpoints');
        return Promise.all(
          API_ENDPOINTS.map(url => {
            return fetch(url).then(response => {
              if (response.ok) {
                return cache.put(url, response);
              }
            }).catch(err => {
              console.log('[SW] Failed to cache API endpoint:', url, err);
            });
          })
        );
      })
    ]).then(() => {
      console.log('[SW] Installation complete');
      // Force activation of new SW
      return self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[SW] Activating service worker...');

  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          // Delete old caches
          if (cacheName !== STATIC_CACHE_NAME &&
              cacheName !== API_CACHE_NAME &&
              cacheName.startsWith('number-trainer-')) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('[SW] Activation complete');
      // Take control of all clients immediately
      return self.clients.claim();
    })
  );
});

// Fetch event - handle requests with caching strategies
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Only handle requests from our origin
  if (url.origin !== location.origin) {
    return;
  }

  // Choose caching strategy based on request type
  if (url.pathname.startsWith('/api/')) {
    // API requests: Network First with cache fallback
    event.respondWith(handleApiRequest(request));
  } else if (url.pathname.startsWith('/static/')) {
    // Static assets: Cache First
    event.respondWith(handleStaticRequest(request));
  } else {
    // HTML pages: Stale While Revalidate
    event.respondWith(handlePageRequest(request));
  }
});

// Network First strategy for API requests
async function handleApiRequest(request) {
  const cache = await caches.open(API_CACHE_NAME);

  try {
    // Try network first
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      // Cache successful responses
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log('[SW] Network failed for API, trying cache:', request.url);

    // Fall back to cache
    const cachedResponse = await cache.match(request);

    if (cachedResponse) {
      return cachedResponse;
    }

    // If no cache available, return offline response for specific endpoints
    if (request.url.includes('/api/health')) {
      return new Response(JSON.stringify({
        status: 'offline',
        service: 'number-trainer-web',
        message: 'Application is running offline'
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    // For other API endpoints, return error
    return new Response(JSON.stringify({
      error: 'Network unavailable',
      message: 'Please check your internet connection'
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Cache First strategy for static assets
async function handleStaticRequest(request) {
  const cache = await caches.open(STATIC_CACHE_NAME);

  // Try cache first
  const cachedResponse = await cache.match(request);

  if (cachedResponse) {
    return cachedResponse;
  }

  // If not in cache, fetch from network and cache
  try {
    const networkResponse = await fetch(request);

    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }

    return networkResponse;
  } catch (error) {
    console.log('[SW] Failed to fetch static asset:', request.url);

    // Return a fallback for CSS files
    if (request.url.includes('.css')) {
      return new Response('/* Offline - CSS unavailable */', {
        headers: { 'Content-Type': 'text/css' }
      });
    }

    // Return a fallback for JS files
    if (request.url.includes('.js')) {
      return new Response('console.log("Offline - JS unavailable");', {
        headers: { 'Content-Type': 'application/javascript' }
      });
    }

    throw error;
  }
}

// Stale While Revalidate strategy for HTML pages
async function handlePageRequest(request) {
  const cache = await caches.open(STATIC_CACHE_NAME);

  // Get from cache immediately (stale)
  const cachedResponse = await cache.match(request);

  // Fetch from network in background (revalidate)
  const networkResponsePromise = fetch(request).then(response => {
    if (response.ok) {
      cache.put(request, response.clone());
    }
    return response;
  }).catch(error => {
    console.log('[SW] Network failed for page:', request.url);
    return null;
  });

  // Return cached version immediately if available
  if (cachedResponse) {
    // Still update cache in background
    networkResponsePromise;
    return cachedResponse;
  }

  // If no cache, wait for network
  const networkResponse = await networkResponsePromise;

  if (networkResponse) {
    return networkResponse;
  }

  // Fallback offline page
  return new Response(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Number Trainer - Offline</title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, sans-serif;
          text-align: center;
          padding: 20px;
          background: #f8fafc;
          color: #1e293b;
        }
        .container {
          max-width: 400px;
          margin: 50px auto;
          padding: 30px;
          background: white;
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .icon { font-size: 48px; margin-bottom: 20px; }
        h1 { color: #2563eb; margin-bottom: 20px; }
        p { margin-bottom: 20px; line-height: 1.6; }
        button {
          background: #2563eb;
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          cursor: pointer;
          font-size: 16px;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="icon">🧠</div>
        <h1>Number Trainer</h1>
        <p>You're currently offline. Please check your internet connection and try again.</p>
        <button onclick="window.location.reload()">Try Again</button>
      </div>
    </body>
    </html>
  `, {
    headers: { 'Content-Type': 'text/html' }
  });
}

// Handle messages from main thread
self.addEventListener('message', event => {
  console.log('[SW] Received message:', event.data);

  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

console.log('[SW] Service Worker script loaded');
