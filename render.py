import pygame
import menu
import physicsEngine
from constants import *
import random
import math

pygame.init()  # Giữ nguyên
background_image = None
logo = None

WIDTH = 1600
HEIGHT = 900

player_red_image = None
player_blue_image = None
blue_lock_logo = None
boti = []

# Danh sách ảnh chiêu thức (khởi tạo rỗng)
skill_images = {
    "nagi_dash":None,
    "nagi_magnet":None,
    "isagi_flow":None,
    "isagi_direct":None,
    "bachira_samba":None,
    "bachira_monster":None,
    "sae_magical":None,
    "sae_perfect":None,
    "barou_dribbling":None,
    "barou_king":None,
    "kunigami_block":None,
    "kunigami_wild":None,
    "lorenzo_ace":None,
    "lorenzo_zombie":None,
    "kaiser_impact":None,
    "kaiser_emperor":None,
    "rin_curve":None,
    "rin_opposite":None

}

# Mapping từ avatar sang tên nhân vật
avatar_to_name = {
    "./assets/images/Nagi.png": "Nagi",
    "./assets/images/Isagi.png": "Isagi",
    "./assets/images/Bachira.png": "Bachira",
    "./assets/images/Sae.png": "Sae",
    "./assets/images/Barou.png": "Barou",
    "./assets/images/Kunigami.png": "Kunigami",
    "./assets/images/Lorenzo.png": "Lorenzo",
    "./assets/images/Kaiser.png": "Kaiser",
    "./assets/images/Rin.png": "Rin"
}

# Hàm khởi tạo ảnh chiêu thức
def load_skill_images():
    try:
        skill_images["rin_curve"] = pygame.image.load("./assets/skills/rin_curve.png").convert_alpha()
        print("Loaded rin_curve.png:", skill_images["rin_curve"] is not None)
    except Exception as e:
        print(f"Error loading rin_curve.png: {e}")
    try:
        skill_images["rin_opposite"] = pygame.image.load("./assets/skills/rin_opposite.png").convert_alpha()
        print("Loaded rin_opposite.png:", skill_images["rin_opposite"] is not None)
    except Exception as e:
        print(f"Error loading rin_opposite.png: {e}")
    try:
        skill_images["nagi_dash"] = pygame.image.load("./assets/skills/nagi_dash.png").convert_alpha()
        print("Loaded nagi_dash.png:", skill_images["nagi_dash"] is not None)
    except Exception as e:
        print(f"Error loading nagi_dash.png: {e}")
    skill_images["nagi_magnet"] = pygame.image.load("./assets/skills/nagi_magnet.png").convert_alpha()
    skill_images["isagi_flow"] = pygame.image.load("./assets/skills/isagi_flow.png").convert_alpha()
    skill_images["isagi_direct"] = pygame.image.load("./assets/skills/isagi_direct.png").convert_alpha()
    skill_images["bachira_samba"] = pygame.image.load("./assets/skills/bachira_samba.png").convert_alpha()
    skill_images["bachira_monster"] = pygame.image.load("./assets/skills/bachira_monster.png").convert_alpha()
    skill_images["sae_magical"] = pygame.image.load("./assets/skills/sae_magical.png").convert_alpha()
    skill_images["sae_perfect"] = pygame.image.load("./assets/skills/sae_perfect.png").convert_alpha()
    skill_images["barou_dribbling"] = pygame.image.load("./assets/skills/barou_dribbling.png").convert_alpha()
    skill_images["barou_king"] = pygame.image.load("./assets/skills/barou_king.png").convert_alpha()
    skill_images["kunigami_block"] = pygame.image.load("./assets/skills/kunigami_block.png").convert_alpha()
    skill_images["kunigami_wild"] = pygame.image.load("./assets/skills/kunigami_wild.png").convert_alpha()
    skill_images["lorenzo_ace"] = pygame.image.load("./assets/skills/lorenzo_ace_eater.png").convert_alpha()
    skill_images["lorenzo_zombie"] = pygame.image.load("./assets/skills/lorenzo_zombie.png").convert_alpha()
    skill_images["kaiser_emperor"] = pygame.image.load("./assets/skills/kaiser_emperor_flow.png").convert_alpha()
    skill_images["kaiser_impact"] = pygame.image.load("./assets/skills/kaiser_kaiser_impact.png").convert_alpha()
def wrap_text(text, font, max_width):
    """Tách văn bản thành nhiều dòng dựa trên chiều rộng tối đa."""
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    
    if current_line:
        lines.append(current_line.strip())
    
    return lines

def init_images():
    """Khởi tạo các hình ảnh cần thiết cho game"""
    global player_red_image, player_blue_image, characterLargeImages, characterSmallImages, blue_lock_logo
    player_red_image = pygame.image.load("./assets/images/Barou.png").convert_alpha()
    player_blue_image = pygame.image.load("./assets/images/Isagi.png").convert_alpha()
    characterLargeImages = {path: pygame.image.load(path).convert_alpha() for path in menu.characterImages}
    characterSmallImages = characterLargeImages
    
    # Tải và resize logo Blue Lock với debug chi tiết
    try:
        logo_path = "./assets/images/blue_lock_logo.png"
        blue_lock_logo = pygame.image.load(logo_path).convert_alpha()
        blue_lock_logo = pygame.transform.scale(blue_lock_logo, (400, 250))
        print("Blue Lock logo loaded successfully, size:", blue_lock_logo.get_size())
    except FileNotFoundError:
        print(f"Error: File '{logo_path}' not found. Please check the file path.")
        blue_lock_logo = None
    except pygame.error as e:
        print(f"Error loading '{logo_path}': {e}. File may be corrupted or not a valid image.")
        blue_lock_logo = None
    except Exception as e:
        print(f"Unexpected error loading '{logo_path}': {e}")
        blue_lock_logo = None
    load_skill_images()

