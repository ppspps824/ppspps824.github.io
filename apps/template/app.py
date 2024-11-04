import json

import pyxel


class App:
    def __init__(self):

        pyxel.init(160, 120, title="Fruits Catch")
        pyxel.load("assets/my_resource.pyxres")  # リソースファイルの読み込み

        with open(f"assets/music.json", "rt", encoding="utf-8") as fin:
            self.music = json.loads(fin.read())

        self.init_set()
        pyxel.run(self.update, self.draw)

    def init_set(self):
        # BGMを再生（ループ設定）
        # 再生
        if pyxel.play_pos(0) is None:
            for ch, sound in enumerate(self.music):
                pyxel.sound(ch).set(*sound)
                pyxel.play(ch, ch, loop=True)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)


App()
