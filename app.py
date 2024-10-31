import pyxel


class App:
    def __init__(self):

        pyxel.init(160, 120, title="Fruits Catch")
        # pyxel.mouse(True)

        # 音声データの作成
        pyxel.sound(0).set(  # 果物ゲット時の効果音
            "e3a3", "t", "7", "s", 30  # note  # tone  # volume  # effect  # speed
        )

        pyxel.sound(1).set(  # BGM
            "c3e3g3c4g3c4g3e3",  # note
            "t",  # tone
            "4",  # volume
            "n",  # effect
            20,  # speed
        )

        # BGMを再生（ループ設定）
        pyxel.play(0, 1, loop=True)

        self.init_set()

        self.GAME_DURATION = 30 * 10

        # 色ごとの点数を辞書で定義
        self.color_scores = {
            1: 10,  # 紺色
            2: 20,  # 紫
            3: 30,  # 緑
            4: 40,  # 茶色
            5: 50,  # 濃い青
            6: 60,  # 水色
            7: 70,  # 白
            8: 80,  # 赤
            9: 90,  # オレンジ
            10: 100,  # 黄色
            11: 110,  # 緑
            12: 120,  # 青
            13: 130,  # グレー
            14: 140,  # ピンク
            15: 150,  # ベージュ
        }
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
            self.fruits.append(
                {
                    "x": random.randint(0, 160),
                    "y": 0,
                    "speed": random.uniform(1, 3),
                    "color": random.randint(
                        1, 15
                    ),  # 色を0-15からランダムに選択（0は黒なので除外）
                }
            )

    def update(self):
        # ゲームオーバー時は更新しない
        if self.game_over:
            pyxel.stop(0)  # BGMを停止
            # if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            #     self.init_set()
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

            # プレイヤーと果物の当たり判定
            if self.check_collision(fruit):
                self.score += self.color_scores[fruit["color"]]  # 色に応じた点数を加算
                pyxel.play(1, 0)  # 効果音を再生（チャンネル1、サウンド0）
                self.fruits.remove(fruit)
                self.add_fruit()
            # 画面外に出た場合
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
        # プレイヤーと果物の描画（既存のコード）
        pyxel.circ(self.player_x, self.player_y, 8, 7)
        for fruit in self.fruits:
            pyxel.circ(fruit["x"], fruit["y"], 4, fruit["color"])

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


App()
