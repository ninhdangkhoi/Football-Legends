import pygame
import physicsEngine
import math
import time
import menu
import gameHandler
import random
#from render import skill_images, avatar_to_name
#MENU CLASSES

class Button(object):
    def __init__(self, section, x, y, w, h, string, alignLeft, font, textColor, color, colorOver, colorPressed, f,argument):
        self.section = section

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.string = string
        self.alignLeft = alignLeft
        self.font = font
        self.textColor = textColor
        self.visible = True
        self.label = self.font.render(self.string, True, self.textColor)
        self.label_rect = self.label.get_rect(center=(x + w / 2, y + h / 2))
        if self.alignLeft:
            self.label_rect.left = self.x + 5

        self.color = color
        self.colorPressed = colorPressed
        self.colorOver = colorOver

        self.wasPressed = False
        self.isPressed = False
        self.isOver = False

        self.f = f
        self.argument = argument
        menu.buttonList.append(self)

    def update(self):
        self.label = self.font.render(self.string, True, self.textColor)
        self.label_rect = self.label.get_rect(center=(self.x + self.w / 2, self.y + self.h / 2))
        if self.alignLeft:
            self.label_rect.left = self.x + 5

class PlayerBar(object):
    def __init__(self, player):
        self.player = player
    
        if player.team == "RED":
            self.pos = gameHandler.redPlayersCount
        elif player.team == "BLUE":
            self.pos = gameHandler.bluePlayersCount
        else:
            self.pos = gameHandler.spectatorsCount

        self.isOver = False
        self.colorOver = (27, 35, 40)
        self.color = (17,22,25)

        self.x = 0
        self.y = 0
        self.w = 220
        self.h = 25

        self.updateCoordinates()

        self.updateName()
        
        menu.playerBarList.append(self)

    def updateName(self):
        self.label = menu.lightFont.render( self.player.nick, True, (255,255,255))
        self.label_rect = self.label.get_rect( center=( self.x + self.w/2, self.y + self.h/2))
        self.label_rect.left = self.x + 5

    def updateCoordinates(self):
        if self.player.team == "RED":
            self.x = menu.redTeamBox.x
        elif self.player.team == "BLUE":
            self.x = menu.blueTeamBox.x
        else:
            self.x = menu.spectatorTeamBox.x
        self.y = menu.spectatorTeamBox.y + (self.pos - 1) * self.h

    def openOptions(self):
        menu.gameSection = 4
        menu.selectedPlayerBar = self
        menu.nickBox.string = self.player.nick
        menu.nickBox.update()

class DropdownItem(object):
    def __init__(self, x, y, w, h, string, font, color, colorOver, f, argument):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.string = string
        self.font = font

        self.label = self.font.render( self.string, True, (255,255,255))
        self.label_rect = self.label.get_rect( center=( x + w/2, y + h/2))
        self.label_rect.left = self.x + 5
        
        self.color = color
        self.colorOver = colorOver

        self.wasPressed = False
        self.isPressed = False
        self.isOver = False

        self.f = f
        self.argument = argument
        
        menu.dropdownList.append(self)
        
#PHYSIC OBJECTS CLASSES
        
