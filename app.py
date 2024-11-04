import json
import random

import pyxel

time_limit = 60 * 30


class App:
    def __init__(self):
        self.WIDTH = 160
        self.HEIGHT = 120
        self.CELL_SIZE = 8
        self.COLS = self.WIDTH // self.CELL_SIZE
        self.ROWS = self.HEIGHT // self.CELL_SIZE

        pyxel.init(self.WIDTH, self.HEIGHT, title="Maze Game")
        self.game_state = "playing"  # "playing" または "gameover"
        self.time_limit = time_limit
        self.cleared_count = 0

        with open(f"assets/music.json", "rt", encoding="utf-8") as fin:
            self.music = json.loads(fin.read())

        pyxel.sound(3).set(  #
            "e3a3", "t", "7", "s", 30  # note  # tone  # volume  # effect  # speed
        )
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # 迷路の生成
        self.maze = self.generate_maze()

        # プレイヤーの初期位置（スコア表示エリアの直下に変更）
        self.player_x = 8  # スコア表示エリアの幅
        self.player_y = 4  # スコア表示エリアの高さ

        # ゴールの位置を設定
        self.goal_x = self.COLS - 2
        self.goal_y = self.ROWS - 2
        # ゴール地点を通路にする
        self.maze[self.goal_y][self.goal_x] = 0

        if pyxel.play_pos(0) is None:
            for ch, sound in enumerate(self.music):
                pyxel.sound(ch).set(*sound)
                pyxel.play(ch, ch, loop=True)

    def generate_maze(self):
        # 迷路の初期化（壁で埋める）
        maze = [[1 for x in range(self.COLS)] for y in range(self.ROWS)]

        # スコア表示エリアを空白にする（左上の領域）
        score_area_width = 8  # 64ピクセル分（8セル）
        score_area_height = 4  # 32ピクセル分（4セル）
        for y in range(score_area_height):
            for x in range(score_area_width):
                maze[y][x] = 1  # この領域は壁として確保

        def carve_path(x, y):
            maze[y][x] = 0
            directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < self.COLS
                    and 0 <= new_y < self.ROWS
                    and maze[new_y][new_x] == 1
                    # スコア表示エリアを避ける
                    and not (new_y < score_area_height and new_x < score_area_width)
                ):
                    maze[y + dy // 2][x + dx // 2] = 0
                    carve_path(new_x, new_y)

        # 迷路の生成開始（スコア表示エリアを避けた位置から）
        start_x = score_area_width
        start_y = score_area_height
        carve_path(start_x, start_y)

        # プレイヤーの初期位置を通路にする
        maze[start_y][start_x] = 0
        return maze

    def update(self):
        if self.game_state == "playing":
            self.time_limit -= 1
            if self.time_limit <= 0:
                self.game_state = "gameover"
                return

            # プレイヤーの移動（押し続けに対応）
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                if (
                    self.player_y > 0
                    and self.maze[self.player_y - 1][self.player_x] == 0
                ):
                    self.player_y -= 1
            if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                if (
                    self.player_y < self.ROWS - 1
                    and self.maze[self.player_y + 1][self.player_x] == 0
                ):
                    self.player_y += 1
            if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                if (
                    self.player_x > 0
                    and self.maze[self.player_y][self.player_x - 1] == 0
                ):
                    self.player_x -= 1
            if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                if (
                    self.player_x < self.COLS - 1
                    and self.maze[self.player_y][self.player_x + 1] == 0
                ):
                    self.player_x += 1

            # ゴールに到達したかチェック
            if self.player_x == self.goal_x and self.player_y == self.goal_y:
                pyxel.play(3, 3)  # 効果音を再生
                self.cleared_count += 1
                self.reset_game()
        else:
            # ゲームオーバー時にエンターキーでリスタート
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                self.game_state = "playing"
                self.time_limit = time_limit
                self.cleared_count = 0
                self.reset_game()

    def draw(self):
        pyxel.cls(0)

        # 迷路の描画
        for y in range(self.ROWS):
            for x in range(self.COLS):
                if self.maze[y][x] == 1:
                    pyxel.rect(
                        x * self.CELL_SIZE,
                        y * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE,
                        7,
                    )

        # ゴールの描画（緑色）
        pyxel.rect(
            self.goal_x * self.CELL_SIZE,
            self.goal_y * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE,
            11,
        )

        # プレイヤーの描画
        pyxel.rect(
            self.player_x * self.CELL_SIZE,
            self.player_y * self.CELL_SIZE,
            self.CELL_SIZE,
            self.CELL_SIZE,
            8,
        )

        # 残り時間とクリア数の表示（背景付き）
        remaining_seconds = self.time_limit // 30
        # 時間表示の背景
        pyxel.rect(2, 2, 50, 22, 1)
        pyxel.text(4, 4, f"TIME: {remaining_seconds:2d}", 7)
        pyxel.text(4, 12, f"CLEARED: {self.cleared_count}", 7)

        # ゲームオーバー画面
        if self.game_state == "gameover":
            pyxel.stop(1)  # BGMを停止
            # 半透明の黒背景（画面全体を暗く）
            for y in range(self.HEIGHT):
                for x in range(self.WIDTH):
                    if (x + y) % 2 == 0:  # ディザリングパターン
                        pyxel.pset(x, y, 0)

            # 結果表示の背景
            pyxel.rect(30, 45, 100, 35, 1)
            pyxel.text(60, 50, "GAME OVER", 8)
            pyxel.text(40, 60, f"Cleared Maps: {self.cleared_count}", 7)
            pyxel.text(35, 70, "Press ENTER to restart", 7)


App()