def drawButton(window, button):
    if not button.visible:
        return
    if button.section == menu.gameSection or button == menu.tutorialButton:
        if button.isPressed:
            pygame.draw.rect(window, button.colorPressed, (button.x, button.y, button.w, button.h))
        elif button.isOver:
            pygame.draw.rect(window, button.colorOver, (button.x, button.y, button.w, button.h))
        else:
            pygame.draw.rect(window, button.color, (button.x, button.y, button.w, button.h))

        if isinstance(button.argument, str) and button.argument == "image1":
            img_path = menu.characterImages[menu.currentCharacterIndex]
            if img_path in characterLargeImages:
                image = characterLargeImages[img_path]
                scaled_image = pygame.transform.scale(image, (button.w, button.h))
                window.blit(scaled_image, (button.x, button.y))
            else:
                print(f"Error: Image {img_path} not loaded")
                image = player_blue_image  # Fallback
                scaled_image = pygame.transform.scale(image, (button.w, button.h))
                window.blit(scaled_image, (button.x, button.y))
        else:
            # Kiểm tra nếu là characterDescButton
            if button == menu.characterDescButton:
                # Tách văn bản thành nhiều dòng
                lines = wrap_text(button.string, button.font, button.w)
                labels = [button.font.render(line, True, button.textColor) for line in lines]
                line_height = button.font.get_height()
                total_height = len(labels) * line_height
                start_y = button.y + (button.h - total_height) / 2  # Căn giữa theo chiều dọc
                for i, label in enumerate(labels):
                    rect = label.get_rect(center=(button.x + button.w / 2, start_y + i * line_height))
                    if button.alignLeft:
                        rect.left = button.x + 5
                    window.blit(label, rect.topleft)
            else:
                # Vẽ bình thường cho các nút khác
                window.blit(button.label, button.label_rect)

def drawPlayerBar(window, bar):
    """Vẽ thanh người chơi trong lobby, bao gồm biểu tượng bot nếu có"""
    if menu.gameSection == 1:
        if bar.isOver:
            color = bar.colorOver
        else:
            color = bar.color
        pygame.draw.rect(window, color, (bar.x, bar.y, bar.w, bar.h))
        window.blit(bar.label, bar.label_rect)
        if bar.player.isbot > 0:
            icon = boti[bar.player.isbot - 1]
            window.blit(icon, (bar.x + bar.w - icon.get_rect().size[0] / 2 - 9, bar.y + bar.h - icon.get_rect().size[1] / 2 - 9))

def drawDropdownItem(window, item):
    """Vẽ các mục trong dropdown list"""
    if menu.isDropdownListActive:
        if item == menu.dropdownSelectedItem:
            pygame.draw.rect(window, item.colorOver, (item.x, item.y, item.w, item.h))
        else:
            pygame.draw.rect(window, item.color, (item.x, item.y, item.w, item.h))
        window.blit(item.label, item.label_rect)