class Player(object):
    def __init__(self, nick, team, keys, isbot):
        self.nick = nick
        self.team = team
        self.kicking = False
        self.isbot = isbot
        self.avatar = menu.characterImages[0] if nick == "Player 1" else menu.characterImages[1]
        print(f"Player {self.nick} avatar set to: {self.avatar}")
        self.x = 100000
        self.y = 100000
        self.vx = 0
        self.vy = 0
        self.r = 26
        self.mass = 25
        self.kcd = 0
        self.skill_image = None
        self.skill_image_timer = 0

        self.speed = 5  # Tốc độ cơ bản
        self.shootForce = 10  # Lực sút cơ bản

        # Thêm thuộc tính cho particle
        self.particles = []  # Danh sách particle

        self.emperor_flow_cd = 0  # Cooldown Emperor Flow
        self.emperor_flow_active = False  # Trạng thái kích hoạt Emperor Flow
        self.emperor_flow_timer = 0  # Thời gian hiệu ứng Emperor Flow
        self.kaiser_impact_cd = 0  # Cooldown Kaiser Impact
        self.kaiser_impact_active = False  # Trạng thái kích hoạt Kaiser Impact
        self.kaiser_impact_timer = 0  # Thời gian hiệu ứng Kaiser Impact
        self.original_speed = self.speed  # Lưu tốc độ gốc
        self.original_shootForce = self.shootForce  # Lưu lực sút gốc
        self.debuff_speed_timer = 0  # Thời gian debuff tốc độ đối phương
        self.debuff_shoot_timer = 0  # Thời gian debuff lực sút đối phương
        # Phím điều khiển và kỹ năng
        self.keyUp, self.keyDown, self.keyLeft, self.keyRight, self.keyKick, self.keyAbility, self.keyShoot = keys
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
        # Thêm các biến cho Isagi's Skills
        self.isFlowState = False
        self.flowStateTimer = 0
        self.flowStateSpeedBoost = 1.5
        self.flowStateKickBoost = 1.5
        self.isDirectShot = False
        
        # Thêm các biến cho Bachira's Skills
        self.isSambaDance = False
        self.sambaDanceTimer = 0
        self.sambaDanceSpeed = 15
        self.sambaDanceBall = None
        self.sambaZigzagPhase = 0
        self.isFreeNutmeg = False
        self.nutmegTimer = 0
        self.nutmegTargetPlayer = None
        self.nutmegTargetBall = None
        self.nutmegFreezeTimer = 0  # Đã có sẵn cho Bachira, nhưng cần cho tất cả Player

        # Thêm các biến cho Itoshi Sae's Skills
        self.isMagicalTurn = False
        self.magicalTurnTimer = 0
        self.magicalTurnBall = None
        self.magicalTurnPhase = 0
        self.magicalTurnDirection = None  # Hướng nút bấm (up, down, left, right)
        self.isPerfectShot = False
        self.perfectShotTimer = 0
        self.perfectShotTargetBall = None

        # Thêm các biến cho Barou's Skills
        self.isDribblingLord = False
        self.dribblingLordTimer = 0
        self.dribblingLordBall = None
        self.dribblingLordPhase = 0
        self.dribblingLordDirection = None
        self.isKingShot = False
        self.kingShotTimer = 0
        self.kingShotTargetBall = None

        # Thêm thuộc tính cho Kunigami's Skills
        self.isBodyBlock = False
        self.bodyBlockTimer = 0
        self.bodyBlockTargetPlayer = None
        self.isWildShot = False
        self.wildShotTimer = 0
        self.wildShotTargetBall = None

        # Thêm thuộc tính cho Don Lorenzo's Skills
        self.isAceEater = False
        self.aceEaterTimer = 0
        self.aceEaterPhase = 0
        self.aceEaterStartX = 0
        self.aceEaterStartY = 0
        self.aceEaterTargetBall = None
        self.aceEaterTargetPlayer = None
        self.isZombieDribbling = False
        self.zombieDribblingTimer = 0
        self.zombieDribblingBall = None
        self.zombieSpeedBoost = 1.8  # +80% speed
        
        #Rin skill 1
        self.isCS = False
        self.CSTimer = 0
        self.CSball = None
        self.CSgoal = 0
        self.cx = 0
        self.cy = 0
        #Rin skill 2
        self.isOppositeDirection = False
        self.OppositeDirectionTimer = 0
        self.OppositeDirectionSpeed = 150
        self.ODx = 0
        self.ODy = 0
        self.ODimagex = []
        self.ODimagey = []
        self.AIlv= []
        self.OppositeDirectionBall = None
        self.OppositeDirectionPlayer = []

        # Thêm thuộc tính này cho tất cả người chơi để đối thủ bị ảnh hưởng
        self.nutmegFreezeTimer = 0  # Khởi tạo mặc định là 0
        self.dead = False

        # Cập nhật skillCooldowns
        self.skillCooldowns = {
            "dash": {"max": 600, "current": 0},
            "magnet": {"max": 1680, "current": 0},
            "flow": {"max": 960, "current": 0},
            "direct": {"max": 1440, "current": 0},
            "samba": {"max": 1080, "current": 0},
            "monster": {"max": 1680, "current": 0},
            "magical": {"max": 1200, "current": 0},
            "perfect": {"max": 1800, "current": 0},
            "dribbling": {"max": 1200, "current": 0}, 
            "king": {"max": 1800, "current": 0},
            "block": {"max": 1080, "current": 0},  
            "wild": {"max": 1800, "current": 0},
            "Ace": {"max": 1800, "current": 0},  
            "zombie": {"max": 2400, "current": 0},
            "Emperor": {"max": 840, "current": 0},  
            "Impact": {"max": 1800, "current": 0},
            "opposite": {"max": 1200, "current": 0},
            "curve": {"max": 1600, "current": 0}
        }

        if team == "RED":
            gameHandler.redPlayersCount += 1
        elif team == "BLUE":
            gameHandler.bluePlayersCount += 1
        else:
            gameHandler.spectatorsCount += 1
        
        self.hasKicked = False
        physicsEngine.playerList.append(self)
        PlayerBar(self)
    def applyBuff(self):
        if self.avatar == "./assets/images/Lorenzo.png":
            self.speed *= 1.35
            self.shootForce *= 1.25
            print(f"Buff applied for {self.nick}: Speed = {self.speed}, Shoot Force = {self.shootForce}")
    def steer(self, previousKeys, currentKeys, stadiumWidth):
        #print(f"{self.nick}:{self.keyShoot} ")
        #print(f"Player: {self.nick}, Avatar: {self.avatar}, Q: {currentKeys[self.keyAbility]}, V: {currentKeys[self.keyShoot]}")
        #print(f"Samba Cooldown: {self.skillCooldowns['samba']['current']}, Nutmeg Cooldown: {self.skillCooldowns['nutmeg']['current']}")
        #if currentKeys[self.keyAbility]:
            #print(f"{self.nick} - Q PRESSED")
        #if currentKeys[self.keyShoot]:
            #print(f"{self.nick} - V PRESSED")
        vertical = 0
        horizontal = 0
        
        # Cập nhật hướng cuối cùng (lastDirection) ngay cả khi đang trong Magnet
        if currentKeys[self.keyUp]:
            self.lastDirection = "up"
        if currentKeys[self.keyDown]:
            self.lastDirection = "down"
        if currentKeys[self.keyLeft]:
            self.lastDirection = "left"
        if currentKeys[self.keyRight]:
            self.lastDirection = "right"
        
        # Kích hoạt Emperor Flow
        if (self.avatar == "./assets/images/Kaiser.png" and currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and self.skillCooldowns["Emperor"]["current"] == 0 and not self.kaiser_impact_active):
            self.emperor_flow_active = True
            self.emperor_flow_timer = 720#6s (120 FPS * 6)
            self.skill_image = "kaiser_emperor"
            self.skill_image_timer = 120
            self.skillCooldowns["Emperor"]["current"] = self.skillCooldowns["Emperor"]["max"]
            self.speed = self.original_speed * 1.9  # +90% tốc độ
            self.shootForce = self.original_shootForce * 1.9  # +90% lực sút
            for player in physicsEngine.playerList:
                if player != self:
                    player.speed = player.original_speed * 0.25  # -75% tốc độ đối phương
                    player.shootForce = player.original_shootForce * 0.2  # -80% lực sút
                    player.debuff_speed_timer = 240  # 4s (60 FPS * 4)
                    player.debuff_shoot_timer = 180  # 3s (60 FPS * 3)
            for ball in physicsEngine.ballList:
                ball.slow = True

        # Kiểm tra Kaiser Impact
        ball = physicsEngine.ballList[0]
        if (self.avatar == "./assets/images/Kaiser.png" and currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and self.skillCooldowns["Impact"]["current"] == 0 and pygame.math.Vector2(self.x - ball.x, self.y - ball.y).length() < 50 and not self.emperor_flow_active):
            self.kaiser_impact_active = True
            self.kaiser_impact_timer = 30  # 0.5s (60 FPS * 0.5)
            self.skill_image = "kaiser_impact"
            self.skill_image_timer = 120
            self.skillCooldowns["Impact"]["current"] = self.skillCooldowns["Impact"]["max"]
            self.shootForce = self.original_shootForce * 2.2  # +120% lực sút khi dùng Impact
            ball.owner = self
         # Giảm cooldown
        if self.skillCooldowns["Emperor"]["current"] > 0:
            self.skillCooldowns["Emperor"]["current"] -= 1
        if self.skillCooldowns["Impact"]["current"] > 0:
            self.skillCooldowns["Impact"]["current"] -= 1
        if self.kaiser_impact_cd > 0:
            self.kaiser_impact_cd -= 1
        # Cập nhật trạng thái skill
        if self.emperor_flow_active:
            self.emperor_flow_timer -= 1
            if self.emperor_flow_timer <= 0:
                self.emperor_flow_active = False
                self.speed = self.original_speed
                self.shootForce = self.original_shootForce
                for ball in physicsEngine.ballList:
                    ball.slow = False

        if self.kaiser_impact_active:
            self.kaiser_impact_timer -= 1
            if self.kaiser_impact_timer <= 0:
                self.kaiser_impact_active = False
                self.shoot_ball(ball, currentKeys)

        # Quản lý debuff đối phương
        if self.debuff_speed_timer > 0:
            self.debuff_speed_timer -= 1
            if self.debuff_speed_timer == 0:
                self.speed = self.original_speed
        if self.debuff_shoot_timer > 0:
            self.debuff_shoot_timer -= 1
            if self.debuff_shoot_timer == 0:
                self.shootForce = self.original_shootForce
        if (self.avatar == "./assets/images/Lorenzo.png" and not (self.isDashing or self.isSambaDance or self.isFreeNutmeg or self.isDribblingLord or self.isKingShot or self.isAceEater or self.isShootDelay)):
            if (abs(self.vx) > 0.1 or abs(self.vy) > 0.1) and (random.random() < 0.25):  # 20% cơ hội mỗi frame
                # Hướng ngược với vận tốc để giống dấu chân rơi lại phía sau
                direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                particle_vx = -direction.x * random.uniform(1, 3) if not self.isZombieDribbling else direction.x
                particle_vy = -direction.y * random.uniform(1, 3) if not self.isZombieDribbling else direction.y
                # Màu tím-đen ngẫu nhiên
                color = (75, 0, 130) if random.random() < 0.6 else (0, 0, 0)
                self.particles.append(Particle(
                    x=self.x, 
                    y=self.y, 
                    vx=particle_vx, 
                    vy=particle_vy, 
                    lifetime=random.randint(30, 60),  # 0.25-0.5 giây (120 FPS)
                    color=color, 
                    size=random.uniform(3, 6)  # Kích thước nhỏ
                ))
        if (self.avatar == "./assets/images/Kaiser.png" and not (self.isDashing or self.isSambaDance or self.isFreeNutmeg or self.isDribblingLord or 
        self.isKingShot or self.isAceEater or self.isZombieDribbling or self.isShootDelay or 
        self.emperor_flow_active or self.kaiser_impact_active)):
            if (abs(self.vx) > 0.1 or abs(self.vy) > 0.1) and random.random() < 0.2:  # 20% chance mỗi frame
                direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                particle_vx = -direction.x * random.uniform(1, 3)
                particle_vy = -direction.y * random.uniform(1, 3)
                color = (0, 255, 255) if random.random() < 0.6 else (255, 255, 255)  # Cyan white
                self.particles.append(Particle(
                    x=self.x, 
                    y=self.y, 
                    vx=particle_vx, 
                    vy=particle_vy, 
                    lifetime=random.randint(30, 60),  # 0.25-0.5 seconds at 120 FPS
                    color=color, 
                    size=random.uniform(2, 4)  
                ))
        # Cập nhật và loại bỏ particle
        for particle in self.particles[:]:  # Sao chép danh sách để tránh lỗi khi xóa
            particle.x += particle.vx
            particle.y += particle.vy
            particle.lifetime -= 1
            if particle.lifetime <= 0:
                self.particles.remove(particle)
        # Chỉ áp dụng di chuyển nếu không trong trạng thái Magnet (isShootDelay)
        if not self.isShootDelay:
            if currentKeys[self.keyUp]:
                vertical -= gameHandler.playerAcceleration
            if currentKeys[self.keyDown]:
                vertical += gameHandler.playerAcceleration
            if currentKeys[self.keyLeft]:
                horizontal -= gameHandler.playerAcceleration
            if currentKeys[self.keyRight]:
                horizontal += gameHandler.playerAcceleration

        # Xử lý phím Kick
        if currentKeys[self.keyKick]:
            if self.kicking:
                self.kicking = True
            elif previousKeys[self.keyKick]:
                self.kicking = False
            else:
                self.kicking = True
        else:
            self.kicking = False

        # Cập nhật thời gian hồi chiêu
        for skill in self.skillCooldowns:
            if self.skillCooldowns[skill]["current"] > 0:
                self.skillCooldowns[skill]["current"] -= 1
        
        # Quản lý thời gian hiển thị ảnh chiêu thức
        if self.skill_image_timer > 0:
            self.skill_image_timer -= 1
            if self.skill_image_timer <= 0:
                self.skill_image = None
        # Cập nhật timer hiệu ứng Direct Shot cho tất cả bóng
        for ball in physicsEngine.ballList:
            if ball.isDirectShotEffect:
                if ball.directShotEffectTimer > 0:
                    ball.directShotEffectTimer -= 1
                else:
                    ball.isDirectShotEffect = False

        # Nagi's Dash (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["dash"]["current"] <= 0 and self.avatar == "./assets/images/Nagi.png"):
            print("Dash activated")
            self.isDashing = True
            self.skillCooldowns["dash"]["current"] = self.skillCooldowns["dash"]["max"]
            self.dashTimer = 10
            self.skill_image = "nagi_dash"
            self.skill_image_timer = 120  # 1 giây (120 FPS * 1)
            if currentKeys[self.keyUp]:
                self.vy = -self.dashSpeed
            elif currentKeys[self.keyDown]:
                self.vy = self.dashSpeed
            elif currentKeys[self.keyLeft]:
                self.vx = -self.dashSpeed
            elif currentKeys[self.keyRight]:
                self.vx = self.dashSpeed
            else:
                dash_dir = 1 if self.team == "BLUE" else -1
                self.vx = dash_dir * self.dashSpeed

        # Nagi's Magnet (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["magnet"]["current"] <= 0 and self.avatar == "./assets/images/Nagi.png" and not self.isShootDelay):
            print("Magnet activated - Checking range")
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    print(f"Ball in range: {((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5}")
                    self.isShootDelay = True
                    self.skillCooldowns["magnet"]["current"] = self.skillCooldowns["magnet"]["max"]
                    self.shootDelayTimer = 360  # 3 giây (120 FPS * 3)
                    self.shootTargetBall = ball
                    self.grab_ball(ball)
                    ball.besteal = self
                    self.skill_image = "nagi_magnet"
                    self.skill_image_timer = 120  # 1 giây
                    # Đặt vận tốc về 0 khi kích hoạt Magnet
                    self.vx = 0
                    self.vy = 0
                    break
            else:
                print("No ball in range")

        # Isagi's Flow State (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["flow"]["current"] <= 0 and self.avatar == "./assets/images/Isagi.png"):
            print("Flow State activated")
            self.skill_image = "isagi_flow"
            self.skill_image_timer = 120  # 1 giây
            self.isFlowState = True
            self.skillCooldowns["flow"]["current"] = self.skillCooldowns["flow"]["max"]
            self.flowStateTimer = 840  # 7 giây

        # Isagi's Direct Shot (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["direct"]["current"] <= 0 and self.avatar == "./assets/images/Isagi.png"):
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            distance_to_goal = ((self.x - target_goal.xm) ** 2 + (self.y - target_goal.ym) ** 2) ** 0.5
            if distance_to_goal < 350:
                print("Direct Shot activated")
                self.skill_image = "isagi_direct"
                self.skill_image_timer = 120  # 1 giây
                self.isDirectShot = True
                self.skillCooldowns["direct"]["current"] = self.skillCooldowns["direct"]["max"]
                for ball in physicsEngine.ballList:
                    if self.is_in_range(ball):
                        ball.besteal = self
                        self.shoot_direct(ball, target_goal)
                        break
            else:
                print("Not in range for Direct Shot")
            # Debug tổng quan: Xác định nhân vật và avatar
            print(f"Player: {self.nick}, Avatar: {self.avatar}")

        # Debug phím Skill 1 (Samba Dance - Q)
        #if currentKeys[self.keyAbility]:
            #print(f"Skill 1 (Q) pressed: Cooldown = {self.skillCooldowns['samba']['current']}")
        #if not previousKeys[self.keyAbility]:
            #print("Skill 1 (Q) is a new press (not held)")
        #print(f"Player: {self.nick}, Avatar: {self.avatar}, Q: {currentKeys[self.keyAbility]}, V: {currentKeys[self.keyShoot]}")

        # Skill 1: Samba Dance
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["samba"]["current"] <= 0 and self.avatar == "./assets/images/Bachira.png"):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):  # Kiểm tra khoảng cách đến bóng
                    print("Samba Dance activated")
                    ball.besteal =self
                    self.isSambaDance = True
                    self.skillCooldowns["samba"]["current"] = self.skillCooldowns["samba"]["max"]
                    self.sambaDanceTimer = 120
                    self.sambaDanceBall = ball  # Gán bóng gần nhất
                    self.sambaZigzagPhase = 0
                    direction = pygame.math.Vector2(0, 0)
                    self.skill_image = "bachira_samba"
                    self.skill_image_timer = 120  # 1 giây
                    if currentKeys[self.keyUp]:
                        direction = pygame.math.Vector2(0, -1)
                    elif currentKeys[self.keyDown]:
                        direction = pygame.math.Vector2(0, 1)
                    elif currentKeys[self.keyLeft]:
                        direction = pygame.math.Vector2(-1, 0)
                    elif currentKeys[self.keyRight]:
                        direction = pygame.math.Vector2(1, 0)
                    else:
                        direction = pygame.math.Vector2(1 if self.team == "BLUE" else -1, 0)
                    direction.normalize_ip()
                    self.vx = direction.x * self.sambaDanceSpeed
                    self.vy = direction.y * self.sambaDanceSpeed
                    gameHandler.kickSound.play()
                    break
            else:
                print("Samba Dance failed: No ball in range")

        # Quản lý Samba Dance
        if self.isSambaDance:
            if self.sambaDanceTimer > 0:
                self.sambaDanceTimer -= 1
                self.sambaZigzagPhase += 0.2  # Tốc độ zigzag
                zigzag_offset = math.sin(self.sambaZigzagPhase) * 10  # Độ lệch zigzag
                if self.sambaDanceBall:
                    direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                    perpendicular = pygame.math.Vector2(-direction.y, direction.x)
                    self.sambaDanceBall.x = self.x + direction.x * (self.r + self.sambaDanceBall.r + 5) + perpendicular.x * zigzag_offset
                    self.sambaDanceBall.y = self.y + direction.y * (self.r + self.sambaDanceBall.r + 5) + perpendicular.y * zigzag_offset
                    self.sambaDanceBall.vx = self.vx
                    self.sambaDanceBall.vy = self.vy
            else:
                self.isSambaDance = False
                self.sambaDanceBall = None
                self.vx *= 0.5
                self.vy *= 0.5

            # Debug trạng thái Samba Dance
            #if self.isSambaDance:
                #print(f"Samba Dance active: Timer = {self.sambaDanceTimer}")

        # Debug phím Skill 2 (Free Nutmeg - V)
        #if currentKeys[self.keyShoot]:
            #print(f"Skill 2 (V) pressed: Cooldown = {self.skillCooldowns['monster']['current']}")
        #if not previousKeys[self.keyShoot]:
            #print("Skill 2 (V) is a new press (not held)")

        # Skill 2: Free Nutmeg
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and self.skillCooldowns["monster"]["current"] <= 0 and self.avatar == "./assets/images/Bachira.png"):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    for opponent in physicsEngine.playerList:
                        if opponent != self and self.is_in_range_to_player(opponent) and opponent.team != self.team:
                            print(f"Free Nutmeg activated - Opponent: {opponent.nick}")
                            self.isFreeNutmeg = True
                            self.skillCooldowns["monster"]["current"] = self.skillCooldowns["monster"]["max"]
                            self.nutmegTimer = 216  # Thời gian kỹ năng: 1.8 giây
                            self.skill_image = "bachira_monster"
                            self.skill_image_timer = 120  # 1 giây
                            self.nutmegTargetBall = ball
                            self.nutmegTargetPlayer = opponent
                            opponent.dead =True
                            self.nutmegTargetPlayer.nutmegFreezeTimer = 360  # 3 giây (120 FPS * 3)
                            ball.besteal =self
                            self.grab_ball(ball)
                            gameHandler.kickSound.play()
                            break
                    else:
                        print("Free Nutmeg failed: No opponent in range")
                    break
            else:
                print("Free Nutmeg failed: No ball in range")
                # Debug trạng thái Free Nutmeg
        if self.isFreeNutmeg:
            print(f"Free Nutmeg active: Timer = {self.nutmegTimer}, Freeze Timer = {self.nutmegTargetPlayer.nutmegFreezeTimer if self.nutmegTargetPlayer else 'None'}")

        if  self.nutmegTargetPlayer:
            if self.nutmegTargetPlayer.nutmegFreezeTimer>0: 
                self.nutmegTargetPlayer.nutmegFreezeTimer -= 1
            else:
                self.nutmegTargetPlayer.dead = False
                self.nutmegTargetPlayer = None
        # Quản lý Free Nutmeg
        if self.isFreeNutmeg:
            if self.nutmegTimer > 0:
                self.nutmegTimer -= 1
                if self.nutmegTargetPlayer and self.nutmegTargetPlayer.nutmegFreezeTimer > 0:
                    self.nutmegTargetPlayer.vx = 0
                    self.nutmegTargetPlayer.vy = 0  # Đóng băng đối thủ
                    print("wut")

                if self.nutmegTimer > 156:  # Giai đoạn đưa bóng qua (0-0.5s)
                    if self.nutmegTargetBall and self.nutmegTargetPlayer:
                        direction = pygame.math.Vector2(self.nutmegTargetPlayer.x - self.x, self.nutmegTargetPlayer.y - self.y).normalize()
                        self.nutmegTargetBall.x = self.x + direction.x * 150
                        self.nutmegTargetBall.y = self.y + direction.y * 150
                        self.nutmegTargetBall.vx = direction.x * 15
                        self.nutmegTargetBall.vy = direction.y * 15
                elif self.nutmegTimer > 36:  # Giai đoạn chạy vòng (0.5-1.5s)
                    if self.nutmegTargetPlayer and self.nutmegTargetBall:
                        target_pos = pygame.math.Vector2(self.nutmegTargetBall.x, self.nutmegTargetBall.y)
                        player_pos = pygame.math.Vector2(self.x, self.y)
                        direction_to_ball = (target_pos - player_pos).normalize()
                        perpendicular = pygame.math.Vector2(-direction_to_ball.y, direction_to_ball.x)
                        curve_offset = perpendicular * math.sin(self.nutmegTimer * 0.08) * 70
                        self.vx = (direction_to_ball.x * 20 + curve_offset.x) * 0.7
                        self.vy = (direction_to_ball.y * 20 + curve_offset.y) * 0.7
                else:  # Giai đoạn kết thúc (1.5-1.8s)
                    self.isFreeNutmeg = False
                    self.nutmegTargetBall = None
                    self.vx *= 0.5
                    self.vy *= 0.5
            else:
                self.isFreeNutmeg = False
                self.nutmegTargetBall = None

        # Skill 1: Magical Turn (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["magical"]["current"] <= 0 and self.avatar == "./assets/images/Sae.png"):
            nearest_opponent = None
            min_distance = float('inf')
            for opponent in physicsEngine.playerList:
                if opponent != self and opponent.team != self.team:
                    distance = ((self.x - opponent.x) ** 2 + (self.y - opponent.y) ** 2) ** 0.5
                    if distance < min_distance and distance < 100:  # Phạm vi gần đối thủ
                        min_distance = distance
                        nearest_opponent = opponent
            if nearest_opponent:
                for ball in physicsEngine.ballList:
                    if self.is_in_range(ball):
                        print("Magical Turn kích hoạt!")
                        self.skill_image = "sae_magical"
                        self.skill_image_timer = 120  # 1 giây
                        self.isMagicalTurn = True
                        self.skillCooldowns["magical"]["current"] = self.skillCooldowns["magical"]["max"]
                        self.magicalTurnTimer = 30  # 0.25 giây (rất nhanh, 120 FPS * 0.25)
                        self.magicalTurnBall = ball
                        ball.besteal =self
                        self.magicalTurnPhase = 0
                        # Tính toán điểm đích (B) sau lưng đối thủ
                        direction = pygame.math.Vector2(nearest_opponent.x - self.x, nearest_opponent.y - self.y)
                        distance_to_opponent = direction.length()
                        direction.normalize_ip()
                        self.startX = self.x  # Lưu vị trí bắt đầu
                        self.startY = self.y
                        self.targetX = self.x + direction.x * distance_to_opponent * 2  # Điểm B
                        self.targetY = self.y + direction.y * distance_to_opponent * 2
                        self.dashDirection = direction  # Hướng di chuyển
                        gameHandler.kickSound.play()
                        break
                else:
                    print("Magical Turn thất bại: Không có bóng trong tầm!")
            else:
                print("Magical Turn thất bại: Không có đối thủ gần!")
        # Skill 2: Perfect Shot (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["perfect"]["current"] <= 0 and self.avatar == "./assets/images/Sae.png"):
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            distance_to_border = min(abs(self.x - stadiumWidth / 2), abs(self.x + stadiumWidth / 2))
            spin_factor = max(10, 20 - distance_to_border / 100)  # Tăng độ xoáy gần biên (tối đa 20)
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    print("Perfect Shot kích hoạt!")
                    self.skill_image = "sae_perfect"
                    self.skill_image_timer = 120  # 1 giây
                    self.isPerfectShot = True
                    self.skillCooldowns["perfect"]["current"] = self.skillCooldowns["perfect"]["max"]
                    self.perfectShotTimer = 240  # 2 giây hiệu ứng (120 FPS * 2)
                    self.perfectShotTargetBall = ball
                    ball.besteal =self
                    self.shoot_perfect(ball, target_goal, spin_factor)
                    break
            else:
                print("Perfect Shot thất bại: Không có bóng trong tầm!")

                
        # Quản lý Magical Turn
        if self.isMagicalTurn:
            if self.magicalTurnTimer > 0:
                self.magicalTurnTimer -= 1
                self.magicalTurnPhase += 0.5  # Tốc độ vòng cung
                # Di chuyển vòng cung cực nhanh
                progress = 1 - self.magicalTurnTimer / 30  # Tiến độ từ 0 đến 1
                perpendicular = pygame.math.Vector2(-self.dashDirection.y, self.dashDirection.x)
                curve_offset = perpendicular * math.sin(progress * math.pi) * 50  # Vòng cung nhẹ
                self.x = self.startX + (self.targetX - self.startX) * progress + curve_offset.x
                self.vx = (self.targetX - self.startX) / 30  # Tốc độ cực nhanh
                self.y = self.startY + (self.targetY - self.startY) * progress + curve_offset.y
                self.vy = (self.targetY - self.startY) / 30
                
                if self.magicalTurnBall:
                    # Bóng dính chân trong quá trình di chuyển
                    ball_direction = self.dashDirection
                    self.magicalTurnBall.x = self.x + ball_direction.x * (self.r + self.magicalTurnBall.r + 5)
                    self.magicalTurnBall.y = self.y + ball_direction.y * (self.r + self.magicalTurnBall.r + 5)
                    self.magicalTurnBall.vx = self.vx
                    self.magicalTurnBall.vy = self.vy
            else:
                # Kết thúc Magical Turn, nhả bóng
                self.isMagicalTurn = False
                if self.magicalTurnBall:
                    self.magicalTurnBall.vx = self.dashDirection.x * 5  # Nhả bóng nhẹ
                    self.magicalTurnBall.vy = self.dashDirection.y * 5
                    self.magicalTurnBall = None
                self.vx = 0
                self.vy = 0

        # Quản lý Perfect Shot
        if self.isPerfectShot:
            if self.perfectShotTimer > 0:
                self.perfectShotTimer -= 1
            else:
                self.isPerfectShot = False
                self.perfectShotTargetBall = None

        # Skill 1: Dribbling Lord (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["dribbling"]["current"] <= 0 and self.avatar == "./assets/images/Barou.png"):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    print("Dribbling Lord kích hoạt!")
                    self.skill_image = "barou_dribbling"
                    ball.besteal = self
                    self.skill_image_timer = 120  # 1 giây
                    self.isDribblingLord = True
                    self.skillCooldowns["dribbling"]["current"] = self.skillCooldowns["dribbling"]["max"]
                    self.dribblingLordTimer = 240  # 2 giây (120 FPS * 2), chia thành 3 giai đoạn
                    self.dribblingLordBall = ball
                    self.dribblingLordPhase = 0
                    # Xác định hướng dựa trên phím bấm
                    direction = pygame.math.Vector2(0, 0)
                    if currentKeys[self.keyRight]:  # D
                        direction = pygame.math.Vector2(1, 0)  # Qua phải
                    elif currentKeys[self.keyLeft]:  # A
                        direction = pygame.math.Vector2(-1, 0)  # Qua trái
                    elif currentKeys[self.keyUp]:  # W
                        direction = pygame.math.Vector2(0, -1)  # Lên trên
                    elif currentKeys[self.keyDown]:  # S
                        direction = pygame.math.Vector2(0, 1)  # Xuống dưới
                    else:
                        direction = pygame.math.Vector2(1 if self.team == "BLUE" else -1, 0)  # Mặc định theo đội
                    self.dribblingLordDirection = direction
                    gameHandler.kickSound.play()
                    break
            else:
                print("Dribbling Lord thất bại: Không có bóng trong tầm!")

        # Skill 2: KingShot (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["king"]["current"] <= 0 and self.avatar == "./assets/images/Barou.png" and not self.isKingShot):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    print("KingShot kích hoạt!")
                    self.skill_image = "barou_king"
                    ball.besteal =self
                    self.skill_image_timer = 120  # 1 giây
                    self.isKingShot = True
                    self.skillCooldowns["king"]["current"] = self.skillCooldowns["king"]["max"]
                    self.kingShotTimer = 60  # 0.5 giây lấy đà (120 FPS * 0.5)
                    self.kingShotTargetBall = ball
                    self.vx = 0  # Đứng im khi lấy đà
                    self.vy = 0
                    self.grab_ball(ball)  # Giữ bóng trước khi sút
                    break
            else:
                print("KingShot thất bại: Không có bóng trong tầm!")

        # Quản lý Dribbling Lord
        if self.isDribblingLord:
            if self.dribblingLordTimer > 0:
                self.dribblingLordTimer -= 1
                direction = self.dribblingLordDirection.normalize()
                speed = 6  # Tốc độ dash
                
                if self.dribblingLordTimer > 160:  # Giai đoạn 1: Dash xuống 45 độ (0.25s đầu tiên)
                    angle = math.radians(45)  # Xuống 45 độ so với phương ngang
                    self.vx = (direction.x * math.cos(angle) + direction.y * math.sin(angle)) * speed
                    self.vy = (direction.x * math.sin(angle) - direction.y * math.cos(angle)) * speed
                elif self.dribblingLordTimer > 80:  # Giai đoạn 2: Dash lên 45 độ (0.25-0.5s)
                    angle = math.radians(-45)  # Lên 45 độ so với phương ngang
                    self.vx = (direction.x * math.cos(angle) + direction.y * math.sin(angle)) * speed
                    self.vy = (direction.x * math.sin(angle) - direction.y * math.cos(angle)) * speed
                else:  # Giai đoạn 3: Dash xuống 45 độ (0.5-0.75s)
                    angle = math.radians(45)  # Xuống 45 độ so với phương ngang
                    self.vx = (direction.x * math.cos(angle) + direction.y * math.sin(angle)) * speed
                    self.vy = (direction.x * math.sin(angle) - direction.y * math.cos(angle)) * speed

                # Giữ bóng theo hướng di chuyển
                if self.dribblingLordBall:
                    ball_direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                    self.dribblingLordBall.x = self.x + ball_direction.x * (self.r + self.dribblingLordBall.r + 5)
                    self.dribblingLordBall.y = self.y + ball_direction.y * (self.r + self.dribblingLordBall.r + 5)
                    self.dribblingLordBall.vx = self.vx
                    self.dribblingLordBall.vy = self.vy
            else:
                # Kết thúc Dribbling Lord, nhả bóng
                self.isDribblingLord = False
                if self.dribblingLordBall:
                    direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                    self.dribblingLordBall.vx = direction.x * 5  # Nhả bóng nhẹ
                    self.dribblingLordBall.vy = direction.y * 5
                    self.dribblingLordBall = None
                self.vx = 0
                self.vy = 0
        # Quản lý KingShot
        if self.isKingShot:
            if self.kingShotTimer > 0:
                self.kingShotTimer -= 1
                if self.kingShotTargetBall:
                    self.grab_ball(self.kingShotTargetBall)  # Giữ bóng trong lúc lấy đà
            else:
                # Sút bóng sau khi hết thời gian lấy đà
                if self.kingShotTargetBall:
                    self.shoot_kingshot(self.kingShotTargetBall)
                    self.isKingShot = False
                    self.kingShotTargetBall = None

        # Skill 1: Body Block (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["block"]["current"] <= 0 and self.avatar == "./assets/images/Kunigami.png"):
            for opponent in physicsEngine.playerList:
                if opponent != self and opponent.team != self.team and self.is_in_range_to_player(opponent):
                    print("Body Block activated!")
                    self.skill_image = "kunigami_block"
                    self.skill_image_timer = 120  # 1 giây
                    self.isBodyBlock = True
                    self.skillCooldowns["block"]["current"] = self.skillCooldowns["block"]["max"]
                    self.bodyBlockTimer = 180  # 1.5 giây hiệu ứng
                    self.bodyBlockTargetPlayer = opponent
                    opponent.dead=True
                    self.body_block(opponent, stadiumWidth)  # Truyền stadiumWidth nếu dùng Cách 1
                    gameHandler.kickSound.play()
                    break
            else:
                print("Body Block failed: No opponent in range")

        # Quản lý Body Block
        if self.isBodyBlock:
            if self.bodyBlockTimer > 0:
                self.bodyBlockTimer -= 1
                if self.bodyBlockTimer <120 and self.bodyBlockTargetPlayer:
                    self.bodyBlockTargetPlayer.dead =False
            else:
                self.isBodyBlock = False
                self.bodyBlockTargetPlayer = None
        # Skill 2: Wild Shot (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["wild"]["current"] <= 0 and self.avatar == "./assets/images/Kunigami.png" and not self.isWildShot):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    print("Wild Shot activated!")
                    ball.besteal = self
                    self.skill_image = "kunigami_wild"
                    self.skill_image_timer = 120  # 1 giây
                    self.isWildShot = True
                    self.skillCooldowns["wild"]["current"] = self.skillCooldowns["wild"]["max"]
                    self.wildShotTimer = 144  # 1.2 giây lấy đà (120 FPS * 1.2)
                    self.wildShotTargetBall = ball
                    self.vx = 0  # Đứng im khi lấy đà
                    self.vy = 0
                    self.grab_ball(ball)  # Giữ bóng trước khi sút
                    break
            else:
                print("Wild Shot failed: No ball in range")

        # Quản lý Wild Shot
        if self.isWildShot:
            if self.wildShotTimer > 0:
                self.wildShotTimer -= 1
                if self.wildShotTargetBall:
                    self.grab_ball(self.wildShotTargetBall)  # Giữ bóng trong lúc lấy đà
            else:
                if self.wildShotTargetBall:
                    self.shoot_wildshot(self.wildShotTargetBall, currentKeys)
                    self.isWildShot = False
                    self.wildShotTargetBall = None
        # Skill 1: Ace Eater (Q)
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["Ace"]["current"] <= 0 and self.avatar == "./assets/images/Lorenzo.png"):
            for opponent in physicsEngine.playerList:
                if opponent != self and opponent.team != self.team and self.is_in_range_to_player(opponent):
                    for ball in physicsEngine.ballList:
                        if ((opponent.x - ball.x) ** 2 + (opponent.y - ball.y) ** 2) ** 0.5 < 70:  # Đối thủ đang gần bóng
                            print("Ace Eater activated!")
                            self.skill_image = "lorenzo_ace"
                            ball.besteal =self
                            self.skill_image_timer = 120  # 1 giây
                            self.isAceEater = True
                            self.skillCooldowns["Ace"]["current"] = self.skillCooldowns["Ace"]["max"]
                            self.aceEaterTimer = 360  # 3 giây hiệu ứng (120 FPS * 3)
                            self.aceEaterPhase = 0
                            self.aceEaterStartX = self.x  # Lưu vị trí ban đầu
                            self.aceEaterStartY = self.y
                            self.aceEaterTargetBall = ball
                            self.aceEaterTargetPlayer = opponent
                            self.x = ball.x  # Dash cực nhanh đến bóng
                            self.y = ball.y
                            self.vx = 0
                            self.vy = 0
                            self.grab_ball(ball)  # Cướp bóng
                            gameHandler.kickSound.play()
                            break
                    break
            else:
                print("Ace Eater failed: No opponent with ball in range")

        # Quản lý Ace Eater
        if self.isAceEater:
            if self.aceEaterTimer > 0:
                self.aceEaterTimer -= 1
                self.aceEaterPhase += 0.2  # Tốc độ xoay
                if self.aceEaterTimer > 180:  # Giai đoạn 1: Cướp bóng (0-1.5s)
                    if self.aceEaterTargetBall:
                        self.grab_ball(self.aceEaterTargetBall)
                else:  # Giai đoạn 2: Dash về vị trí ban đầu (1.5-3s)
                    direction = pygame.math.Vector2(self.aceEaterStartX - self.x, self.aceEaterStartY - self.y).normalize()
                    self.vx = direction.x * 20  # Dash cực nhanh
                    self.vy = direction.y * 20
                    if self.aceEaterTargetBall:
                        self.aceEaterTargetBall.x = self.x + direction.x * (self.r + self.aceEaterTargetBall.r + 5)
                        self.aceEaterTargetBall.y = self.y + direction.y * (self.r + self.aceEaterTargetBall.r + 5)
                        self.aceEaterTargetBall.vx = self.vx
                        self.aceEaterTargetBall.vy = self.vy
            else:
                self.isAceEater = False
                self.aceEaterTargetBall = None
                self.vx = 0
                self.vy = 0
        # Skill 2: Zombie Dribbling (V)
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["zombie"]["current"] <= 0 and self.avatar == "./assets/images/Lorenzo.png"):
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    min_distance_to_opponent = float('inf')
                    for opponent in physicsEngine.playerList:
                        if opponent != self and opponent.team != self.team:
                            distance = ((opponent.x - ball.x) ** 2 + (opponent.y - ball.y) ** 2) ** 0.5
                            if distance < min_distance_to_opponent:
                                min_distance_to_opponent = distance
                    if self.is_in_range(ball) and min_distance_to_opponent > 70:  # Lorenzo gần bóng hơn đối thủ
                        print("Zombie Dribbling activated!")
                        ball.besteal = self
                        self.skill_image = "lorenzo_zombie"
                        self.skill_image_timer = 120  # 1 giây
                        self.isZombieDribbling = True
                        self.skillCooldowns["zombie"]["current"] = self.skillCooldowns["zombie"]["max"]
                        self.zombieDribblingTimer = 660  # 5.5 giây (120 FPS * 5.5)
                        self.zombieDribblingBall = ball
                        self.grab_ball(ball)
                        gameHandler.kickSound.play()
                        break
            else:
                print("Zombie Dribbling failed: Ball not close enough or opponent too near")

        # Quản lý Zombie Dribbling
        if self.isZombieDribbling:
            if self.zombieDribblingTimer > 0:
                self.zombieDribblingTimer -= 1
                if self.zombieDribblingBall:
                    self.grab_ball(self.zombieDribblingBall)  # Bóng dính chân
                self.mass = 1000  # Tăng mass để xuyên qua đối thủ
            else:
                self.isZombieDribbling = False
                self.zombieDribblingBall = None
                self.mass = self.normalMass  # Khôi phục mass
                self.vx *= 0.5
                self.vy *= 0.5
        #Skill 1 Rin
        if (currentKeys[self.keyAbility] and not previousKeys[self.keyAbility] and 
            self.skillCooldowns["curve"]["current"] <= 0 and self.avatar == "./assets/images/Rin.png" and not self.isCS):

            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    ball.besteal =self
                    self.CSball = ball
                    self.isCS = True
                    ball.immune = True
                    self.skillCooldowns["curve"]["current"] = self.skillCooldowns["curve"]["max"]
                    self.CSgoal = 600 if self.team == "RED" else -600
                    self.cx = (ball.x +self.CSgoal)/2
                    self.CSTimer = abs(ball.x-self.CSgoal)/4-40
                    self.cy = ball.y+(800 if self.team == "RED" else -800)
                    self.skill_image = "rin_curve"  # Tên hình ảnh cần khớp với file trong thư mục tài nguyên
                    self.skill_image_timer = 120
                    break
        if self.isCS:
            if self.CSTimer>0:
                if self.CSball:
                    if self.CSball.besteal != self:
                        self.CSball.immune = False
                        self.CSball = None
                        self.isCS = False
                        self.CSgoal = 0
                        self.cx = 0
                        self.CSTimer = 0
                        self.cy = 0
                        
                    else:
                        print(self.CSTimer," ",self.cx-self.CSball.x," ",self.cy-self.CSball.y)
                        self.CSTimer-=1
                        self.CSball.vx = self.cx-self.CSball.x
                        self.CSball.vy = self.cy-self.CSball.y
                        dic = pygame.Vector2(self.CSball.vy,self.CSball.vx).normalize()
                        self.CSball.vx = dic.x*10
                        self.CSball.vy = -dic.y*10
                        if random.random()<0.7 :
                            self.CSball.particles.append(Particle(
                                x=self.CSball.x, 
                                y=self.CSball.y, 
                                vx=self.CSball.vx, 
                                vy=self.CSball.vy, 
                                lifetime=18,  # 0.25-0.5 giây (120 FPS)
                                color=random.choice([(7, 189, 238),(61, 234, 245),(58, 186, 220)]), 
                                size=random.uniform(3, 6)  # Kích thước nhỏ
                            ))
                        if abs(self.CSgoal - self.cx) > abs(self.CSgoal-self.CSball.x):
                            self.CSball.immune = False
            else:
                if self.CSball:
                    self.CSball.immune = False
                    self.CSball = None
                    self.isCS = False
                    
                    self.CSgoal = 0
                    self.cx = 0
                    self.CSTimer = 0
                    self.cy = 0
        #Skill 2 Rin
        if (currentKeys[self.keyShoot] and not previousKeys[self.keyShoot] and 
            self.skillCooldowns["opposite"]["current"] <= 0 and self.avatar == "./assets/images/Rin.png" and not self.isOppositeDirection):
            
            for ball in physicsEngine.ballList:
                if self.is_in_range(ball):
                    ball.besteal =self
                    self.isOppositeDirection = True
                    self.skillCooldowns["opposite"]["current"]=self.skillCooldowns["opposite"]["max"]
                    self.OppositeDirectionTimer = 90
                    self.OppositeDirectionBall = ball
                    ball.behold = True
                    if self.lastDirection == "left":
                        self.ODx = 1
                        ball.x = self.x-62.24
                        ball.y = self.y
                    elif self.lastDirection == "right":
                        self.ODx = -1
                        ball.x = self.x+62.24
                        ball.y = self.y
                    elif self.lastDirection == "up":
                        self.ODy = -1
                        ball.x = self.x
                        ball.y = self.y-62.24
                    elif self.lastDirection == "down":
                        self.ODy = 1
                        ball.x = self.x+62.24
                        ball.y = self.y
                    break
            if self.OppositeDirectionBall:
                for plr in physicsEngine.playerList:
                    if plr.is_in_range(self.OppositeDirectionBall) and plr != self:
                        self.OppositeDirectionPlayer.append(plr)
                        plr.dead =True
            
        if self.isOppositeDirection:
            if self.OppositeDirectionTimer >0 and self.OppositeDirectionBall:
                self.OppositeDirectionTimer -=1
                if self.OppositeDirectionTimer % 9 == 0:
                    print("Time to AI")
                    
                    for i in range(len(self.AIlv)-1):
                       self.AIlv[i] -= 1
                    
                    self.ODimagex.append(self.x)
                    self.ODimagey.append(self.y)
                    self.AIlv.append(2)
                    if len(self.AIlv)>5:
                        self.ODimagex.pop(0)
                        self.ODimagey.pop(0)
                        self.AIlv.pop(0)    
                    
            else:
                if self.OppositeDirectionBall:
                    self.OppositeDirectionBall.behold = False
                    self.OppositeDirectionBall.vx *= 0.7
                    self.OppositeDirectionBall.vy *= 0.7
                    self.OppositeDirectionBall = None
                    self.isOppositeDirection = False
                    self.ODx = 0
                    self.ODy = 0
                    for plr in self.OppositeDirectionPlayer:
                        plr.dead =False
                    self.OppositeDirectionPlayer.clear()
                    self.ODimagex.clear()
                    self.ODimagey.clear()
                    self.AIlv.clear()
            
            if self.OppositeDirectionTimer >60 and self.OppositeDirectionBall:

                self.vx = (-self.ODx*1.037*gameHandler.playerAcceleration + (-1.037*gameHandler.playerAcceleration*self.ODy if self.ODy !=0 else 0))*self.OppositeDirectionSpeed
                self.vy = (self.ODy*1.037*gameHandler.playerAcceleration + (1.037*gameHandler.playerAcceleration*self.ODx if self.ODx !=0 else 0))*self.OppositeDirectionSpeed
                print(self.vx," ",self.vy," ",self.x," ",self.y)
            elif self.OppositeDirectionTimer >30 and self.OppositeDirectionBall:

                self.vx = self.ODy*self.OppositeDirectionSpeed/0.4*gameHandler.playerAcceleration
                self.vy = -self.ODx*self.OppositeDirectionSpeed/0.4*gameHandler.playerAcceleration
                self.OppositeDirectionBall.vx = self.ODy*self.OppositeDirectionSpeed/0.45*gameHandler.playerAcceleration
                self.OppositeDirectionBall.vy = -self.ODx*self.OppositeDirectionSpeed/0.45*gameHandler.playerAcceleration
            else:
                if self.OppositeDirectionBall:
                    self.OppositeDirectionBall.vx = -self.ODx*self.OppositeDirectionSpeed/1*gameHandler.playerAcceleration*1.65
                    self.OppositeDirectionBall.vy = self.ODy*self.OppositeDirectionSpeed/1 *gameHandler.playerAcceleration*1.65
                    self.vx = -self.ODx*self.OppositeDirectionSpeed/1*gameHandler.playerAcceleration*1.65
                    self.vy = self.ODy*self.OppositeDirectionSpeed/1*gameHandler.playerAcceleration*1.65

        if self.skillCooldowns["opposite"]["current"] >= 1050 and self.skillCooldowns["opposite"]["current"] <= 1110:
            horizontal *= 1.25
            vertical *= 1.25
        # Quản lý Flow State
        if self.isFlowState:
            if self.flowStateTimer > 0:
                self.flowStateTimer -= 1
            else:
                self.isFlowState = False

        # Quản lý Nagi's Dash
        if self.isDashing:
            if self.dashTimer > 0:
                self.dashTimer -= 1
            else:
                self.isDashing = False
                self.vx *= 0.5
                self.vy *= 0.5

        # Quản lý Nagi's Magnet
        if self.isShootDelay:
            if self.shootDelayTimer > 0:
                self.shootDelayTimer -= 1
                self.isShooting = True
                if self.shootTargetBall:
                    self.grab_ball(self.shootTargetBall)
                if self.kicking and not self.hasKicked:
                    if self.shootTargetBall:  # Add check
                        self.shoot_ball(self.shootTargetBall, currentKeys)
                    self.isShootDelay = False
                    self.isShooting = False
                    self.shootTargetBall = None
                    self.hasKicked = True
            else:
                self.isShootDelay = False
                self.isShooting = False
                if self.shootTargetBall:  # Add check
                    self.shoot_ball(self.shootTargetBall, currentKeys)
                self.shootTargetBall = None


        # Quản lý Bachira's Samba Dance
        if self.isSambaDance:
            if self.sambaDanceTimer > 0:
                self.sambaDanceTimer -= 1
                self.sambaZigzagPhase += 0.2  # Tốc độ zigzag
                zigzag_offset = math.sin(self.sambaZigzagPhase) * 10  # Độ lệch zigzag
                if self.sambaDanceBall:
                    direction = pygame.math.Vector2(self.vx, self.vy).normalize()
                    perpendicular = pygame.math.Vector2(-direction.y, direction.x)
                    self.sambaDanceBall.x = self.x + direction.x * (self.r + self.sambaDanceBall.r + 5) + perpendicular.x * zigzag_offset
                    self.sambaDanceBall.y = self.y + direction.y * (self.r + self.sambaDanceBall.r + 5) + perpendicular.y * zigzag_offset
                    self.sambaDanceBall.vx = self.vx
                    self.sambaDanceBall.vy = self.vy
            else:
                self.isSambaDance = False
                self.sambaDanceBall = None
                self.vx *= 0.5
                self.vy *= 0.5

        # Quản lý Bachira's Free Nutmeg
        if self.isFreeNutmeg:
            if self.nutmegTimer > 0:
                self.nutmegTimer -= 1
                if self.nutmegFreezeTimer > 0:
                    self.nutmegFreezeTimer -= 1
                    if self.nutmegTargetPlayer:
                        self.nutmegTargetPlayer.vx = 0
                        self.nutmegTargetPlayer.vy = 0  # Đóng băng đối thủ
                      # Hết thời gian đóng băng

                if self.nutmegTimer > 156:  # Giai đoạn đưa bóng qua (0-0.5s)
                    if self.nutmegTargetBall and self.nutmegTargetPlayer:                        
                        direction = pygame.math.Vector2(self.nutmegTargetPlayer.x - self.x, self.nutmegTargetPlayer.y - self.y).normalize()
                        self.nutmegTargetBall.x = self.x + direction.x * 100  # Đưa bóng xa 100 đơn vị
                        self.nutmegTargetBall.y = self.y + direction.y * 100
                        self.nutmegTargetBall.vx = direction.x * 10
                        self.nutmegTargetBall.vy = direction.y * 10
                elif self.nutmegTimer > 36:  # Giai đoạn chạy vòng (0.5-1.5s)
                    if self.nutmegTargetPlayer:
                        
                        target_pos = pygame.math.Vector2(self.nutmegTargetBall.x, self.nutmegTargetBall.y)
                        player_pos = pygame.math.Vector2(self.x, self.y)
                        direction_to_ball = (target_pos - player_pos).normalize()
                        perpendicular = pygame.math.Vector2(-direction_to_ball.y, direction_to_ball.x)
                        curve_offset = perpendicular * math.sin(self.nutmegTimer * 0.05) * 50  # Vòng cung
                        self.vx = (direction_to_ball.x * 15 + curve_offset.x) * 0.5
                        self.vy = (direction_to_ball.y * 15 + curve_offset.y) * 0.5
                else:  # Giai đoạn kết thúc (1.5-1.8s)
                    
                    
                    self.isFreeNutmeg = False
                    self.nutmegTargetBall = None
                    self.vx *= 0.5
                    self.vy *= 0.5
            else:
                
                self.isFreeNutmeg = False
                self.nutmegTargetBall = None

        # Áp dụng buff từ Flow State
        speed_boost = self.flowStateSpeedBoost if self.isFlowState else 1.0
        # Không cho di chuyển khi đang trong KingShot lấy đà
        # Áp dụng buff từ Zombie Dribbling
        if not (self.isDashing or self.isSambaDance or self.isFreeNutmeg or self.isDribblingLord or self.isKingShot or self.isAceEater):
            self.vx += horizontal * speed_boost
            self.vy += vertical * speed_boost

        if self.dashCooldown > 0:
            self.dashCooldown -= 1
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

        self.hasKicked = False

        if self.kicking or self.isDashing or self.isSambaDance:
            vertical *= 0.7
            horizontal *= 0.7
        if horizontal != 0 and vertical != 0:
            vertical /= 1.41421356237
            horizontal /= 1.41421356237

        if not (self.isDashing or self.isSambaDance or self.isFreeNutmeg):
            self.vx += horizontal * self.speed * speed_boost 
            self.vy += vertical * self.speed * speed_boost             
    def shoot_kingshot(self, ball):
        """Sút KingShot với hiệu ứng knuckle ball"""
        direction = pygame.math.Vector2(0, 0)
        if self.lastDirection == "up":
            direction = pygame.math.Vector2(0, -1)
        elif self.lastDirection == "down":
            direction = pygame.math.Vector2(0, 1)
        elif self.lastDirection == "left":
            direction = pygame.math.Vector2(-1, 0)
        elif self.lastDirection == "right":
            direction = pygame.math.Vector2(1, 0)
        else:
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)

        direction.normalize_ip()
        force = 25  # Lực sút mạnh
        ball.vx = direction.x * force + random.uniform(-2, 2)  # Thêm xoáy ngẫu nhiên
        ball.vy = direction.y * force + random.uniform(-2, 2)
        ball.isDirectShotEffect = True  # Tái sử dụng hiệu ứng Direct Shot cho KingShot
        ball.directShotEffectTimer = 120  # 1 giây hiệu ứng
        gameHandler.kickSound.play()
    
    def body_block(self, opponent, stadiumWidth):
        """Cướp bóng và hất văng đối thủ ra xa"""
        direction = pygame.math.Vector2(opponent.x - self.x, opponent.y - self.y).normalize()
        force = 20  # Tăng lực hất văng để rõ hiệu ứng
        opponent.vx = direction.x * force
        opponent.vy = direction.y * force
        # Giới hạn trong sân
        opponent.x = max(-stadiumWidth / 2, min(stadiumWidth / 2, opponent.x + opponent.vx))
        opponent.y = max(-gameHandler.stadiumHeight / 2, min(gameHandler.stadiumHeight / 2, opponent.y + opponent.vy))
        # Cướp bóng nếu đối thủ đang gần bóng
        for ball in physicsEngine.ballList:
            if ((opponent.x - ball.x) ** 2 + (opponent.y - ball.y) ** 2) ** 0.5 < 70:
                self.grab_ball(ball)
                break
    def shoot_wildshot(self, ball, currentKeys):
        direction = pygame.math.Vector2(0, 0)
        if currentKeys[self.keyUp]:
            direction.y -= 1
        if currentKeys[self.keyDown]:
            direction.y += 1
        if currentKeys[self.keyLeft]:
            direction.x -= 1
        if currentKeys[self.keyRight]:
            direction.x += 1
        if direction.length() == 0:
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)
        direction.normalize_ip()
        force = 30
        ball.vx = direction.x * force
        ball.vy = direction.y * force
        ball.lastShotDirection = direction  # Lưu hướng sút
        ball.isDirectShotEffect = True
        ball.directShotEffectTimer = 240
        gameHandler.kickSound.play()
    # Hàm shoot_perfect
    def shoot_perfect(self, ball, target_goal, spin_factor):
        """Sút xoáy siêu cong và tự động nhắm khung thành"""
        # Vector từ Sae đến giữa khung thành
        direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)
        distance_to_goal = direction.length()
        direction.normalize_ip()
        
        # Tăng lực sút và độ xoáy
        force = 35  # Lực sút mạnh hơn
        perpendicular = pygame.math.Vector2(-direction.y, direction.x)  # Vector vuông góc
        
        # Tính quỹ đạo parabol với spin_factor
        spin = spin_factor * (1 if self.x < target_goal.xm else -1)  # Xoáy trái/phải tùy vị trí
        ball.vx = direction.x * force + perpendicular.x * spin
        ball.vy = direction.y * force + perpendicular.y * spin
        
        # Điều chỉnh để tự động nhắm khung thành
        time_to_goal = distance_to_goal / force  # Thời gian đến khung thành
        ball.vx += (target_goal.xm - (self.x + ball.vx * time_to_goal)) / time_to_goal  # Hiệu chỉnh X
        ball.vy += (target_goal.ym - (self.y + ball.vy * time_to_goal)) / time_to_goal  # Hiệu chỉnh Y
        
        ball.isDirectShotEffect = True
        ball.directShotEffectTimer = 240  # 2 giây hiệu ứng
        gameHandler.kickSound.play()
    def is_in_range(self, ball):
        distance = ((self.x - ball.x) ** 2 + (self.y - ball.y) ** 2) ** 0.5
        return distance < 70 and not ball.immune

    def is_in_range_to_player(self, player):
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance < 90  # Phạm vi gần đối thủ cho Free Nutmeg

    def grab_ball(self, ball):
        """Kéo bóng về phía trước"""
        direction = pygame.math.Vector2(0, 0)
        if self.lastDirection == "up":
            direction = pygame.math.Vector2(0, -1)
        elif self.lastDirection == "down":
            direction = pygame.math.Vector2(0, 1)
        elif self.lastDirection == "left":
            direction = pygame.math.Vector2(-1, 0)
        elif self.lastDirection == "right":
            direction = pygame.math.Vector2(1, 0)
        else:
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)

        direction.normalize_ip()
        ball.x = self.x + direction.x * (self.r + ball.r + 5)
        ball.y = self.y + direction.y * (self.r + ball.r + 5)
        ball.vx = 0
        ball.vy = 0

    def shoot_ball(self, ball, currentKeys):
        """Sút bóng sau độ trễ (Nagi) hoặc Kaiser Impact với auto-aim mạnh hơn"""
        direction = pygame.math.Vector2(0, 0)
        if self.kaiser_impact_active and self.avatar == "./assets/images/Kaiser.png":
            target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
            direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)
            distance_to_goal = direction.length()
            direction.normalize_ip()
            
            force = 600 
            perpendicular = pygame.math.Vector2(-direction.y, direction.x)
            
            distance_to_border = min(abs(self.x - gameHandler.stadiumWidth / 2), abs(self.x + gameHandler.stadiumWidth / 2))
            spin_factor = max(10, 20 - distance_to_border / 100)  
            spin = spin_factor * (1 if self.x < target_goal.xm else -1)
            ball.vx = direction.x * force + perpendicular.x * spin
            ball.vy = direction.y * force + perpendicular.y * spin
            
            time_to_goal = distance_to_goal / force/10
            ball.vx += (target_goal.xm - (self.x + ball.vx * time_to_goal)) / time_to_goal
            ball.vy += (target_goal.ym - (self.y + ball.vy * time_to_goal)) / time_to_goal
            
            ball.isDirectShotEffect = True
            ball.directShotEffectTimer = 300
        else:
            # Logic sút bóng thông thường cho các nhân vật khác
            if self.lastDirection == "up":
                direction = pygame.math.Vector2(0, -1)
            elif self.lastDirection == "down":
                direction = pygame.math.Vector2(0, 1)
            elif self.lastDirection == "left":
                direction = pygame.math.Vector2(-1, 0)
            elif self.lastDirection == "right":
                direction = pygame.math.Vector2(1, 0)
            else:
                target_goal = physicsEngine.goalList[1] if self.team == "RED" else physicsEngine.goalList[0]
                direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)
            if currentKeys[self.keyLeft]:
                direction.x -= 1
            if currentKeys[self.keyRight]:
                direction.x += 1
            if currentKeys[self.keyUp]:
                direction.y -= 1
            if currentKeys[self.keyDown]:
                direction.y += 1
            if direction.length() == 0:
                direction.x = 1 if self.team == "RED" else -1
            direction.normalize_ip()
            ball.vx = direction.x * self.shootForce
            ball.vy = direction.y * self.shootForce
        gameHandler.kickSound.play()

    def shoot_direct(self, ball, target_goal):
        """Sút thẳng vào khung thành (Isagi's Direct Shot)"""
        direction = pygame.math.Vector2(target_goal.xm - self.x, target_goal.ym - self.y)
        direction.normalize_ip()
        force = 15
        if self.isFlowState:
            force *= self.flowStateKickBoost
        ball.vx = direction.x * force
        ball.vy = direction.y * force
        ball.isDirectShotEffect = True
        ball.directShotEffectTimer = 60
        self.isDirectShot = False
        gameHandler.kickSound.play()
    def is_to_goal(self,bal,goalx):
        x = bal.x-self.x
        y = bal.y-self.y
        x1 = goalx - self.x
        y1 = y*x1/x
        y1 +=self.y
        #print(f"{self.nick}: {y1}")
        if abs(self.x)>abs(bal.x):
            if y<0:
                return 1
            else :
                return -1
        else:
            if y1<-106:
                return 1
            elif y1>106:
                return -1
            else: return 0

    def botmove(self, botlv, bal):

        vertical = 0
        horizontal = 0

        # Xác định hướng khung thành đối phương và khung thành của mình
        target_goal_x = gameHandler.stadiumWidth / 2-25 if self.team == "RED" else 0-gameHandler.stadiumWidth / 2+25
        own_goal_x = -gameHandler.stadiumWidth / 2 if self.team == "RED" else gameHandler.stadiumWidth / 2
        goal_dir_x = target_goal_x - bal.x
        goal_dir_y = 0 - bal.y
        goal_dis = math.sqrt(goal_dir_x * goal_dir_x + goal_dir_y * goal_dir_y)
        if goal_dis > 0:
            goal_dir_x /= goal_dis
            goal_dir_y /= goal_dis

       
        hx = bal.x - self.x
        hy = bal.y - self.y
        dis = math.sqrt(hx * hx + hy * hy)
        if dis > 0:
            hx /= dis
            hy /= dis

        # Kiểm tra bóng ở góc sân
        ball_in_corner = (abs(bal.x) >= gameHandler.stadiumWidth/2 - 110 and (abs(bal.y) >= gameHandler.stadiumHeight/2-120 or abs(bal.y-106)<=16+20 or abs(bal.y+106)<=16+20))
        print(ball_in_corner)
        near_wall = abs(self.x) > (gameHandler.stadiumWidth / 2 - 50) or abs(self.y) > (gameHandler.stadiumHeight / 2 - 50)
        #print(ball_in_corner)
        # Kiểm tra xem có bot đồng đội nào gần bóng không
        teammate_near = False
        for other_bot in physicsEngine.playerList:
            if other_bot != self and other_bot.team == self.team:
                bot_dis = math.sqrt((bal.x - other_bot.x) ** 2 + (bal.y - other_bot.y) ** 2)
                if bot_dis < 50:
                    teammate_near = True
                    break

        # Kiểm tra xem bóng có đang bị người chơi giữ không
        ball_controlled = False
        for player in physicsEngine.playerList:
            plrx = bal.x - player.x
            plry = bal.y - player.y
            disp = math.sqrt(plrx ** 2 + plry ** 2)
            if player !=self and disp<47:
                ball_controlled = True
                break


        # Điều chỉnh hướng di chuyển
        if ball_in_corner and dis <= 50:  # Bóng ở góc và bot gần bóng
            # Rê bóng ra giữa sân, tránh khung thành của mình
            print("rê bóng")
