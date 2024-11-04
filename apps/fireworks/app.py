import json
import random

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Fireworks")

        # 効果音の定義
        pyxel.sound(1).set(  # 打ち上げ音
            "a3a2a1", "n", "4", "s", 10  # note  # tone  # volume  # effect  # speed
        )

        pyxel.sound(0).set(  # 爆発音
            "c3", "p", "7", "s", 5  # note  # tone  # volume  # effect  # speed
        )

        self.colors = [7, 8, 9, 10, 11, 12, 14]  # 使用する色のリスト
        self.fireworks = []
        pyxel.run(self.update, self.draw)

    def create_normal_particles(self, fw):
        # 通常の360度パーティクル
        for _ in range(45):
            angle = random.uniform(0, 30)
            speed = random.uniform(0.5, 2)
            fw["particles"].append(
                {
                    "x": 0,
                    "y": 0,
                    "dx": speed * pyxel.cos(angle * 30),
                    "dy": speed * pyxel.sin(angle * 30),
                    "life": 30,
                }
            )

    def update(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.fireworks.append(
                {
                    "x": random.randint(10, 150),
                    "y": 120,
                    "target_y": random.randint(20, 60),
                    "speed": 4,
                    "particles": [],
                    "color": random.choice(self.colors),
                    "state": "rising",
                }
            )
            pyxel.play(0, 0)

        for fw in self.fireworks[:]:
            if fw["state"] == "rising":
                fw["y"] -= fw["speed"]
                if fw["y"] <= fw["target_y"]:
                    fw["state"] = "exploding"
                    pyxel.play(1, 1)
                    self.create_normal_particles(fw)

            elif fw["state"] == "exploding":
                # 爆発中のパーティクル更新
                all_dead = True
                for p in fw["particles"]:
                    if p["life"] > 0:
                        all_dead = False
                        p["x"] += p["dx"]
                        p["y"] += p["dy"]
                        p["dy"] += 0.1  # 重力の影響
                        p["life"] -= 1

                if all_dead:
                    self.fireworks.remove(fw)

    def draw(self):
        pyxel.cls(0)

        for fw in self.fireworks:
            if fw["state"] == "rising":
                pyxel.pset(fw["x"], fw["y"], fw["color"])
            else:
                # パーティクルの描画
                for p in fw["particles"]:
                    if p["life"] > 0:
                        x = fw["x"] + p["x"]
                        y = fw["y"] + p["y"]
                        col = fw["color"] if p["life"] > 15 else max(1, fw["color"] - 2)
                        pyxel.pset(x, y, col)


App()
