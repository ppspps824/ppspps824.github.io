const gameSites = [
    ["./apps/maze/index.html", "めいろ"],
    ["./apps/fruits_catch/index.html", "フルーツキャッチ"],
    ["./apps/math/index.html", "たしざん"],
    ["./apps/fireworks/index.html", "はなび"],
    ["./apps/car/index.html", "くるま"],
    ["./apps/pict_roulette/index.html", "るーれっと"],
    ["https://fushigiehon-ai.fly.dev/?akdhfauiegfiwpeufhipweufhpiweufyhiapweugrfaweipugf5864149689468=ce8670e3-404d-4929-ba7a-226cbcdd5915&iudfbweuifbwieufwepuifgipweufgiwpefu1685468=readonly", "えほん"]
];

function loadGameSites() {
    const container = document.getElementById("game-list");
    container.innerHTML = '';

    for (const url of gameSites) {
        let iconUrl;
        if (url[0].includes("fushigiehon-ai.fly.dev")) {
            iconUrl = `https://fushigiehon-ai.fly.dev/app/static/icon-512.png`;
        } else {
            iconUrl = `${url[0].replace('/index.html', '')}/app/static/icon-512.png`;
        }
        const name = url[1];

        const linkElement = document.createElement("a");
        linkElement.href = url[0];
        linkElement.target = "_blank";
        linkElement.classList.add("game-link");
        linkElement.innerHTML = `
            <img src="${iconUrl}" alt="ゲームアイコン" class="game-icon" />
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