def drawPlayer(window, x, y, zoom, player):
    # Kiểm tra và thêm các thuộc tính nếu thiếu
    if not hasattr(player, 'isDashing'):
        player.isDashing = False
    if not hasattr(player, 'isShooting'):
        player.isShooting = False
    if not hasattr(player, 'isShootDelay'):
        player.isShootDelay = False
    if not hasattr(player, 'isFlowState'):
        player.isFlowState = False
    if not hasattr(player, 'isDirectShot'):
        player.isDirectShot = False
    if not hasattr(player, 'isSambaDance'):
        player.isSambaDance = False
    if not hasattr(player, 'isFreeNutmeg'):
        player.isFreeNutmeg = False
    if not hasattr(player, 'nutmegFreezeTimer'):
        player.nutmegFreezeTimer = 0
    if not hasattr(player, 'isMagicalTurn'):
        player.isMagicalTurn = False
    if not hasattr(player, 'isPerfectShot'):
        player.isPerfectShot = False
    if not hasattr(player, 'isKingShot'):
        player.isKingShot = False
    if not hasattr(player, 'isDribblingLord'):
        player.isDribblingLord = False
    if not hasattr(player, 'isBodyBlock'):
        player.isBodyBlock = False
    if not hasattr(player, 'isWildShot'):
        player.isWildShot = False
    if not hasattr(player, 'isAceEater'):
        player.isAceEater = False
    if not hasattr(player, 'isZombieDribbling'):
        player.isZombieDribbling = False
    if not hasattr(player, 'emperor_flow_active'):
        player.emperor_flow_active = False
    if not hasattr(player, 'kaiser_impact_active'):
        player.kaiser_impact_active = False
    if not hasattr(player, 'isOppositeDirection'):
        player.isOppositeDirection = False
    if not hasattr(player, 'OppositeDirectionTimer'):
        player.OppositeDirectionTimer = 0
    if not hasattr(player, 'skill_image'):  # Add this check
        player.skill_image = None
    if not hasattr(player, 'skill_image_timer'):  # Add this check
        player.skill_image_timer = 0

    # Rest of the function remains unchanged
    player_radius = int(player.r * zoom)
    player_pos = (int((player.x - x) * zoom), int((player.y - y) * zoom))
    
    # Khởi tạo hình ảnh nhân vật trước
    player_radius = int(player.r * zoom)
    player_pos = (int((player.x - x) * zoom), int((player.y - y) * zoom))
    inner_diameter = int((player.r - 3) * 2 * zoom)
    if hasattr(player, 'avatar') and player.avatar in characterLargeImages:
        scaled_image = pygame.transform.scale(characterLargeImages[player.avatar], (inner_diameter, inner_diameter))
    else:
        default_image = player_red_image if player.team == "RED" else player_blue_image
        scaled_image = pygame.transform.scale(default_image, (inner_diameter, inner_diameter))
    img_rect = scaled_image.get_rect(center=player_pos)
    if hasattr(player, 'avatar') and player.avatar == "./assets/images/Lorenzo.png":
        zomsurf = pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        zomsurf.set_alpha(25)
        zcolor = [(166, 36, 218,75),(191, 28, 202,75),(0,0,0,75)]
        for particle in player.particles:

            xp = 25*random.uniform(-1,1) if player.isZombieDribbling else 0
            yp = 25*random.uniform(-1,1) if player.isZombieDribbling else 0
            particle_pos = (
                int((particle.x - x +xp) * zoom),
                int((particle.y - y +yp) * zoom)
            )
            if player.isZombieDribbling:
                pygame.draw.circle(
                    window, 
                    random.choice(zcolor),  # Truy cập trực tiếp particle.color
                    particle_pos, 
                    int(particle.size* 1.2* zoom)
                )
            else:
                pygame.draw.circle(
                    window, 
                    particle.color,  # Truy cập trực tiếp particle.color
                    particle_pos, 
                    int(particle.size * zoom)
                )
         
    if hasattr(player, 'avatar') and not player.isZombieDribbling:
        for particle in player.particles:
            particle_pos = (
                int((particle.x - x) * zoom),
                int((particle.y - y) * zoom)
            )
            if particle.shape == "triangle":
                points = [
                    (particle_pos[0], particle_pos[1] - particle.size * zoom),
                    (particle_pos[0] - particle.size * zoom * 0.87, particle_pos[1] + particle.size * zoom * 0.5),
                    (particle_pos[0] + particle.size * zoom * 0.87, particle_pos[1] + particle.size * zoom * 0.5)
                ]
                pygame.draw.polygon(window, particle.color, points)
            else:
                pygame.draw.circle(window, particle.color, particle_pos, int(particle.size * zoom))
    # Vẽ ảnh chiêu thức trên đầu nhân vật
    if player.skill_image is not None:
        skill_img_size = (int(50 * zoom), int(50 * zoom))
        scaled_skill_img = pygame.transform.scale(skill_images[player.skill_image], skill_img_size)
        skill_img_pos = (
            int((player.x - x) * zoom - skill_img_size[0] / 2),
            int((player.y - y - player.r - 20) * zoom - skill_img_size[1])
        )
        window.blit(scaled_skill_img, skill_img_pos)
    #Rin dư ảnh

    if player.isOppositeDirection and player.avatar == "./assets/images/Rin.png":
        player.skill_image = "rin_opposite"  # Gán hình ảnh chiêu thức
        player.skill_image_timer = 60  # Hiển thị trong 60 frame (có thể điều chỉnh)
        for i, ix in enumerate(player.ODimagex):
            area = pygame.Rect((int((ix - x) * zoom), int((player.ODimagey[i] - y) * zoom)), (0, 0)).inflate((player_radius * 2, player_radius * 2))
            layer = pygame.Surface((int((ix - x) * zoom), int((player.ODimagey[i] - y) * zoom)), pygame.SRCALPHA)
            layer.set_alpha(50 * (player.AIlv[i] + 1))
            c1 = pygame.draw.circle(layer, (9, 167, 206), (0 + player_radius, 0 + player_radius), player_radius, 0)
            c2 = pygame.draw.circle(layer, (38, 228, 168), (0 + player_radius, 0 + player_radius), int((player.r - 3) * zoom), 0)
            window.blit(layer, area)
        for _ in range(25):
            minornot = [-1, 1]
            particle_pos = (player_radius + 5) ** 2
            particle_radius = random.random() * particle_pos
            particle_x = player_pos[0] + random.choice(minornot) * math.sqrt(particle_radius) * (random.random() + 0.5) + 3.5
            particle_y = player_pos[1] + random.choice(minornot) * math.sqrt(particle_pos - particle_radius) * (random.random() + 0.5) + 3.5
            alpha_color = (38, 228, 168, random.randint(25, 75))  # Trail xanh dương
            pygame.draw.rect(window, alpha_color, (particle_x - 3, particle_y - 8, 6, 16))
        for _ in range(20):
            minornot = [-1, 1]
            particle_pos = (player_radius + 5) ** 2
            particle_radius = random.random() * particle_pos
            particle_x = player_pos[0] + random.choice(minornot) * math.sqrt(particle_radius) * (random.random() + 0.5) + 3.5
            particle_y = player_pos[1] + random.choice(minornot) * math.sqrt(particle_pos - particle_radius) * (random.random() + 0.5) + 3.5
            alpha_color = (9, 167, 206, random.randint(25, 75))  # Trail xanh dương
            pygame.draw.rect(window, alpha_color, (particle_x - 3, particle_y - 10, 6, 20))   
    # Body Block (Kunigami)
    if player.isBodyBlock and player.avatar == "./assets/images/Kunigami.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Hiệu ứng lửa cháy bùng nổ
        for i in range(3):
            aura_radius = player_radius + i * 15 * zoom
            alpha = int(150 * (1 - i / 3))  # Mờ dần ra ngoài
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 69, 0, alpha), (aura_radius, aura_radius), int(aura_radius))
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))
        # Particle rực lửa cam
        for _ in range(50):
            particle_x = player_pos[0] + random.randint(-player_radius - 20, player_radius + 20)
            particle_y = player_pos[1] + random.randint(-player_radius - 20, player_radius + 20)
            color = (255, 69, 0) if random.random() < 0.7 else (255, 165, 0)
            size = random.randint(3, 6) * zoom
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)

    # Wild Shot (Kunigami)
    elif player.isWildShot and player.avatar == "./assets/images/Kunigami.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura cam rực lửa và khói
        for i in range(3):
            aura_radius = player_radius + i * 12 * zoom
            alpha = int(120 * (1 - i / 3))
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 69, 0, alpha), (aura_radius, aura_radius), int(aura_radius))
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))
        # Particle tam giác 3 màu
        for _ in range(60):
            particle_x = player_pos[0] + random.randint(-player_radius - 30, player_radius + 30)
            particle_y = player_pos[1] + random.randint(-player_radius - 30, player_radius + 30)
            # Chọn ngẫu nhiên 1 trong 3 màu
            color = random.choice([(255, 215, 0), (255, 69, 0), (0, 0, 0)])  # Vàng, cam, đen
            size = random.randint(5, 10) * zoom  # Kích thước tam giác
            # Vẽ tam giác
            points = [
                (particle_x, particle_y - size),  # Đỉnh trên
                (particle_x - size * 0.866, particle_y + size * 0.5),  # Đáy trái
                (particle_x + size * 0.866, particle_y + size * 0.5)   # Đáy phải
            ]
            pygame.draw.polygon(window, color, points)
    # Emperor Flow (Kaiser)
    if player.emperor_flow_active and player.avatar == "./assets/images/Kaiser.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura cyan và trắng
        for i in range(3):
            aura_radius = player_radius + i * 12 * zoom
            alpha = int(120 * (1 - i / 3))
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (0, 255, 255, alpha), (aura_radius, aura_radius), int(aura_radius))
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))
        # Particle tam giác cyan và trắng
        for _ in range(60):
            particle_x = player_pos[0] + random.randint(-player_radius - 30, player_radius + 30)
            particle_y = player_pos[1] + random.randint(-player_radius - 30, player_radius + 30)
            color = random.choice([(0, 255, 255), (0, 200, 255), (255, 255, 255)])  # Cyan, xanh trắng, trắng
            size = random.randint(3, 5) * zoom
            points = [
                (particle_x, particle_y - size),
                (particle_x - size * 0.866, particle_y + size * 0.5),
                (particle_x + size * 0.866, particle_y + size * 0.5)
            ]
            pygame.draw.polygon(window, color, points)

    # Kaiser Impact (Kaiser)
    elif player.kaiser_impact_active and player.avatar == "./assets/images/Kaiser.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura tím và cyan
        for i in range(3):
            aura_radius = player_radius + i * 15 * zoom
            alpha = int(150 * (1 - i / 3))
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (150, 0, 255, alpha), (aura_radius, aura_radius), int(aura_radius))
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))
        # Particle tam giác tím, cyan và trắng
        for _ in range(80):
            particle_x = player_pos[0] + random.randint(-player_radius - 40, player_radius + 40)
            particle_y = player_pos[1] + random.randint(-player_radius - 40, player_radius + 40)
            color = random.choice([(0, 255, 255), (255, 255, 255), (150, 0, 255)])  # Cyan, trắng, tím
            size = random.randint(6, 10) * zoom
            points = [
                (particle_x, particle_y - size),
                (particle_x - size * 0.866, particle_y + size * 0.5),
                (particle_x + size * 0.866, particle_y + size * 0.5)
            ]
            pygame.draw.polygon(window, color, points)
    elif player.isAceEater and player.avatar == "./assets/images/Lorenzo.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura tím-đen gradient galaxy
        for i in range(4):
            aura_radius = player_radius + i * 15 * zoom
            alpha = int(180 * (1 - i / 4))  # Mờ dần ra ngoài
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (75, 0, 130, alpha), (aura_radius, aura_radius), int(aura_radius))  # Tím galaxy
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))
        # Particle tím-đen xoay vòng
        for _ in range(80):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.randint(player_radius, player_radius + 40) * zoom
            particle_x = player_pos[0] + math.cos(angle) * radius
            particle_y = player_pos[1] + math.sin(angle) * radius
            color = (75, 0, 130) if random.random() < 0.6 else (0, 0, 0)  # Tím và đen xen kẽ
            size = random.randint(3, 7) * zoom
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size))
        # Hiệu ứng rung lắc và xoay vòng
        if player.aceEaterPhase > 0:
            shake_offset = (random.randint(-5, 5) * zoom, random.randint(-5, 5) * zoom)
            window.blit(scaled_image, (img_rect.topleft[0] + shake_offset[0], img_rect.topleft[1] + shake_offset[1]))
    elif player.isZombieDribbling and player.avatar == "./assets/images/Lorenzo.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura tím-đen gradient dạng đường thẳng
        
        pnts = []
        zomcolor = [(75, 0, 130),(0, 0, 0)]
        for _ in range (7):
            pnts.append([random.uniform(-0.8,0.8),random.choice(zomcolor)])
        for particl in player.particles:
            pvx = particl.vy *-1*player_radius
            pvy = particl.vx *1*player_radius
            for i in range(7):
                pygame.draw.circle(window,pnts[i][1],(int(particl.x+pnts[i][0]*pvx-x)*zoom,int(particl.y+pnts[i][0]*pvy-y)*zoom),1)
                pnts[i][0]+= -0.1 if (pnts[i][0]>0.7) or(random.random()>0.5 and pnts[i][0]>=-0.7)  else 0.1
            # Particle tím-đen dày đặc dạng đường thẳng
    #    for _ in range(100):
    #        offset = random.randint(-player_radius - 50, player_radius + 50) * zoom
    #        particle_x = player_pos[0] + direction.x * offset + perpendicular.x * random.uniform(-10, 10) * zoom
    #        particle_y = player_pos[1] + direction.y * offset + perpendicular.y * random.uniform(-10, 10) * zoom
    #        color = (75, 0, 130) if random.random() < 0.7 else (0, 0, 0)
    #        size = random.randint(4, 8) * zoom
    #        pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size))
        # Hiệu ứng rung lắc
        shake_offset = (random.randint(-3, 3) * zoom, random.randint(-3, 3) * zoom)

        window.blit(scaled_image, (img_rect.topleft[0] + shake_offset[0], img_rect.topleft[1] + shake_offset[1]))
    #DribblingLord
    if player.isDribblingLord and player.avatar == "./assets/images/Barou.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Hiệu ứng tia sét đỏ đen
        direction = pygame.math.Vector2(player.vx, player.vy).normalize()
        perpendicular = pygame.math.Vector2(-direction.y, direction.x)
        for i in range(16):  # 16 tia sét
            offset = i * 15 * zoom
            length = random.randint(20, 40) * zoom
            start_x = player_pos[0] - direction.x * offset
            start_y = player_pos[1] - direction.y * offset
            end_x = start_x + perpendicular.x * length * random.choice([-1, 1])
            end_y = start_y + perpendicular.y * length * random.choice([-1, 1])
            color = (255, 0, 0) if i % 2 == 0 else (0, 0, 0)  # Đỏ và đen xen kẽ
            pygame.draw.line(window, color, (start_x, start_y), (end_x, end_y), int(4 * zoom))

    # KingShot
    elif player.isKingShot and player.avatar == "./assets/images/Barou.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Hiệu ứng sư tử gầm và tia sét
        for _ in range(80):
            particle_x = player_pos[0] + random.randint(-player_radius - 40, player_radius + 40)
            particle_y = player_pos[1] + random.randint(-player_radius - 40, player_radius + 40)
            color = (255, 0, 0) if random.random() < 0.5 else (0, 0, 0)
            size = random.randint(4, 6) * zoom
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
        # Tia sét bao quanh
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(player_radius, player_radius * 2)
            trail_x = player_pos[0] + math.cos(angle) * length
            trail_y = player_pos[1] + math.sin(angle) * length
            pygame.draw.line(window, (255, 0, 0), player_pos, (int(trail_x), int(trail_y)), int(3 * zoom))
    # Magical Turn
    if player.isMagicalTurn and player.avatar == "./assets/images/Sae.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # 1. Aura quanh Sae
        for i in range(3):
            aura_radius = player_radius + i * 12 * zoom
            alpha = int(120 * (1 - i / 3))  # Mờ dần ra ngoài, sáng hơn
            surface = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 20, 147, alpha), (aura_radius, aura_radius), int(aura_radius))
            window.blit(surface, (int(player_pos[0] - aura_radius), int(player_pos[1] - aura_radius)))

        # 2. Vệt di chuyển (Trail) nâng cấp
        for i in range(15):  # Tăng số vệt từ 10 lên 15
            offset = i * 8 * zoom  # Giảm khoảng cách giữa các vệt
            alpha = int(255 * (1 - i / 15))
            trail_pos = (
                int(player_pos[0] - player.vx * 0.1 * i * zoom),
                int(player_pos[1] - player.vy * 0.1 * i * zoom)
            )
            surface = pygame.Surface((player_radius * 2, player_radius * 2), pygame.SRCALPHA)
            color = (255, 20, 147) if i % 2 == 0 else (148, 0, 211)  # Xen kẽ hồng và đỏ tím
            pygame.draw.circle(surface, (color[0], color[1], color[2], alpha), (player_radius, player_radius), player_radius)
            window.blit(surface, (trail_pos[0] - player_radius, trail_pos[1] - player_radius))

        # 3. Ánh sáng chữ X (X cross pink and red lights)
        for i in range(2):  # Hai nhánh chữ X
            length = 70 * zoom  # Chiều dài nhánh
            thickness = int(6 * zoom)  # Độ dày
            color = (255, 20, 147) if i == 0 else (148, 0, 211)  # Hồng và đỏ tím
            # Nhánh 1: 45 độ
            start_x1 = player_pos[0] - length * math.cos(math.radians(45))
            start_y1 = player_pos[1] - length * math.sin(math.radians(45))
            end_x1 = player_pos[0] + length * math.cos(math.radians(45))
            end_y1 = player_pos[1] + length * math.sin(math.radians(45))
            pygame.draw.line(window, color, (start_x1, start_y1), (end_x1, end_y1), thickness)
            # Nhánh 2: 135 độ
            start_x2 = player_pos[0] - length * math.cos(math.radians(135))
            start_y2 = player_pos[1] - length * math.sin(math.radians(135))
            end_x2 = player_pos[0] + length * math.cos(math.radians(135))
            end_y2 = player_pos[1] + length * math.sin(math.radians(135))
            pygame.draw.line(window, color, (start_x2, start_y2), (end_x2, end_y2), thickness)

        # 4. Tia sét (Lightning)
        direction = pygame.math.Vector2(player.vx, player.vy)
        if direction.length() > 0:  # Kiểm tra để tránh lỗi normalize vector (0, 0)
            direction.normalize_ip()
            perpendicular = pygame.math.Vector2(-direction.y, direction.x)
            for i in range(12):  # 12 tia sét
                offset = i * 8 * zoom
                length = random.randint(25, 60) * zoom  # Chiều dài ngẫu nhiên
                start_x = player_pos[0] - direction.x * offset
                start_y = player_pos[1] - direction.y * offset
                end_x = start_x + perpendicular.x * length * random.choice([-1, 1])
                end_y = start_y + perpendicular.y * length * random.choice([-1, 1])
                color = (255, 20, 147) if i % 2 == 0 else (148, 0, 211)  # Xen kẽ hồng và đỏ tím
                pygame.draw.line(window, color, (start_x, start_y), (end_x, end_y), int(4 * zoom))

        # 5. Particle ngẫu nhiên
        for _ in range(80):  # Tăng từ 50 lên 80
            particle_x = player_pos[0] + random.randint(-player_radius - 50, player_radius + 50)
            particle_y = player_pos[1] + random.randint(-player_radius - 50, player_radius + 50)
            color = (255, 20, 147) if random.random() < 0.5 else (148, 0, 211)  # Hồng và đỏ tím
            size = random.randint(3, 7) * zoom  # Tăng kích thước particle
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
    if player.kicking or player.hasKicked:
        pygame.draw.circle(window, WHITE, player_pos, player_radius, 0)
        if player.hasKicked:
            player.hasKicked = False
    elif player.isDashing and player.avatar == "./assets/images/Nagi.png":
        pygame.draw.circle(window, (255, 255, 0), player_pos, player_radius + 5, 2)
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
    elif (player.isShooting or player.isShootDelay) and player.avatar == "./assets/images/Nagi.png":
        pygame.draw.circle(window, (255, 0, 0), player_pos, player_radius + 5, 2)
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        for _ in range(30):
            particle_x = player_pos[0] + random.randint(-player_radius, player_radius)
            particle_y = player_pos[1] + random.randint(-player_radius, player_radius)
            pygame.draw.circle(window, (0, 191, 255), (int(particle_x), int(particle_y)), int(3 * zoom), 0)
    # Perfect Shot
    elif player.isPerfectShot and player.avatar == "./assets/images/Sae.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Aura đen và hồng
        for _ in range(60):
            particle_x = player_pos[0] + random.randint(-player_radius - 30, player_radius + 30)
            particle_y = player_pos[1] + random.randint(-player_radius - 30, player_radius + 30)
            color = (0, 0, 0) if random.random() < 0.5 else (255, 20, 147)  # Đen và hồng đậm
            size = random.randint(3, 5) * zoom
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
        # Lửa hồng rực rỡ
        for _ in range(30):
            particle_x = player_pos[0] + random.randint(-player_radius - 15, player_radius + 15)
            particle_y = player_pos[1] + random.randint(-player_radius - 15, player_radius + 15)
            alpha_color = (255, 69, 0, 150)  # Lửa đỏ cam
            surface = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(surface, alpha_color, (4, 4), 4)
            window.blit(surface, (int(particle_x), int(particle_y)))
    elif player.isFlowState and player.avatar == "./assets/images/Isagi.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        for _ in range(20):
            particle_x = player_pos[0] + random.randint(-player_radius - 10, player_radius + 10)
            particle_y = player_pos[1] + random.randint(-player_radius - 10, player_radius + 10)
            color = (0, 255, 0) if random.random() < 0.5 else WHITE
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(2 * zoom), 0)
    elif player.isSambaDance and player.avatar == "./assets/images/Bachira.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Hiệu ứng Samba Dance: Particle sắc màu rực rỡ
        for _ in range(60):  # Tăng lên 60 particle
            particle_x = player_pos[0] + random.randint(-player_radius - 25, player_radius + 25)  # Phạm vi rộng hơn
            particle_y = player_pos[1] + random.randint(-player_radius - 25, player_radius + 25)
            color = random.choice([(255, 0, 0), (255, 255, 0), (0, 255, 0), (255, 105, 180), (255, 20, 147)])  # Thêm hồng đậm
            size = random.randint(3, 5) * zoom  # Kích thước particle ngẫu nhiên
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
    elif player.isFreeNutmeg and player.avatar == "./assets/images/Bachira.png":
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        # Hiệu ứng Free Nutmeg: Aura xám và cam với khói/sương mù
        for _ in range(50):  # Tăng lên 50 particle
            particle_x = player_pos[0] + random.randint(-player_radius - 20, player_radius + 20)
            particle_y = player_pos[1] + random.randint(-player_radius - 20, player_radius + 20)
            color = (150, 150, 150) if random.random() < 0.5 else (255, 165, 0)
            size = random.randint(2, 4) * zoom
            pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
        # Thêm hiệu ứng khói mờ
        for _ in range(25):
            particle_x = player_pos[0] + random.randint(-player_radius - 25, player_radius + 25)
            particle_y = player_pos[1] + random.randint(-player_radius - 25, player_radius + 25)
            alpha_color = (150, 150, 150, 120) if random.random() < 0.5 else (255, 165, 0, 120)
            surface = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(surface, alpha_color, (3, 3), 3)
            window.blit(surface, (int(particle_x), int(particle_y)))
    elif player.nutmegFreezeTimer > 0:  # Đối thủ bị đóng băng
        pygame.draw.circle(window, (100, 100, 100), player_pos, player_radius + 5, 2)
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        for _ in range(20):  # Tăng lên 20 particle
            particle_x = player_pos[0] + random.randint(-player_radius - 10, player_radius + 10)
            particle_y = player_pos[1] + random.randint(-player_radius - 10, player_radius + 10)
            pygame.draw.circle(window, (150, 150, 150), (int(particle_x), int(particle_y)), int(2 * zoom), 0)
    elif player.isOppositeDirection and player.avatar == "./assets/images/Rin.png":

        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
        pygame.draw.circle(window, (14, 228, 111), player_pos, player_radius+5, 2)
    else:
        pygame.draw.circle(window, BLACK, player_pos, player_radius, 0)
    if player.team == "RED":
        pygame.draw.circle(window, PLAYER_RED, player_pos, int((player.r - 3) * zoom), 0)
    elif player.team == "BLUE":
        pygame.draw.circle(window, PLAYER_BLUE, player_pos, int((player.r - 3) * zoom), 0)
    #pygame.draw.line(window,GREEN,(int(player.x-x+player.vx*10)*zoom,int(player.y-y+player.vy*10)*zoom),(int(player.x-x+player.vx*20)*zoom,int(player.y-y+player.vy*20)*zoom)) #Vector hướng xanh lá
    img_rect = scaled_image.get_rect(center=player_pos)
    window.blit(scaled_image, img_rect.topleft)

