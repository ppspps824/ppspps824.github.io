import json

import pyxel


class App:
    def __init__(self):

        pyxel.init(160, 120, title="Fruits Catch")
        pyxel.load("assets/my_resource.pyxres")  # リソースファイルの読み込み

        with open(f"assets/music.json", "rt", encoding="utf-8") as fin:
            self.music = json.loads(fin.read())

        # BGMを再生（ループ設定）
        # 再生
        if pyxel.play_pos(0) is None:
            for ch, sound in enumerate(self.music):
                pyxel.sound(ch).set(*sound)
                pyxel.play(ch, ch, loop=True)

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

        self.GAME_DURATION = 30 * 20
        self.add_fruit(2)
        pyxel.run(self.update, self.draw)

    def init_set(self):
        self.player_x = 80
        self.player_y = 60
        self.fruits = []
        self.score = 0
        self.game_over = False
        self.start_time = pyxel.frame_count
        # BGMを再生
        pyxel.play(0, 1, loop=True)

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

            self.fruits.append(
                {
                    "x": random.randint(0, 160),
                    "y": 0,
                    "speed": random.uniform(1, 3),
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

        # キーボード入力
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, 160)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.player_y = max(self.player_y - 2, 0)
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.player_y = min(self.player_y + 2, 120)

        # マウス/タッチ入力
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            target_x = pyxel.mouse_x
            target_y = pyxel.mouse_y

            # 現在位置と目標位置の差分を計算
            dx = target_x - self.player_x
            dy = target_y - self.player_y

            # 移動速度を2に制限
            if abs(dx) > 2:
                dx = 2 if dx > 0 else -2
            if abs(dy) > 2:
                dy = 2 if dy > 0 else -2

            # 移動を適用
            self.player_x = max(0, min(160, self.player_x + dx))
            self.player_y = max(0, min(120, self.player_y + dy))

        # 果物の更新と当たり判定
        for fruit in self.fruits[:]:
            fruit["y"] += fruit["speed"]

            if self.check_collision(fruit):
                if fruit["type"] == "star":
                    self.GAME_DURATION += 30 * 5  # 5秒追加
                    pyxel.play(0, 4)  # 星用の効果音
                else:
                    self.score += self.FRUIT_TYPES[fruit["type"]]["score"]
                    pyxel.play(0, 3)  # 通常の効果音

                self.fruits.remove(fruit)
                self.add_fruit()
            elif fruit["y"] > 120:
                self.fruits.remove(fruit)
                self.add_fruit()

    def check_collision(self, fruit):
        # プレイヤーと果物の距離を計算
        distance = (
            (self.player_x - fruit["x"]) ** 2 + (self.player_y - fruit["y"]) ** 2
        ) ** 0.5
        # プレイヤーの半径(8)と果物の半径(4)の和より距離が小さければ衝突
        return distance < 12

    def draw(self):
        pyxel.cls(0)

        # プレイヤーの描画
        pyxel.circ(self.player_x, self.player_y, 8, 7)

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
