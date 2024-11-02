import json

import pyxel

GAME_DURATION = 30 * 20


class App:
    def __init__(self):

        pyxel.init(160, 120, title="Fruits Catch")
        pyxel.load("assets/my_resource.pyxres")  # リソースファイルの読み込み

        with open(f"assets/music.json", "rt", encoding="utf-8") as fin:
            self.music = json.loads(fin.read())

        pyxel.sound(3).set(  # 果物ゲット時の効果音
            "e3a3", "t", "7", "s", 30  # note  # tone  # volume  # effect  # speed
        )

        pyxel.sound(4).set("c3e3g3c4", "t", "7", "s", 20)  # 星取得時の効果音

        # フルーツの種類を定義
        self.FRUIT_TYPES = {
            "strawberry": {"score": 30, "img_u": 0, "img_v": 0},
            "apple": {"score": 50, "img_u": 8, "img_v": 0},
            "banana": {"score": 20, "img_u": 0, "img_v": 8},
            "star": {"score": 0, "img_u": 8, "img_v": 8},  # 星を追加
        }

        self.init_set()

        self.add_fruit(2)
        pyxel.run(self.update, self.draw)

    def init_set(self):
        self.GAME_DURATION = GAME_DURATION
        self.player_x = 80
        self.player_y = 60
        self.fruits = []
        self.score = 0
        self.game_over = False
        self.start_time = pyxel.frame_count

        # BGMを再生（ループ設定）
        # 再生
        if pyxel.play_pos(0) is None:
            for ch, sound in enumerate(self.music):
                pyxel.sound(ch).set(*sound)
                pyxel.play(ch, ch, loop=True)

        # 最初の果物を追加
        self.add_fruit(2)

    def add_fruit(self, num=1):
        import random

        for _ in range(num):
            # フルーツの種類をランダムに選択（星は出現確率を低くする）
            fruit_type = random.choices(
                list(self.FRUIT_TYPES.keys()),
                weights=[30, 30, 30, 10],  # apple, strawberry, banana, starの出現確率
                k=1,
            )[0]

            # フルーツの種類によって速度を変える
            if fruit_type == "apple":
                speed = random.uniform(2, 4)  # りんごは速め
            elif fruit_type == "banana":
                speed = random.uniform(1, 2)  # バナナは遅め
            elif fruit_type == "star":
                speed = random.uniform(3, 5)  # 星は最も速い
            else:  # strawberry
                speed = random.uniform(1.5, 3)  # いちごは中間

            self.fruits.append(
                {
                    "x": random.randint(0, 160),
                    "y": 0,
                    "speed": speed,
                    "type": fruit_type,
                }
            )

    def update(self):
        # ゲームオーバー時は更新しない
        if self.game_over:
            pyxel.stop(1)  # BGMを停止
            # マウスクリックの座標がRETRYボタンの範囲内かチェック
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                retry_x = 80 - 28  # RETRYボタンのx座標
                retry_y = 60 + 12  # RETRYボタンのy座標
                if (
                    retry_x <= pyxel.mouse_x <= retry_x + 40
                    and retry_y <= pyxel.mouse_y <= retry_y + 10
                ):
                    self.init_set()  # ゲームをリセット
            return

        # 残り時間の計算
        elapsed = pyxel.frame_count - self.start_time
        if elapsed >= self.GAME_DURATION:
            self.game_over = True
            return

        # タッチ判定
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            touch_x = pyxel.mouse_x
            touch_y = pyxel.mouse_y

            # 各フルーツとのタッチ判定
            for fruit in self.fruits[:]:
                if self.check_collision(fruit, touch_x, touch_y):
                    if fruit["type"] == "star":
                        self.GAME_DURATION += 30 * 5  # 5秒追加
                        pyxel.play(0, 4)
                    else:
                        self.score += self.FRUIT_TYPES[fruit["type"]]["score"]
                        pyxel.play(0, 3)

                    self.fruits.remove(fruit)
                    self.add_fruit()

        # フルーツの更新
        for fruit in self.fruits[:]:
            fruit["y"] += fruit["speed"]
            if fruit["y"] > 120:  # 画面外に出たら消える
                self.fruits.remove(fruit)
                self.add_fruit()

    def check_collision(self, fruit, touch_x, touch_y):
        # タッチ位置とフルーツの距離を計算
        dx = fruit["x"] - touch_x
        dy = fruit["y"] - touch_y
        return (dx * dx + dy * dy) < 90  # 8 * 8 (フルーツのサイズに応じて調整)

    def draw(self):
        pyxel.cls(0)
        pyxel.circb(pyxel.mouse_x + 5, pyxel.mouse_y + 5, 5, 11)

        # フルーツの描画
        for fruit in self.fruits:
            fruit_data = self.FRUIT_TYPES[fruit["type"]]
            pyxel.blt(
                fruit["x"] - 4,  # 中心座標に調整
                fruit["y"] - 4,
                0,  # イメージバンク0
                fruit_data["img_u"],
                fruit_data["img_v"],
                8,  # 幅
                8,  # 高さ
                0,  # 透明色（黒）
                scale=3,
            )

        # 残り時間の表示（左上）
        elapsed = pyxel.frame_count - self.start_time
        remaining = max(0, (self.GAME_DURATION - elapsed) // 30)  # 秒単位に変換
        pyxel.text(4, 4, f"TIME:{remaining}", 7)

        # スコアの表示（右上）
        score_text = str(self.score)
        x = 160 - len(score_text) * 4 - 4
        pyxel.text(x, 4, score_text, 7)

        # ゲームオーバー画面
        if self.game_over:
            center_x = 80 - 20  # 画面中央
            center_y = 60 - 8
            pyxel.text(center_x, center_y, "GAME OVER", 8)
            pyxel.text(center_x - 8, center_y + 10, "SCORE:" + str(self.score), 7)
            pyxel.text(center_x - 8, center_y + 20, "RETRY", 7)


App()
