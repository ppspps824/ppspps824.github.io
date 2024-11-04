const gameSites = [
    ["https://ppspps824.github.io/apps/maze/index.html", "maze"],
    ["https://ppspps824.github.io/apps/fruits_catch/index.html", "fruits_catch"],
];

async function loadGameSites() {
    const container = document.getElementById("game-list");

    for (const url of gameSites) {
        const iconUrl = `${url[0]}/static/icon.png`;
        const name = url[1];

        if (iconUrl) {
            const linkElement = document.createElement("a");
            linkElement.href = url[0];
            linkElement.classList.add("game-link");
            linkElement.innerHTML = `
          <img src="${iconUrl}" alt="${name} icon" />
          <span>${name}</span>
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