#            if mid_dis > 0:
#                mid_field_x /= mid_dis
#                mid_field_y /= mid_dis
#            hx = bal.x - self.x
#            hy = bal.y - self.y
#            hy -= 60 if bal.y >= 0 else -60
#            dis = math.sqrt(hx * hx + hy * hy)
#            if dis > 0:
#                hx /= dis
#                hy /= dis

            if abs(self.x - 0) < abs(bal.x - 0)+40:
                    t = hx
                    t2 = hy
                    hx = hy
                    hy = t
                    if (bal.y <0 and self.team == "BLUE") or (bal.y >=0 and self.team == "RED"):
                        hx = hx*-1.2 +0.35*t
                        hy += 0.35*t2
                    else:
                        hy = -1.2*hy +0.35*t2
                        hx += 0.35*t
            vertical += gameHandler.playerAcceleration * hy * 3
            horizontal += gameHandler.playerAcceleration * hx * 3            
        elif ball_controlled:  # Tranh bóng khi đối thủ giữ
            print("tranh")
            vertical += gameHandler.playerAcceleration * hy * 5
            horizontal += gameHandler.playerAcceleration * hx * 5
        elif dis <= 50:  # Gần bóng, rê về khung thành đối phương
            if abs(bal.x - own_goal_x) < 175+25*(botlv+1):  # Gần khung thành mình, rê ra giữa
                if abs(self.x - own_goal_x) > abs(bal.x - own_goal_x)-40:
                    t = hx
                    t2 = hy
                    hx = hy
                    hy = t
                    if (bal.y <0 and self.team == "BLUE") or (bal.y >=0 and self.team == "RED"):
                        hx = hx*(-1.3-0.15*botlv) +0.35*t
                        hy += (0.35)*t2 +hy*0.15*botlv
                    else:
                        hy = (-1.3-0.15*botlv)*hy +0.35*t2
                        hx += (0.35)*t +hx*0.15*botlv
                    print("save"," ",hx," ",hy)
                else:
                    hx*=1.05
                    hy*=1.05
                    print("payback")
            else:
                
