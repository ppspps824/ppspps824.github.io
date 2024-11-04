const gameSites = [
    ["https://ppspps824.github.io/apps/maze/index.html", "maze"],
    ["https://ppspps824.github.io/apps/fruits_catch/index.html", "fruits_catch"],
];

function loadGameSites() {
    const container = document.getElementById("game-list");
    container.innerHTML = '';

    for (const url of gameSites) {
        const iconUrl = `${url[0].replace('/index.html', '')}/static/icon.png`;
        const name = url[1];

        const linkElement = document.createElement("a");
        linkElement.href = "#";
        linkElement.classList.add("game-link");
        linkElement.innerHTML = `
          <img src="${iconUrl}" alt="${name} icon" />
          <span>${name}</span>
        `;

        linkElement.addEventListener('click', (e) => {
            e.preventDefault();
            loadGame(url[0]);
        });

        container.appendChild(linkElement);
    }
}

function loadGame(gameUrl) {
    const container = document.getElementById("game-list");
    container.innerHTML = `
        <div class="game-container">
            <button id="back-button">← 戻る</button>
            <iframe src="${gameUrl}" frameborder="0" width="100%" height="400px"></iframe>
        </div>
    `;

    document.getElementById("back-button").addEventListener('click', () => {
        loadGameSites();
    });
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
