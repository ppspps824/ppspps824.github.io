const gameSites = [
    ["./apps/maze/index.html", "めいろ"],
    ["./apps/fruits_catch/index.html", "フルーツキャッチ"],
    ["./apps/math/index.html", "たしざん"],
    ["./apps/fireworks/index.html", "はなび"],
    ["./apps/car/index.html", "くるま"],
    ["./apps/pict_roulette/index.html", "るーれっと"],
    ["https://qiita.com/papasim824/items/9c8f7f84c04c9b37432c", "えほん"]
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
            <a href="${url[0]}" target="_blank" class="game-link-direct">
                <img src="${iconUrl}" alt="ゲームアイコン" class="game-icon" />
            </a>
          <span>${name}</span>
        `;
        container.appendChild(linkElement);
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