def drawPlayerNick(window, x, y, zoom, player):
    """Vẽ tên người chơi trên sân"""
    font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", int(18 * zoom))
    label = font.render(player.nick, True, WHITE)
    window.blit(label, label.get_rect(center=((player.x - x) * zoom, (player.y - y + 40) * zoom)))

def drawBall(window, x, y, zoom, ball):
    ball_pos = (int((ball.x - x) * zoom), int((ball.y - y) * zoom))
    ball_radius = int(ball.r * zoom)
    for player in physicsEngine.playerList:
        if player.isCS and player.CSball == ball:
            basex = -ball.vy
            basey = ball.vx
            basedic = pygame.Vector2(basey,-basex).normalize()
            dic2 = pygame.Vector2(basex,basey).normalize()
            pygame.draw.polygon(window,(58, 186, 220),[(int(ball.x-x)*zoom+basedic.x*ball_radius*2,int(ball.y-y)*zoom+basedic.y*ball_radius*2),(int(ball.x-x)*zoom+ball_radius*dic2.x*2,int(ball.y-y)*zoom+ball_radius*dic2.y*2),(int(ball.x-x)*zoom-ball_radius*dic2.x*2,int(ball.y-y)*zoom-ball_radius*dic2.y*2)])           
            num = random.uniform(0,10)
            sumx = ball.vx + num*basex
            sumy = ball.vy + num*basey
            sumd = pygame.Vector2(sumx,sumy).normalize()
            suml =pygame.Vector2(sumd.y,-sumd.x).normalize()
            sumr =pygame.Vector2(-sumd.y,sumd.x).normalize()
            if num <=0:
                pygame.draw.polygon(window,random.choice([(7, 189, 238),(61, 234, 245),(58, 186, 220)]),[(int(ball.x-x)*zoom,int(ball.y-y)*zoom),(int(ball.x-x+ball_radius*(suml.x+sumd.x)*2)*zoom,int(ball.y-y+ball_radius*2*(suml.y+sumd.y))*zoom),(int(ball.x-x+ball_radius*(sumr.x+sumd.x))*zoom,int(ball.y-y+ball_radius*(sumr.y+sumd.y))*zoom)])
            else:
                pygame.draw.polygon(window,random.choice([(7, 189, 238),(61, 234, 245),(58, 186, 220)]),[(int(ball.x-x)*zoom,int(ball.y-y)*zoom),(int(ball.x-x+ball_radius*(suml.x+sumd.x))*zoom,int(ball.y-y+ball_radius*(suml.y+sumd.y))*zoom),(int(ball.x-x+ball_radius*(sumr.x+sumd.x)*2)*zoom,int(ball.y-y+ball_radius*(sumr.y+sumd.y)*2)*zoom)])
            basex = -ball.vy
            basey = ball.vx
            num = random.uniform(-10,0)
            sumx = ball.vx + num*basex
            sumy = ball.vy + num*basey
            sumd = pygame.Vector2(sumx,sumy).normalize()
            suml =pygame.Vector2(sumd.y,-sumd.x).normalize()
            sumr =pygame.Vector2(-sumd.y,sumd.x).normalize()
            if num <=0:
                pygame.draw.polygon(window,random.choice([(7, 189, 238),(61, 234, 245),(58, 186, 220)]),[(int(ball.x-x)*zoom,int(ball.y-y)*zoom),(int(ball.x-x+ball_radius*(suml.x+sumd.x)*1.5)*zoom,int(ball.y-y+ball_radius*1.5*(suml.y+sumd.y))*zoom),(int(ball.x-x+ball_radius*(sumr.x+sumd.x))*zoom,int(ball.y-y+ball_radius*(sumr.y+sumd.y))*zoom)])
            else:
                pygame.draw.polygon(window,random.choice([(7, 189, 238),(61, 234, 245),(58, 186, 220)]),[(int(ball.x-x)*zoom,int(ball.y-y)*zoom),(int(ball.x-x+ball_radius*(suml.x+sumd.x))*zoom,int(ball.y-y+ball_radius*(suml.y+sumd.y))*zoom),(int(ball.x-x+ball_radius*(sumr.x+sumd.x)*1.5)*zoom,int(ball.y-y+ball_radius*(sumr.y+sumd.y)*1.5)*zoom)])
            for p in ball.particles:
                px = -p.vy
                py = p.vx
                pdic = pygame.Vector2(px,py).normalize()
                for i in range(-p.lifetime//2,p.lifetime//2+1):
                    pygame.draw.circle(window, p.color, ((int((p.x - x+i*2*pdic.x) * zoom), int((p.y - y+i*2*pdic.y) * zoom))), random.randint(3,6)*zoom, 0)
#                pygame.draw.circle(window, part.color, ((int((part.x - x) * zoom), int((part.y - y) * zoom))), 3, 0)
#                    print(f"{i} {pdic} {abs(i-int(round(part.lifetime/12,0)/2))+0.5} {abs(i-int(round(part.lifetime/12,0)/2))-0.5}")
    pygame.draw.circle(window, BLACK, ball_pos, ball_radius, 0)
    pygame.draw.circle(window, ball.color, ball_pos, int((ball.r - 3) * zoom), 0)
    
    # Hiệu ứng KingShot trên bóng
    for player in physicsEngine.playerList:
        if player.isKingShot and player.kingShotTargetBall == ball and player.kingShotTimer <= 0:
            # Aura đỏ đen và xoáy knuckle ball
            for _ in range(40):
                particle_x = ball_pos[0] + random.randint(-ball_radius - 20, ball_radius + 20)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 20, ball_radius + 20)
                color = (255, 0, 0) if random.random() < 0.5 else (0, 0, 0)
                size = random.randint(2, 4) * zoom
                pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
            # Hiệu ứng xoáy
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(ball_radius, ball_radius * 3)
                trail_x = ball_pos[0] + math.cos(angle) * length
                trail_y = ball_pos[1] + math.sin(angle) * length
                pygame.draw.line(window, (255, 0, 0), ball_pos, (int(trail_x), int(trail_y)), int(2 * zoom))
            break
    # Hiệu ứng cho Perfect Shot
    for player in physicsEngine.playerList:
        if player.isPerfectShot and player.perfectShotTargetBall == ball:
            # Hiệu ứng xoáy siêu cong hồng và đỏ tím
            for i in range(20):
                angle = i * 0.5 + ball.directShotEffectTimer * 0.1  # Xoáy nhanh
                length = (ball_radius + i * 5) * zoom
                trail_x = ball_pos[0] + math.cos(angle) * length
                trail_y = ball_pos[1] + math.sin(angle) * length
                color = (255, 20, 147) if i % 2 == 0 else (148, 0, 211)  # Hồng và đỏ tím
                pygame.draw.line(window, color, ball_pos, (int(trail_x), int(trail_y)), int(4 * zoom))
            for _ in range(40):
                particle_x = ball_pos[0] + random.randint(-ball_radius * 3, ball_radius * 3)
                particle_y = ball_pos[1] + random.randint(-ball_radius * 3, ball_radius * 3)
                pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(3 * zoom), 0)
            break
    # Hiệu ứng Wild Shot trên bóng
    for player in physicsEngine.playerList:
        if player.isWildShot and player.wildShotTargetBall == ball and player.wildShotTimer <= 0:
            # Particle tam giác 3 màu xung quanh bóng
            for _ in range(40):
                particle_x = ball_pos[0] + random.randint(-ball_radius - 20, ball_radius + 20)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 20, ball_radius + 20)
                color = random.choice([(255, 215, 0), (255, 69, 0), (0, 0, 0)])  # Vàng, cam, đen
                size = random.randint(4, 8) * zoom
                points = [
                    (particle_x, particle_y - size),
                    (particle_x - size * 0.866, particle_y + size * 0.5),
                    (particle_x + size * 0.866, particle_y + size * 0.5)
                ]
                pygame.draw.polygon(window, color, points)
            # Đường lửa kéo dài với tam giác
            if ball.vx != 0 or ball.vy != 0:  # Kiểm tra vận tốc khác 0
                direction = pygame.math.Vector2(ball.vx, ball.vy).normalize()
                for i in range(20):
                    trail_x = ball_pos[0] - direction.x * i * 10 * zoom
                    trail_y = ball_pos[1] - direction.y * i * 10 * zoom
                    color = random.choice([(255, 215, 0), (255, 69, 0), (0, 0, 0)])  # 3 màu ngẫu nhiên
                    size = 3 * zoom
                    points = [
                        (trail_x, trail_y - size),
                        (trail_x - size * 0.866, trail_y + size * 0.5),
                        (trail_x + size * 0.866, trail_y + size * 0.5)
                    ]
                    pygame.draw.polygon(window, color, points)
            break
    # Hiệu ứng "xẹt xẹt" trắng cho Direct Shot
    if hasattr(ball, 'isDirectShotEffect') and ball.isDirectShotEffect:
        for _ in range(20):
            angle = random.uniform(0, 2 * math.pi)
            length = random.randint(ball_radius, ball_radius * 3)
            trail_x = ball_pos[0] + math.cos(angle) * length
            trail_y = ball_pos[1] + math.sin(angle) * length
            pygame.draw.line(window, WHITE, ball_pos, (int(trail_x), int(trail_y)), int(3 * zoom))
        for _ in range(25):
            particle_x = ball_pos[0] + random.randint(-ball_radius * 2, ball_radius * 2)
            particle_y = ball_pos[1] + random.randint(-ball_radius * 2, ball_radius * 2)
            pygame.draw.circle(window, WHITE, (int(particle_x), int(particle_y)), int(2 * zoom), 0)
    
    # Hiệu ứng Samba Dance cho bóng
    for player in physicsEngine.playerList:
        if player.isFreeNutmeg and player.nutmegTargetBall == ball:
            for _ in range(40):  # Tăng lên 40 particle
                particle_x = ball_pos[0] + random.randint(-ball_radius - 20, ball_radius + 20)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 20, ball_radius + 20)
                color = (150, 150, 150) if random.random() < 0.5 else (255, 165, 0)
                size = random.randint(2, 4) * zoom
                pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size), 0)
            # Thêm khói mờ cho bóng
            for _ in range(20):
                particle_x = ball_pos[0] + random.randint(-ball_radius - 25, ball_radius + 25)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 25, ball_radius + 25)
                alpha_color = (150, 150, 150, 120) if random.random() < 0.5 else (255, 165, 0, 120)
                surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                pygame.draw.circle(surface, alpha_color, (3, 3), 3)
                window.blit(surface, (int(particle_x), int(particle_y)))
            break
        # Hiệu ứng Free Nutmeg cho bóng
        if player.isFreeNutmeg and player.nutmegTargetBall == ball:
            for _ in range(20):
                particle_x = ball_pos[0] + random.randint(-ball_radius - 10, ball_radius + 10)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 10, ball_radius + 10)
                color = (150, 150, 150) if random.random() < 0.5 else (255, 165, 0)
                pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(2 * zoom), 0)
            break
        #lorenzo
        if player.isZombieDribbling and player.zombieDribblingBall == ball:
            # Particle tím-đen quanh bóng
            for _ in range(40):
                particle_x = ball_pos[0] + random.randint(-ball_radius - 20, ball_radius + 20)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 20, ball_radius + 20)
                color = (75, 0, 130) if random.random() < 0.7 else (0, 0, 0)
                size = random.randint(3, 5) * zoom
                pygame.draw.circle(window, color, (int(particle_x), int(particle_y)), int(size))
            break
        # Hiệu ứng Kaiser Impact trên bóng
        if player.kaiser_impact_active and player.avatar == "./assets/images/Kaiser.png":
            # Particle tam giác tím, cyan và trắng quanh bóng
            for _ in range(60):  # Tăng từ 40 lên 60 particle
                particle_x = ball_pos[0] + random.randint(-ball_radius - 30, ball_radius + 30)
                particle_y = ball_pos[1] + random.randint(-ball_radius - 30, ball_radius + 30)
                color = random.choice([(0, 255, 255), (255, 255, 255), (150, 0, 255)])  # Cyan, trắng, tím
                size = random.randint(6, 10) * zoom  # Tăng kích thước particle
                points = [
                    (particle_x, particle_y - size),
                    (particle_x - size * 0.866, particle_y + size * 0.5),
                    (particle_x + size * 0.866, particle_y + size * 0.5)
                ]
                pygame.draw.polygon(window, color, points)
            # Thêm đường xoáy mạnh
            for _ in range(20):
                angle = random.uniform(0, 2 * math.pi)
                length = random.randint(ball_radius, ball_radius * 3)
                trail_x = ball_pos[0] + math.cos(angle) * length
                trail_y = ball_pos[1] + math.sin(angle) * length
                pygame.draw.line(window, (150, 0, 255), ball_pos, (int(trail_x), int(trail_y)), int(4 * zoom))
            break
        

    
