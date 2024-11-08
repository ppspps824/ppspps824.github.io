class App {
    constructor() {
        this.canvas = document.createElement('canvas');
        this.canvas.width = window.innerWidth - 25;
        this.canvas.height = window.innerHeight - 25;
        document.body.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');

        // 色の定義
        this.colors = [
            '#ffffff', // 7
            '#ff77a8', // 8
            '#ff9d81', // 9
            '#fff024', // 10
            '#00e756', // 11
            '#29adff', // 12
            '#ff77a8'  // 14
        ];

        this.fireworks = [];

        // イベントリスナーの設定
        document.addEventListener('click', () => this.createFirework());
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.createFirework();
        });

        // メインループの開始
        this.update();

        // 音声オブジェクトを事前に作成
        this.audio_hyu = new Audio('assets/hyu.mp3');
        this.audio_bomb = new Audio('assets/bomb.mp3');
    }

    createNormalParticles(fw) {
        for (let i = 0; i < 45; i++) {
            const angle = Math.random() * Math.PI * 5;
            const speed = Math.random() * 2 + 0.5;
            fw.particles.push({
                x: 0,
                y: 0,
                dx: speed * Math.cos(angle),
                dy: speed * Math.sin(angle),
                life: 100
            });
        }
        // 効果音の再生
        this.audio_bomb.currentTime = 0;  // 再生位置をリセット
        this.audio_bomb.play();
    }

    createFirework() {
        // 新しい花火を作成
        this.fireworks.push({
            x: Math.random() * (this.canvas.width - 10) + 10,
            y: this.canvas.height,
            target_y: Math.random() * this.canvas.height * 0.5,
            speed: 4,
            particles: [],
            color: this.colors[Math.floor(Math.random() * this.colors.length)],
            state: 'rising'
        });

        // 効果音の再生
        this.audio_hyu.currentTime = 0;  // 再生位置をリセット
        this.audio_hyu.play();
    }

    update() {
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        for (let i = this.fireworks.length - 1; i >= 0; i--) {
            const fw = this.fireworks[i];

            if (fw.state === 'rising') {
                fw.y -= fw.speed;
                if (fw.y <= fw.target_y) {
                    fw.state = 'exploding';
                    this.createNormalParticles(fw);
                }
                // 打ち上げ中の花火を描画
                this.ctx.fillStyle = fw.color;
                this.ctx.fillRect(fw.x, fw.y, 5, 5);
            } else if (fw.state === 'exploding') {
                let allDead = true;

                for (const p of fw.particles) {
                    if (p.life > 0) {
                        allDead = false;
                        p.x += p.dx;
                        p.y += p.dy;
                        p.dy += 0.1; // 重力
                        p.life--;

                        // パーティクルの描画
                        this.ctx.fillStyle = p.life > 15 ? fw.color : this.fadeColor(fw.color);
                        this.ctx.fillRect(fw.x + p.x, fw.y + p.y, 5, 5);
                    }
                }

                if (allDead) {
                    this.fireworks.splice(i, 1);
                }
            }
        }

        requestAnimationFrame(() => this.update());
    }

    fadeColor(color) {
        // 色を暗くする簡単な実装
        return color === '#ffffff' ? '#666666' : color;
    }
}

// アプリケーションの開始
window.addEventListener('DOMContentLoaded', () => {
    new App();
});