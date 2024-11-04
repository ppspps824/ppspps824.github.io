self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open("static-cache").then((cache) => {
            return cache.addAll(["/", "/index.html", "static/styles.css", "static/app.js", "static/icon-192.png"]);
        })
    );
});

self.addEventListener("fetch", (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
