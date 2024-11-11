const config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    // フレームレートを制御するための設定を追加
    fps: {
        target: 10,    // 1秒間に10フレーム
        forceSetTimeOut: true
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

const game = new Phaser.Game(config);

let player; // キャラクター
let isSwiping = false; // スワイプ中かどうかのフラグ
let isTouch = false; // タッチ中かどうかのフラグ
let lastPointerPosition = { x: 0, y: 0 }; // 前回のタッチ位置
let images = []; // 画像配列
let isSpinning = true; // ルーレットが回転中かどうか
let spinSpeed = 0.1; // 回転速度
let currentIndex = 0; // 現在表示している画像のインデックス

function preload() {
    // 画像を001から055までロード
    for (let i = 1; i <= 55; i++) {
        const imageNumber = i.toString().padStart(3, '0');
        this.load.image(`image${i}`, `assets/${imageNumber}.png`);
    }

    // 音声ファイルをロード
    this.load.audio('roulette_sound', 'assets/roulette_sound.mp3');
    this.load.audio('roulette_stop_sound', 'assets/roulette_stop_sound.mp3');
}

function create() {
    // 画像キー配列を1から55まで生成
    const imageKeys = Array.from({ length: 55 }, (_, i) => `image${i + 1}`);
    imageKeys.forEach(key => {
        const image = this.add.sprite(400, 300, key);
        image.setVisible(false);
        images.push(image);
    });

    // 最初の画像を表示
    images[0].setVisible(true);
    this.sound.play('roulette_sound');

    // クリックとキーボードイベントの追加
    this.input.on('pointerdown', () => {
        isSpinning = true;
        this.sound.play('roulette_sound');
    });

    this.input.keyboard.on('keydown-ENTER', () => {
        isSpinning = true;
        this.sound.play('roulette_sound');
    });

    this.input.keyboard.on('keydown-NUMPAD_ENTER', () => {
        isSpinning = true;
        this.sound.play('roulette_sound');
    });
}

function update() {
    if (isSpinning) {
        // 現在の画像を非表示
        images[currentIndex].setVisible(false);

        // 次の画像のインデックスを計算
        currentIndex = (currentIndex + 1) % images.length;

        // 次の画像を表示
        images[currentIndex].setVisible(true);

        // 3秒後に停止
        if (!this.spinTimer) {
            // 2～3.5秒のランダムな時間を待つ
            const randomTime = Phaser.Math.Between(2000, 3500);
            this.spinTimer = this.time.delayedCall(randomTime, () => {
                // ルーレット音を停止
                this.sound.stopAll();
                // ルーレット停止音再生
                this.sound.play('roulette_stop_sound');
                isSpinning = false;
                this.spinTimer = null;
            }, [], this);
        }
    }
}