def drawPost(window, x, y, zoom, post):
    """Vẽ cột gôn trên sân"""
    pygame.draw.circle(window, BLACK, (int((post.x - x) * zoom), int((post.y - y) * zoom)), int(post.r * zoom), 0)
    pygame.draw.circle(window, post.color, (int((post.x - x) * zoom), int((post.y - y) * zoom)), int((post.r - 3) * zoom), 0)

def drawLine(window, x, y, zoom, line):
    """Vẽ các đường trên sân"""
    if line.visible:
        pygame.draw.line(window, line.color, [int((line.x1 - x) * zoom), int((line.y1 - y) * zoom)],
                         [int((line.x2 - x) * zoom), int((line.y2 - y) * zoom)], int(line.width * zoom))

def drawArc(window, x, y, zoom, arc):
    """Vẽ các cung tròn trên sân"""
    if arc.visible:
        pygame.draw.arc(window, arc.color, (int((arc.x - x - arc.r) * zoom), int((arc.y - y - arc.r) * zoom),
                                            int(2 * arc.r * zoom), int(2 * arc.r * zoom)), arc.a0, arc.a,
                        int(arc.width * zoom))

# render.py
def screenUpdate(window, x, y, zoom, physicObjects):
    """Cập nhật màn hình game, vẽ tất cả các thành phần"""
    window.fill(BACKGROUND_GREEN)
    bgW = int(background_image.get_rect().size[0] * zoom)
    bgH = int(background_image.get_rect().size[1] * zoom)
    bimg = pygame.transform.scale(background_image, (bgW, bgH))

    x -= (WIDTH / 2) / zoom
    y -= (HEIGHT / 2) / zoom

    x0 = int((-x * zoom) % bgW - bgW)
    y0 = int((-y * zoom) % bgH - bgH)

    for xb in range(x0, WIDTH, bgW):
        for yb in range(y0, HEIGHT, bgH):
            window.blit(bimg, (xb, yb))

    if physicObjects is not None:
        for line in physicObjects['lines']:
            drawLine(window, x, y, zoom, line)
        for visualLine in physicObjects['visualLines']:
            drawLine(window, x, y, zoom, visualLine)
        for kickoffLine in physicObjects['kickoffLines']:
            drawLine(window, x, y, zoom, kickoffLine)
        for arc in physicObjects['arcs']:
            drawArc(window, x, y, zoom, arc)
        for kickoffArc in physicObjects['kickoffArcs']:
            drawArc(window, x, y, zoom, kickoffArc)
        for player in physicObjects['players']:
            drawPlayer(window, x, y, zoom, player)
        # Vẽ particle cho bóng
        for ball in physicObjects['balls']:
            drawBall(window, x, y, zoom, ball)
        for post in physicObjects['posts']:
            drawPost(window, x, y, zoom, post)
        for player in physicObjects['players']:
            drawPlayerNick(window, x, y, zoom, player)

    for button in menu.buttonList:
        drawButton(window, button)
    for bar in menu.playerBarList:
        drawPlayerBar(window, bar)
    for item in menu.dropdownList:
        drawDropdownItem(window, item)

    if menu.gameSection == 0:
        window.blit(logo, (WIDTH / 2 - logo.get_rect().size[0] / 2, HEIGHT / 2 - logo.get_rect().size[1] / 2 - 300))
    
    # Vẽ logo Blue Lock khi ở section 6 (Characters)
    if menu.gameSection == 6 and blue_lock_logo is not None:
        window.blit(blue_lock_logo, (270, 30))
    elif menu.gameSection == 6:
        print("Warning: blue_lock_logo is None, cannot draw logo")
    
    # Hiển thị cooldown cho Player 1 (góc dưới trái)
    player1 = next((p for p in physicsEngine.playerList if p.nick == "Player 1"), None)
    if player1 and menu.gameSection == 2:  # Chỉ hiển thị khi đang trong game
        cooldown_font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", 20)
        y_offset = HEIGHT - 60
        for skill, cd in player1.skillCooldowns.items():
            if cd["current"] > 0:
                cd_time = cd["current"] / 120  # Chuyển từ frame sang giây (120 fps)
                text = f"{skill.capitalize()}: {cd_time:.1f}s cooldown"
                label = cooldown_font.render(text, True, WHITE)
                label_rect = label.get_rect(topleft=(50, y_offset - 30))  # Căn trái với padding 
                # Đảm bảo text không vượt ra ngoài màn hình
                if label_rect.right > WIDTH:
                    label_rect.left = WIDTH - label_rect.width
                window.blit(label, label_rect.topleft)
                y_offset += 25

    # Hiển thị cooldown cho Player 2 (góc dưới phải)
    player2 = next((p for p in physicsEngine.playerList if p.nick == "Player 2"), None)
    if player2 and menu.gameSection == 2:
        cooldown_font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", 20)
        y_offset = HEIGHT - 60
        for skill, cd in player2.skillCooldowns.items():
            if cd["current"] > 0:
                cd_time = cd["current"] / 120
                text = f"{skill.capitalize()}: {cd_time:.1f}s cooldown"
                label = cooldown_font.render(text, True, WHITE)
                label_rect = label.get_rect(topright=(WIDTH - 50, y_offset - 30))  # Căn phải với padding 
                # Đảm bảo text không vượt ra ngoài màn hình
                if label_rect.left < 0:
                    label_rect.left = 0
                window.blit(label, label_rect.topleft)
                y_offset += 25
# Ẩn logo khi bật hướng dẫn
def drawLogo(window):
    if not menu.show_tutorial:  # Chỉ hiển thị nếu không bật hướng dẫn
        window.blit(logo, (WIDTH/2 - 100, HEIGHT/2 - 300))