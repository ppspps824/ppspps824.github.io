const gameSites = [
    "https://example-game1.com",
    "https://example-game2.com"
];

async function fetchGameSiteData(url) {
    try {
        const response = await fetch(`${url}/manifest.json`);
        const manifest = await response.json();

        const iconUrl = `${url}/${manifest.icons[0].src}`;
        const name = manifest.name || manifest.short_name;

        return { name, iconUrl, link: url };
    } catch (error) {
        console.error("Error fetching manifest:", error);
        return null;
    }
}

async function loadGameSites() {
    const container = document.getElementById("game-list");

    for (const url of gameSites) {
        const siteData = await fetchGameSiteData(url);
        if (siteData) {
            const linkElement = document.createElement("a");
            linkElement.href = siteData.link;
            linkElement.classList.add("game-link");
            linkElement.innerHTML = `
          <img src="${siteData.iconUrl}" alt="${siteData.name} icon" />
          <span>${siteData.name}</span>
        `;
            container.appendChild(linkElement);
        }
    }
}

loadGameSites();

// Service Worker登録
if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("service-worker.js").then(() => {
        console.log("Service Worker registered successfully.");
    }).catch((error) => {
        console.error("Service Worker registration failed:", error);
    });
}
