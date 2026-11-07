from pico2d import *

class Slime:
    FW, FH, COUNT, FPS = 64, 64, 4, 8        # slime_sheet.json 값
    def __init__(self, sheet, x, y, speed=60):
        self.img = load_image(sheet)
        self.x, self.y, self.speed, self.t = x, y, speed, 0.0
    def update(self, dt, tx, ty):
        self.t += dt
        dx, dy = tx - self.x, ty - self.y
        d = (dx*dx + dy*dy) ** 0.5 or 1
        self.x += dx / d * self.speed * dt
        self.y += dy / d * self.speed * dt
        self.face = 1 if dx >= 0 else -1
    def draw(self):
        f = int(self.t * self.FPS) % self.COUNT
        if self.face > 0:
            self.img.clip_draw(f*self.FW, 0, self.FW, self.FH, self.x, self.y)
        else:  # 왼쪽 이동 시 좌우 반전
            self.img.clip_composite_draw(f*self.FW, 0, self.FW, self.FH, 0, 'h', self.x, self.y, self.FW, self.FH)

open_canvas(800, 600)
green = Slime('slime_green.png', 100, 100, 60)
red = Slime('slime_red.png', 700, 500, 90)   # 밤/스테이지 변형 예시
tx, ty = 400, 300
prev = get_time()
running = True
while running:
    now = get_time(); dt = now - prev; prev = now
    for e in get_events():
        if e.type == SDL_QUIT: running = False
        elif e.type == SDL_MOUSEMOTION: tx, ty = e.x, 600 - 1 - e.y   # 마우스를 플레이어처럼 추적
    green.update(dt, tx, ty); red.update(dt, tx, ty)
    clear_canvas(); green.draw(); red.draw(); update_canvas()
    delay(0.01)
close_canvas()
