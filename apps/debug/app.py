import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Input Debug")
        self.last_inputs = []  # 最後に押されたボタンのリストを保持
        self.max_display = 10  # 画面に表示する最大入力履歴数

        pyxel.run(self.update, self.draw)

    def update(self):
        # キーボード入力のチェック
        for key_name in dir(pyxel):
            if key_name.startswith("KEY_"):
                key_value = getattr(pyxel, key_name)
                if pyxel.btnp(key_value):
                    self.add_input(f"KEY: {key_name}")

        # マウス入力のチェック
        for button_name in dir(pyxel):
            if button_name.startswith("MOUSE_BUTTON_"):
                button_value = getattr(pyxel, button_name)
                if pyxel.btnp(button_value):
                    self.add_input(f"MOUSE: {button_name}")

        # ゲームパッド入力のチェック
        for pad_name in dir(pyxel):
            if pad_name.startswith("GAMEPAD1_BUTTON_"):
                pad_value = getattr(pyxel, pad_name)
                if pyxel.btnp(pad_value):
                    self.add_input(f"GAMEPAD: {pad_name}")

    def add_input(self, input_text):
        self.last_inputs.insert(0, input_text)  # リストの先頭に追加
        if len(self.last_inputs) > self.max_display:
            self.last_inputs.pop()  # 古い入力を削除

    def draw(self):
        pyxel.cls(7)

        # 入力履歴を表示
        pyxel.text(5, 5, "Input History:", 0)
        for i, input_text in enumerate(self.last_inputs):
            pyxel.text(5, 15 + i * 10, input_text, 0)

        # 操作説明
        pyxel.text(5, 110, "Press any key/button to test", 0)


App()