#                hx*=1.05
#                hy*=1.05
#                vertical += gameHandler.playerAcceleration * hy * 5
#                horizontal += gameHandler.playerAcceleration * hx * 5
                sec = self.is_to_goal(bal,target_goal_x)
                if sec != 0:
                    #print("atkback",dis)
                    t = hx
                    t2 = hy
                    hx = hy
                    hy = t
                    if (sec>0 and self.team=="BLUE")or(sec<=0 and self.team=="RED"):
                        hx = hx*(-1.35-botlv*0.1) +0.35*t
                        hy += hy*(botlv*0.1)+0.35*t2 
                        print("left")
                    else:
                        hy = (-1.35-botlv*0.1)*hy +0.35*t2
                        hx += hx*(botlv*0.1)+0.35*t
                        print("right")
                    if self.team=="RED":
                        hx*=1.15
                        hy*=1.15
                else:
                    print("atkfront",dis)
                    hx = bal.x - self.x
                    hy = bal.y - self.y
                    dis = math.sqrt(hx * hx + hy * hy)
                    if dis > 0:
                        hx /= dis
                        hy /= dis
                    hx*=1.05
                    hy*=1.05
                
            vertical += gameHandler.playerAcceleration * hy * 3
            horizontal += gameHandler.playerAcceleration * hx * 3
        else:  # Xa bóng, đuổi theo bóng
            print("chase ",dis)
            hx*=1.05
            hy*=1.05
            vertical += gameHandler.playerAcceleration * hy * 5
            horizontal += gameHandler.playerAcceleration * hx * 5

        # Logic rê bóng và đá bóng
        kick_chance = False
        if dis - bal.r - self.r <= 5 and not self.hasKicked:
            ball_to_goal = target_goal_x - bal.x
            ball_to_own_goal = own_goal_x - bal.x
            if (self.team == "RED" and ball_to_goal > 0) or (self.team == "BLUE" and ball_to_goal < 0):
                if botlv == 1:  # Easy: Đá ngẫu nhiên
                    kick_chance = random.random() < 0.3
                elif botlv == 2:  # Medium: Đá khi gần khung thành hoặc tranh bóng
                    kick_chance = (random.random() < 0.6 and abs(self.x - target_goal_x) < 300 and abs(ball_to_own_goal) > 200) or \
                                  (ball_controlled and random.random() < 0.8)
                elif botlv == 3:  # Hard: Đá chính xác hơn
                    kick_chance = random.random() < 0.9 and abs(self.x - target_goal_x) < 400 and abs(ball_to_own_goal) > 200

            # Xử lý bóng ở góc: Đá ra nếu quá gần góc và không rê được
            if ball_in_corner and near_wall and abs(bal.vx) < 1 and abs(bal.vy) < 1 and not teammate_near:
                kick_chance = random.random() < 0.5
            elif near_wall and abs(bal.vx) < 1 and abs(bal.vy) < 1 and teammate_near:
                kick_chance = False  # Tránh spam khi có đồng đội gần

            if kick_chance and self.kcd <= 0:
                self.kicking = True
                self.hasKicked =True
            elif dis-bal.r-self.r < 5:  # Rê bóng nếu không đá
                vertical *= 0.8
                horizontal *= 0.8

        if not self.kicking:
            if self.kcd <= 0:
                self.hasKicked = False
            else:
                self.kcd -= 1
            self.kicking = False

        if self.kicking:
            #print("KICKED")
            vertical *= 0.7
            horizontal *= 0.7

        if horizontal != 0 and vertical != 0:
            vertical /= 1.41421356237
            horizontal /= 1.41421356237


        target_vx = horizontal * 10.5
        target_vy = vertical * 10.5
        self.vx = (self.vx * 0.6 + target_vx * 0.4+(0.03*botlv)*bal.vx)*(1.32+self.isbot*0.02)
        self.vy = (self.vy * 0.6 + target_vy * 0.4+(0.03*botlv)*bal.vy)*(1.32+self.isbot*0.02)
        self.vx *= 1.03
        self.vy *= 1.03

