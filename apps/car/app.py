import json
import random

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Car")
        self.cars = []
        pyxel.load("assets/cars.pyxres")

        # 車ごとの画像の左上(x1,y1)と右下(x2,y2)の座標を定義
        self.CAR_SPECS = [
            {"x1": 0, "y1": 0, "x2": 72, "y2": 40},  # 車1
            {"x1": 96, "y1": 0, "x2": 152, "y2": 40},  # 車2
            {"x1": 176, "y1": 0, "x2": 248, "y2": 40},  # 車3
            {"x1": 0, "y1": 56, "x2": 72, "y2": 104},  # 車4
            {"x1": 88, "y1": 56, "x2": 160, "y2": 112},  # 車5
            {"x1": 176, "y1": 64, "x2": 248, "y2": 104},  # 車6
            {"x1": 0, "y1": 120, "x2": 64, "y2": 152},  # 車7
            {"x1": 88, "y1": 120, "x2": 160, "y2": 160},  # 車8
            {"x1": 176, "y1": 120, "x2": 240, "y2": 168},  # 車9
        ]
        pyxel.run(self.update, self.draw)

    def reset_car(self):
        direction = random.choice(["left", "right", "top", "bottom"])
        car_index = random.randint(0, 8)
        car = {
            "direction": direction,
            "image": car_index,
            "spec": self.CAR_SPECS[car_index],
        }

        # 車の幅と高さを計算
        width = car["spec"]["x2"] - car["spec"]["x1"]
        height = car["spec"]["y2"] - car["spec"]["y1"]

        base_speed = random.uniform(1.0, 3.0)

        if direction == "left":
            car["x"] = 0
            car["y"] = random.randint(0, 120 - height)
            car["speed_x"] = base_speed
            car["speed_y"] = 0
        elif direction == "right":
            car["x"] = 160
            car["y"] = random.randint(0, 120 - height)
            car["speed_x"] = -base_speed
            car["speed_y"] = 0
        elif direction == "top":
            car["x"] = random.randint(0, 160 - width)
            car["y"] = 0
            car["speed_x"] = 0
            car["speed_y"] = base_speed
        else:  # bottom
            car["x"] = random.randint(0, 160 - width)
            car["y"] = 120
            car["speed_x"] = 0
            car["speed_y"] = -base_speed

        return car

    def update(self):
        if (
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            or pyxel.btnp(pyxel.KEY_RETURN)
            or pyxel.btnp(pyxel.KEY_KP_ENTER)
        ):
            self.cars.append(self.reset_car())
            pyxel.play(0, 0)

        for car in self.cars[:]:
            car["x"] += car["speed_x"]
            car["y"] += car["speed_y"]

            if car["x"] < -16 or car["x"] > 160 or car["y"] < -16 or car["y"] > 120:
                self.cars.remove(car)

    def draw(self):
        pyxel.cls(0)
        for car in self.cars:
            spec = car["spec"]
            width = spec["x2"] - spec["x1"]
            height = spec["y2"] - spec["y1"]

            if car["direction"] == "left":
                pyxel.blt(
                    car["x"],
                    car["y"],
                    0,
                    spec["x1"],
                    spec["y1"],
                    -width,
                    height,
                    0,
                    scale=0.5,
                )
            elif car["direction"] == "right":
                pyxel.blt(
                    car["x"],
                    car["y"],
                    0,
                    spec["x1"],
                    spec["y1"],
                    width,
                    height,
                    0,
                    scale=0.5,
                )
            elif car["direction"] == "top":
                pyxel.blt(
                    car["x"],
                    car["y"],
                    0,
                    spec["x1"],
                    spec["y1"],
                    width,
                    height,
                    0,
                    rotate=90,
                    scale=0.5,
                )
            else:  # bottom
                pyxel.blt(
                    car["x"],
                    car["y"],
                    0,
                    spec["x1"],
                    spec["y1"],
                    width,
                    height,
                    0,
                    rotate=270,
                    scale=0.5,
                )


App()
