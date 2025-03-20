# Script tạo file ./assets/custom_menu_match
import pickle
import zlib
import copy
import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Định nghĩa các hằng số
WHITE = (255, 255, 255)

# Định nghĩa các lớp cần thiết
class Button:
    def __init__(self, section, x, y, w, h, string, alignLeft, font, textColor, color, colorOver, colorPressed, f, argument):
        self.section = section
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.string = string
        self.alignLeft = alignLeft
        self.font = font
        self.textColor = textColor
        self.color = color
        self.colorOver = colorOver
        self.colorPressed = colorPressed
        self.f = f
        self.argument = argument
        self.visible = True
        self.label = self.font.render(self.string, True, self.textColor) if font else None
        self.label_rect = self.label.get_rect(center=(x + w / 2, y + h / 2)) if self.label else None
        if self.alignLeft and self.label_rect:
            self.label_rect.left = self.x + 5
        self.wasPressed = False
        self.isPressed = False
        self.isOver = False

class Player:
    def __init__(self, nick, team, keys, isbot):
        self.nick = nick
        self.team = team
        self.kicking = False
        self.isbot = isbot
        self.avatar = "./assets/images/player_red.png" if team == "RED" else "./assets/images/player_blue.png"
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.r = 26
        self.mass = 25
        self.kcd = 0
        # Đảm bảo keys có 7 phần tử (Up, Down, Left, Right, Kick, Ability, Shoot)
        self.keyUp, self.keyDown, self.keyLeft, self.keyRight, self.keyKick, self.keyAbility, self.keyShoot = keys if len(keys) == 7 else keys + (0, 0)
        self.dashCooldown = 0
        self.shootCooldown = 0
        self.isDashing = False
        self.isShooting = False
        self.isShootDelay = False
        self.dashTimer = 0
        self.shootTimer = 0
        self.shootDelayTimer = 0
        self.dashSpeed = 20
        self.shootForce = 10
        self.lastDirection = None
        self.normalMass = 25
        self.mass = self.normalMass
        self.shootTargetBall = None
        # Isagi's Skills
        self.isFlowState = False
        self.flowStateTimer = 0
        self.flowStateSpeedBoost = 1.5
        self.flowStateKickBoost = 1.5
        self.isDirectShot = False
        # Bachira's Skills
        self.isSambaDance = False
        self.sambaDanceTimer = 0
        self.sambaDanceSpeed = 15
        self.sambaDanceBall = None
        self.sambaZigzagPhase = 0
        self.isFreeNutmeg = False
        self.nutmegTimer = 0
        self.nutmegTargetPlayer = None
        self.nutmegTargetBall = None
        self.nutmegFreezeTimer = 0  # Thuộc tính cần thiết
        self.hasKicked = False
        # Thời gian hồi chiêu
        self.skillCooldowns = {
            "dash": {"max": 600, "current": 0},
            "magnet": {"max": 1680, "current": 0},
            "flow": {"max": 960, "current": 0},
            "direct": {"max": 1440, "current": 0},
            "samba": {"max": 1080, "current": 0},
            "nutmeg": {"max": 1680, "current": 0}
        }

class Ball:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.mass = 15
        self.color = color

class Post:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Wall:
    def __init__(self, a, b, c):
        self.A = a
        self.B = b
        self.C = c

class Line:
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xm = (x1 + x2) / 2
        self.ym = (y1 + y2) / 2
        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2
        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2)**0.5
        self.color = color
        self.width = width
        self.visible = visible

class VisualLine:
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.width = width
        self.visible = visible

class Goal:
    def __init__(self, team, x1, y1, x2, y2):
        self.team = team
        self.score = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xm = (x1 + x2) / 2
        self.ym = (y1 + y2) / 2
        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2
        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2)**0.5

class Arc:
    def __init__(self, x, y, r, a0, a, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a
        self.color = color
        self.width = width
        self.visible = visible
        self.point1 = Point(x + r * pygame.math.Vector2(1, 0).rotate(-a0 * 180 / 3.14159).x, y + r * pygame.math.Vector2(1, 0).rotate(-a0 * 180 / 3.14159).y)
        self.point2 = Point(x + r * pygame.math.Vector2(1, 0).rotate(-a * 180 / 3.14159).x, y + r * pygame.math.Vector2(1, 0).rotate(-a * 180 / 3.14159).y)

class KickoffPoint:
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team

class KickoffLine:
    def __init__(self, x1, y1, x2, y2, team, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.xm = (x1 + x2) / 2
        self.ym = (y1 + y2) / 2
        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2
        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2)**0.5
        self.team = team
        self.color = color
        self.width = width
        self.visible = visible

class KickoffArc:
    def __init__(self, x, y, r, a0, a, team, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a
        self.team = team
        self.color = color
        self.width = width
        self.visible = visible
        self.point1 = KickoffPoint(x + r * pygame.math.Vector2(1, 0).rotate(-a0 * 180 / 3.14159).x, y + r * pygame.math.Vector2(1, 0).rotate(-a0 * 180 / 3.14159).y, team)
        self.point2 = KickoffPoint(x + r * pygame.math.Vector2(1, 0).rotate(-a * 180 / 3.14159).x, y + r * pygame.math.Vector2(1, 0).rotate(-a * 180 / 3.14159).y, team)

# Mock module classes để pickle nhận diện đúng tên module
class MockClassesModule:
    Button = Button
    Player = Player
    Ball = Ball
    Post = Post
    Point = Point
    Wall = Wall
    Line = Line
    VisualLine = VisualLine
    Goal = Goal
    Arc = Arc
    KickoffPoint = KickoffPoint
    KickoffLine = KickoffLine
    KickoffArc = KickoffArc

# Gán module giả lập vào sys.modules
sys.modules['classes'] = MockClassesModule()

# Đọc và giải nén menu_match
def load_menu_match(path="./assets/menu_match"):
    try:
        with open(path, "rb") as file:
            compressed_data = pickle.load(file)
            decompressed_data = zlib.decompress(compressed_data)
            menu_match_data = pickle.loads(decompressed_data)
            return menu_match_data
    except Exception as e:
        print(f"Lỗi khi tải menu_match: {e}")
        return None

# Thay đổi tên trong danh sách players
def customize_names(menu_match_data, new_name_red="PlayerRed", new_name_blue="PlayerBlue"):
    modified_data = copy.deepcopy(menu_match_data)
    for frame in modified_data:
        for player in frame['players']:
            if player.nick == "Chlyb":
                player.nick = new_name_red
            elif player.nick == "kompetero":
                player.nick = new_name_blue
    return modified_data

# Lưu dữ liệu đã chỉnh sửa thành file mới
def save_custom_menu_match(data, output_path="./assets/custom_menu_match"):
    compressed_data = zlib.compress(pickle.dumps(data, -1))
    with open(output_path, "wb") as file:
        pickle.dump(compressed_data, file)
    print(f"Đã lưu menu_match tùy chỉnh vào {output_path}")

# Chạy thử
original_data = load_menu_match()
if original_data:
    print("Trước khi chỉnh sửa:")
    for player in original_data[0]['players']:
        print(f"Player: {player.nick}, Team: {player.team}")

    custom_data = customize_names(original_data, new_name_red="Football", new_name_blue="Legends")

    print("\nSau khi chỉnh sửa:")
    for player in custom_data[0]['players']:
        print(f"Player: {player.nick}, Team: {player.team}")

    save_custom_menu_match(custom_data)