class Ball(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.immune = False
        self.slow = False
        self.particles = []  # Thêm dòng này để khởi tạo danh sách particle
        self.lastShotDirection = pygame.math.Vector2(0, 0)
        self.mass = 15
        self.color = color
        self.isDirectShotEffect = False
        self.directShotEffectTimer = 0
        self.besteal = None
        physicsEngine.ballList.append(self)  # Di chuyển dòng này xuống cuối nếu cần
    def upd(self):
        for particle in self.particles[:]:  # Sao chép danh sách để tránh lỗi khi xóa
            
            particle.lifetime -= 1
            if particle.lifetime <= 0:
                self.particles.remove(particle)
class Particle(object):
    def __init__(self, x, y, vx, vy, lifetime, color, size, shape="circle"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime  # Thời gian sống của particle (frame)
        self.color = color  # Màu sắc
        self.size = size  # Kích thước
        self.shape = shape
class Post(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        
        self.color = color
        physicsEngine.postList.append(self)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        physicsEngine.pointList.append(self)

class Wall(object):
    #A * x + B * y + C = 0
    def __init__(self, a, b, c):
        self.A = a
        self.B = b
        self.C = c

        physicsEngine.wallList.append(self)

class Line(object):
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1

        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.lineList.append(self)

class VisualLine(object):
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.visualLineList.append(self)

class Goal(object):
    def __init__(self, team, x1, y1, x2, y2):
        self.team = team
        self.score = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1

        physicsEngine.goalList.append(self)

class Arc(object):
    def __init__(self, x, y, r, a0, a, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a

        self.color = color
        self.width = width
        self.visible = visible

        self.point1 = Point( x + r * math.cos(a0), y - r * math.sin(a0))
        self.point2 = Point( x + r * math.cos(a), y - r * math.sin(a))
        
        physicsEngine.arcList.append(self)

class KickoffPoint(object):
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        
        physicsEngine.kickoffPointList.append(self)

class KickoffLine(object):
    def __init__(self, x1, y1, x2, y2, team, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1
        self.team = team
        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.kickoffLineList.append(self)     

class KickoffArc(object):
    def __init__(self, x, y, r, a0, a, team, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a

        self.point1 = KickoffPoint( x + r * math.cos(a0), y - r * math.sin(a0), team)
        self.point2 = KickoffPoint( x + r * math.cos(a), y - r * math.sin(a), team)

        self.team = team
        self.color = color
        self.width = width
        self.visible = visible
        
        physicsEngine.kickoffArcList.append(self)
