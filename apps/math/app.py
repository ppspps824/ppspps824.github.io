import json
import random

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Math Game")
        self.selected_choice = 0
        self.score = 0  # スコアを追加
        self.time_left = 30 * 30  # 30秒 * 30フレーム
        self.game_over = False  # ゲームオーバー状態

        with open(f"assets/music.json", "rt", encoding="utf-8") as fin:
            self.music = json.loads(fin.read())

        self.reset_problem()
        pyxel.run(self.update, self.draw)

    def reset_problem(self):
        # 新しい問題を生成
        self.num1 = random.randint(1, 9)
        self.num2 = random.randint(1, 9)
        self.correct_answer = self.num1 + self.num2

        # 選択肢を生成（正解を含む4つの数字）
        self.choices = [self.correct_answer]
        while len(self.choices) < 4:
            wrong_answer = random.randint(2, 18)
            if wrong_answer not in self.choices:
                self.choices.append(wrong_answer)
        random.shuffle(self.choices)

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.__init__()
            return

        # 時間を減らす
        self.time_left -= 1
        if self.time_left <= 0:
            self.game_over = True
            return

        # 選択肢の移動（上下キーまたはゲームパッド）
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            self.selected_choice = (self.selected_choice - 1) % 4
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            self.selected_choice = (self.selected_choice + 1) % 4

        # 決定（エンターキーまたはゲームパッドのAボタン）
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            if self.choices[self.selected_choice] == self.correct_answer:
                self.score += 100  # 正解でスコア加算
                self.reset_problem()
                self.selected_choice = 0

    def draw(self):
        pyxel.cls(7)

        # スコアと残り時間の表示
        pyxel.text(10, 10, f"SCORE: {self.score}", 0)
        pyxel.text(100, 10, f"TIME: {self.time_left // 30}", 0)

        if self.game_over:
            # ゲームオーバー画面
            pyxel.text(45, 50, f"GAME OVER! Score: {self.score}", 0)
            pyxel.text(35, 70, "Press SPACE to restart", 0)
            return

        # 問題文の表示
        question = f"{self.num1} + {self.num2} = ?"
        pyxel.text(60, 30, question, 0)

        # 選択肢の表示（選択中の項目は色を変える）
        for i, choice in enumerate(self.choices):
            color = 8 if i == self.selected_choice else 0
            pyxel.text(60, 50 + i * 10, f"{i+1}: {choice}", color)

        # 操作説明
        pyxel.text(20, 100, "UP/DOWN: Select  ENTER: Answer", 0)


App()
