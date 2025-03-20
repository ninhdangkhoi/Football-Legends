import time
import pygame

import physicsEngine
import gameHandler

from render import WIDTH
from render import HEIGHT

import functools
from classes import *
from constants import *
 
pygame.init()

regularFont = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf",20)
semiboldFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UNirkOUuhp.ttf",20)
boldFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",20)

lightFont = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf",18)
buttonFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",18)
buttonFont2 = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",24)
buttonFont3 = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",28)
bigFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",22)
gigaFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",100)

buttonList = []
characterButtons = []  # Danh sách các nút trong UI chọn nhân vật
playerBarList = []
dropdownList = []

characterButtons = []  # Danh sách các nút trong UI chọn nhân vật
characterSection = 6

selectedPlayerBar = None
isTyping = False
textBox = None
textBoxUnicode = True
typedObject = None
typedObjectAttribute = None
typedObjectUpdate = None
typeOnce = False
typeRawInput = False
typeResult = None
typedInO = None
typedInTB = None

isDragging = False
dragPointX = 0
dragPointY = 0

isDropdownListActive = False
dropdownListBox = None
dropdownSelectedItem = None
dropdownListX = 0
dropdownListY = 0
dropdownListW = 0
dropdownListH = 0
overDropdownList = False

redTeamBox = None
spectatorTeamBox = None
blueTeamBox = None

gameSection = 0
show_tutorial = False
show_credits = False
def doNothing( button, argument):
    pass
#these 2 functions comes from a reply by @unutbu on https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects
def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))
# Khai báo biến global để quản lý nút
global tutorialButton
global tutorialButton2
global creditsButton
global creditsButton2
tutorialButton = Button(3, WIDTH / 2 - 317.5, HEIGHT / 2 - 217.5, 650, 600, " ", False, buttonFont, WHITE, (0, 0, 0), (0, 0, 0),(0, 0, 0), doNothing, None)
tutorialButton2 = Button(0, WIDTH/2 - 300, HEIGHT/2 - 200, 615, 565, " ", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
creditsButton = Button(0, WIDTH / 2 - 317.5, HEIGHT / 2 - 217.5, 650, 525, " ", False, buttonFont, WHITE, (0, 0, 0), (0, 0, 0),(0, 0, 0), doNothing, None)
creditsButton2 = Button(0, WIDTH/2 - 300, HEIGHT/2 - 200, 615, 490, " ", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
buttonList.append(tutorialButton)  # Thêm vào danh sách để quản lý
buttonList.append(tutorialButton2)  # Thêm vào danh sách để quản lý
tutorialButton.visible = False  # Ẩn nút ban đầu
tutorialButton2.visible = False  # Ẩn nút ban đầu

buttonList.append(creditsButton)  # Thêm vào danh sách để quản lý
buttonList.append(creditsButton2)  # Thêm vào danh sách để quản lý
creditsButton.visible = False  # Ẩn nút ban đầu
creditsButton2.visible = False  # Ẩn nút ban đầu
# CHARACTER'S AVATARS LIST
characterImages = [
    "./assets/images/Barou.png",
    "./assets/images/Isagi.png",
    "./assets/images/Nagi.png",
    "./assets/images/Rin.png",
    "./assets/images/Sae.png",
    "./assets/images/Kunigami.png",
    "./assets/images/Bachira.png",
    "./assets/images/Lorenzo.png",
    "./assets/images/Kaiser.png"
]

# Danh sách tên và mô tả cho từng nhân vật
characterDetails = [
    {"name": "Barou Shoei", "description": "“Whenever I’m out on the field, I’m the King!”                                                             SKILL 1: Dribbling Lord - SKILL 2: King Shot"},
    {"name": "Isagi Yoichi", "description": "“Ore wa, STRIKER DA! This is the moment of Yoichi Isagi’s awakening!”                                                             SKILL 1: Flow State - SKILL 2: Direct Shot"}, 
    {"name": "Nagi Seishiro", "description": "“Nice to meet you, Japan. I am...NAGI SEISHIRO!”                                                             SKILL 1: Dash - SKILL 2: Magnet Control"},
    {"name": "Rin Itoshi", "description": "“Friend or foe doesn’t matter. You’re all half-baked NPC’s to me.”                                                             SKILL 1: Curve Shot - SKILL 2: Opposite Direction"},
    {"name": "Sae Itoshi", "description": "“This is a one-shot match. You'll never surpass me.”                                                             SKILL 1: Magical Turn - SKILL 2: Perfect Shot"},
    {"name": "Kunigami Rensuke", "description": "“Don't forget about this dark horse.”                                                             SKILL 1: Body Block - SKILL 2: Wild Shot"},
    {"name": "Bachira Meguru", "description": "“Both the U-20s and this field, we’ve got ‘em. We’ll smash them all!”                                                             SKILL 1: Samba Dance - SKILL 2: Monster Dance"},
    {"name": "Don Lorenzo", "description": "[New Generation World XI] “There's nothing in the world that money can't buy. Yo, Michael!”                                                             SKILL 1: Ace Eater - SKILL 2: Zombie Dribbling"},
    {"name": "Michael Kaiser", "description": "[New Generation World XI] “I’m Kaiser, the one who reveals what’s impossible.”                                                             SKILL 1: Emperor Flow - SKILL 2: Kaiser Impact"}
]

currentCharacterIndex = 0  # Chỉ số nhân vật hiện tại
selectedPlayer = 1  # 1 = Player 1, 2 = Player 2 (mặc định chọn Player 1)
player1Avatar = characterImages[0]  # Avatar mặc định cho Player 1
player2Avatar = characterImages[1]  # Avatar mặc định cho Player 2
#BUTTON FUNCTIONS
def showTutorial(button, argument):
    global show_tutorial, tutorialButton, tutorialButton2, buttonList
    show_tutorial = not show_tutorial
    tutorialButton.visible = show_tutorial  # Bật/tắt nút viền ngoài
    tutorialButton2.visible = show_tutorial  # Bật/tắt nút nền chính

    # Danh sách các nút cần ẩn (loại bỏ "How to Play?" và nút hướng dẫn)
    buttons_to_hide = [
        "Play", "Settings", "Exit", "Characters", "Credits", "", "   "  # Chữ tác giả
    ]

    for btn in buttonList:
        # Chỉ ẩn các nút trong danh sách buttons_to_hide, không ẩn nút viền "  "
        if btn.string in buttons_to_hide:
            btn.visible = not show_tutorial  # Ẩn khi bật hướng dẫn, hiện khi tắt

        # Đảm bảo nút viền "  " chỉ hiển thị khi show_tutorial bật
        if btn == tutorialButton or btn == tutorialButton2:
            btn.visible = show_tutorial
def showCredits(button, argument):
    global show_credits, creditsButton, creditsButton2, buttonList
    show_credits = not show_credits
    creditsButton.visible = show_credits  # Bật/tắt nút viền ngoài
    creditsButton2.visible = show_credits  # Bật/tắt nút nền chính

    # Danh sách các nút cần ẩn (loại bỏ "Credits" và nút credits)
    buttons_to_hide = [
        "Play", "Settings", "Exit", "Characters", "How to play?", "", "  "
    ]

    for btn in buttonList:
        # Chỉ ẩn các nút trong danh sách buttons_to_hide, không ẩn nút viền "   "
        if btn.string in buttons_to_hide:
            btn.visible = not show_credits  # Ẩn khi bật credits, hiện khi tắt

        # Đảm bảo nút viền "   " chỉ hiển thị khi show_credits bật
        if btn == creditsButton or btn == creditsButton2:
            btn.visible = show_credits

def goToSection( button, argument):
    global gameSection
    gameSection = argument

def goToExit( button, argument):
    gameHandler.saveRecord()
    gameHandler.run = False

def addPlayer(button, argument):
    if gameHandler.SoundOn:
        gameHandler.joinedSound.play()
    
    Player("Player " + str(gameHandler.redPlayersCount+gameHandler.bluePlayersCount+gameHandler.spectatorsCount + 1), "NONE", NO_KEYS, 0)
def tutorial(win):
    if show_tutorial:  # Chỉ vẽ nếu show_tutorial == True
        instructions = [
            "Tutorials:",
            "1. PLAY:",
            "- Play vs Human:",
            "   + Right click to change controls and nickname.",
            "- Play vs Bot:",
            "   + Left click 1x for Easy Bot (White).",
            "   + Left click 2x for Medium Bot (Yellow).",
            "   + Left click 3x for Hard Bot (Red).",
            "- To continue the game, press Esc",
            "2. SETTINGS:",
            "- Replays: Turn on and of records of the match.",
            "- Sounds: Turn on and off the sounds & music.",
            "3. CHARACTERS:",
            "- Select different characters to play with their styles.",
            "4. EXIT:",
            "- Click 'Exit' to close the game.",
            "5. CREDITS:",
            "- Just the credits of the game and the source."
        ]
        title_font = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf", 30)  # Font to đậm hơn
        content_font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", 22)  # Font nhỏ hơn cho nội dung

        title_surface = title_font.render("Tutorials:", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 175))  # Căn giữa

        win.blit(title_surface, title_rect)  # Vẽ tiêu đề

        # Vẽ nội dung căn trái
        start_x = WIDTH / 2 - 275  # Căn lề trái
        start_y = HEIGHT / 2 - 150  # Xuống dưới tiêu đề

        for i, line in enumerate(instructions[1:]):  # Bỏ "Tutorials:" vì đã vẽ riêng
            text_surface = content_font.render(line, True, WHITE)
            win.blit(text_surface, (start_x, start_y + i * 30))  # Căn lề trái

def Credit(win):
    if show_credits:  # Chỉ vẽ nếu show_tutorial == True
        instructions = [
            "Credits:",
            "Raw source from @Chylb/GitHub (2018 file), reworked",
            "and continuously developed by:",
            "",
            "- Truong Hoang Tan Dung",
            "- Nguyen Doan Minh",
            "- Do Minh Quan",
            "- Ninh Dang Khoi"
        ]
        title_font = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf", 30)  # Font to đậm hơn
        content_font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", 22)  # Font nhỏ hơn cho nội dung

        title_surface = title_font.render("Credits:", True, WHITE)
        title_rect = title_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 175))  # Căn giữa

        win.blit(title_surface, title_rect)  # Vẽ tiêu đề

        # Vẽ nội dung căn trái
        start_x = WIDTH / 2 - 275  # Căn lề trái
        start_y = HEIGHT / 2 - 150  # Xuống dưới tiêu đề

        for i, line in enumerate(instructions[1:]):  # Bỏ "Credits:" vì đã vẽ riêng
            text_surface = content_font.render(line, True, WHITE)
            win.blit(text_surface, (start_x, start_y + i * 30))  # Căn lề trái

def changeNick( button, argument):
    global isTyping
    global textBox
    global textBoxUnicode
    global typedObject
    global typedObjectAttribute
    global typedObjectUpdate
    global typeResult
    global typeOnce
    global typeRawInput
    global selectedPlayerBar

    isTyping = True
    textBox = button
    textBoxUnicode = True
    typedObject = selectedPlayerBar
    typedObjectAttribute = "player.nick"
    typedObjectUpdate = selectedPlayerBar.updateName
    typeResult = selectedPlayerBar.player.nick
    typeOnce = False
    typeRawInput = False

def goToPlayerControls(button, argument):
    global gameSection
    global selectedPlayerBar
    gameSection = 5

    global upKeyBox, downKeyBox, leftKeyBox, rightKeyBox, kickKeyBox, abilityKeyBox, shootKeyBox

    upKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyUp)
    downKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyDown)
    leftKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyLeft)
    rightKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyRight)
    kickKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyKick)
    
    # Debug: In thông tin phím hiện tại
    print(f"Player {selectedPlayerBar.player.nick} controls opened: Ability={pygame.key.name(selectedPlayerBar.player.keyAbility)}, Shoot={pygame.key.name(selectedPlayerBar.player.keyShoot)}")

    # Đổi tên skill tùy theo nhân vật
    if selectedPlayerBar.player.avatar == "./assets/images/Nagi.png":
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Dash", True, WHITE)
        shootKeyBox.label = buttonFont.render("Shoot", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Isagi.png":
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Flow State", True, WHITE)
        shootKeyBox.label = buttonFont.render("Direct Shot", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Bachira.png":  # Thêm trường hợp cho Bachira
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Samba Dance", True, WHITE)
        shootKeyBox.label = buttonFont.render("Free Nutmeg", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Sae.png":  # Thêm trường hợp cho Sae
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Magical Turn", True, WHITE)
        shootKeyBox.label = buttonFont.render("Perfect Shot", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Barou.png":  # Thêm trường hợp cho Barou
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Dribbling Lord", True, WHITE)
        shootKeyBox.label = buttonFont.render("King Shot", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Kunigami.png":  # Thêm trường hợp cho Kunigami
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Body Block", True, WHITE)
        shootKeyBox.label = buttonFont.render("Wild Shot", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Lorenzo.png":  # Thêm trường hợp cho Lorenzo
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Ace Eater", True, WHITE)
        shootKeyBox.label = buttonFont.render("Zombie Dribbling", True, WHITE)
    elif selectedPlayerBar.player.avatar == "./assets/images/Kaiser.png":  # Thêm trường hợp cho kaiser
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Emperor Flow", True, WHITE)
        shootKeyBox.label = buttonFont.render("Kaiser Impact", True, WHITE)
    else:
        abilityKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyAbility)
        shootKeyBox.string = pygame.key.name(selectedPlayerBar.player.keyShoot)
        abilityKeyBox.label = buttonFont.render("Skill 1", True, WHITE)
        shootKeyBox.label = buttonFont.render("Skill 2", True, WHITE)

    upKeyBox.update()
    downKeyBox.update()
    leftKeyBox.update()
    rightKeyBox.update()
    kickKeyBox.update()
    abilityKeyBox.update()
    shootKeyBox.update()

    upKeyBox.update()
    downKeyBox.update()
    leftKeyBox.update()
    rightKeyBox.update()
    kickKeyBox.update()
    abilityKeyBox.update()
    shootKeyBox.update()

def changePlayerControls(button, argument):
    global isTyping, textBox, textBoxUnicode, typedObject, typedObjectAttribute, typedObjectUpdate, typeResult, typeOnce, typeRawInput, selectedPlayerBar

    isTyping = True
    textBox = button
    textBoxUnicode = False
    typedObject = selectedPlayerBar
    typedObjectUpdate = selectedPlayerBar.updateName
    typeOnce = True
    typeRawInput = True

    if argument == 0:
        textBox = upKeyBox
        typedObjectAttribute = "player.keyUp"
    elif argument == 1:
        textBox = downKeyBox
        typedObjectAttribute = "player.keyDown"
    elif argument == 2:
        textBox = leftKeyBox
        typedObjectAttribute = "player.keyLeft"
    elif argument == 3:
        textBox = rightKeyBox
        typedObjectAttribute = "player.keyRight"
    elif argument == 4:
        textBox = kickKeyBox
        typedObjectAttribute = "player.keyKick"
    elif argument == 5:
        textBox = abilityKeyBox
        typedObjectAttribute = "player.keyAbility"
    elif argument == 6:
        textBox = shootKeyBox
        typedObjectAttribute = "player.keyShoot"

    # Debug: In phím được chọn
    print(f"Changing control for {selectedPlayerBar.player.nick}: {typedObjectAttribute} -> waiting for input")
def deletePlayer(button, argument):
    if gameHandler.SoundOn:
        gameHandler.leftSound.play()
    global selectedPlayerBar
    if selectedPlayerBar.player.team == "BLUE":
        gameHandler.bluePlayersCount -= 1
    elif selectedPlayerBar.player.team == "RED":
        gameHandler.redPlayersCount -= 1
    else:
        gameHandler.spectatorsCount -= 1

    for bar in playerBarList:
        if bar.player.team == selectedPlayerBar.player.team:
            if bar.pos > selectedPlayerBar.pos:
                bar.pos -= 1
                bar.updateCoordinates()
                bar.updateName()
    physicsEngine.playerList.remove( selectedPlayerBar.player)
    playerBarList.remove( selectedPlayerBar)

    goToSection( button, 1)

def prevCharacter(button, argument):
    global currentCharacterIndex, characterNameButton, characterDescButton
    currentCharacterIndex = (currentCharacterIndex - 1) % len(characterImages)
    characterCounter.string = f"{currentCharacterIndex + 1}/{len(characterImages)}"
    characterCounter.update()
    # Cập nhật nội dung thay vì tạo mới
    characterNameButton.string = characterDetails[currentCharacterIndex]["name"]
    characterDescButton.string = characterDetails[currentCharacterIndex]["description"]
    characterNameButton.update()
    characterDescButton.update()

def nextCharacter(button, argument):
    global currentCharacterIndex, characterNameButton, characterDescButton
    currentCharacterIndex = (currentCharacterIndex + 1) % len(characterImages)
    characterCounter.string = f"{currentCharacterIndex + 1}/{len(characterImages)}"
    characterCounter.update()
    # Cập nhật nội dung thay vì tạo mới
    characterNameButton.string = characterDetails[currentCharacterIndex]["name"]
    characterDescButton.string = characterDetails[currentCharacterIndex]["description"]
    characterNameButton.update()
    characterDescButton.update()
    
def selectCharacter(button, argument):
    global player1Avatar, player2Avatar
    from physicsEngine import playerList  # Import để truy cập danh sách người chơi
    
    # Chọn avatar dựa trên selectedPlayer
    selected_avatar = characterImages[currentCharacterIndex]
    if selectedPlayer == 1:
        player1Avatar = selected_avatar
        target_nick = "Player 1"
    else:
        player2Avatar = selected_avatar
        target_nick = "Player 2"
    
    # Cập nhật avatar cho người chơi trong playerList
    for player in playerList:
        if player.nick == target_nick:
            player.avatar = selected_avatar
            if player.avatar == "./assets/images/Lorenzo.png":  
                player.applyBuff()
            print(f"Updated avatar for {player.nick} to {player.avatar}")  # Debug
            break
    # Đổi màu nút Select để xác nhận hành động
    button.color = GREEN_PRESSED
    button.update()

def selectPlayer(button, argument):
    global selectedPlayer
    selectedPlayer = argument
    player1Button.textColor = WHITE if selectedPlayer == 1 else BLACK
    player2Button.textColor = WHITE if selectedPlayer == 2 else BLACK
    player1Button.label = player1Button.font.render(player1Button.string, True, player1Button.textColor)
    player2Button.label = player2Button.font.render(player2Button.string, True, player2Button.textColor)

def startGame( button, argument):
    global gameSection

    if not gameHandler.started:
        gameSection = 2

        gameHandler.startNewMatch()
        button.color = RED_BUTTON
        button.colorOver = RED_OVER
        button.colorPressed = RED_PRESSED
        button.string = "Stop game"
        button.update()
    else:
        gameHandler.started = False

        button.color = GREEN_BUTTON
        button.colorOver = GREEN_OVER
        button.colorPressed = GREEN_PRESSED
        button.string = "Start game"
        button.update()

def switchsound( button, argument):
    if gameHandler.SoundOn:
        button.string = "Sounds: OFF"
        gameHandler.SoundOn = False
    else:
        button.string = "Sounds: ON"
        gameHandler.SoundOn = True
    button.update()    
def switchReplay( button, argument):
    if gameHandler.replaysTurnedOn:
        button.string = "Replays: OFF"
        gameHandler.replaysTurnedOn = False
    else:
        button.string = "Replays: ON"
        gameHandler.replaysTurnedOn = True
    button.update()

def dropdownTimeLimit( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.timeLimit)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button

        for i in range (argument):
            DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, str(i), button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setTimeLimit, i)
        dropdownSelectedItem = dropdownList[ gameHandler.timeLimit]

def dropdownScoreLimit( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.scoreLimit)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button

        for i in range (argument):
            DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, str(i), button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setScoreLimit, i)
        dropdownSelectedItem = dropdownList[ gameHandler.scoreLimit]

def dropdownStadiums( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.stadium)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button

        for i, stadium in enumerate(gameHandler.stadiums()):
            if stadium == gameHandler.stadium:
                dropdownSelectedItem = DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, stadium, button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setStadium, stadium)
            else:
                DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, stadium, button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setStadium, stadium)

#DROPDOWN LIST FUNCTIONS

def setTimeLimit( argument):
    gameHandler.timeLimit = argument

def setScoreLimit( argument):
    gameHandler.scoreLimit = argument

def setStadium( argument):
    gameHandler.stadium = argument
    gameHandler.loadStadium( argument)

############################################################################################################################################################################################################################################
#MENU FUNCTIONS

def init():

    #MAIN MENU
    Button(0, WIDTH / 2 - 167.5, HEIGHT / 2 - 167.5, 335, 485, "", False, buttonFont, WHITE, (0,0,0), (0,0,0),(0,0,0), doNothing, None)  # OUTLINE Cho cái viền
    Button( 0, WIDTH/2 - 150, HEIGHT/2 - 150, 300, 450, "", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
    Button( 0, WIDTH/2 + 80, HEIGHT/2 - 220, 0, 0, "", False, bigFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    #Đổi tên nút Play vs Human --> Play
    Button( 0, WIDTH/2 - 80, HEIGHT/2 - 100, 160, 60, "Play", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 1)
    Button( 0, WIDTH/2 - 80, HEIGHT/2, 160, 60, "Settings", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 3)
    Button( 0, WIDTH/2 - 80, HEIGHT/2 + 200, 160, 60, "Exit", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), goToExit, None)
    Button(0, WIDTH/2 - 80, HEIGHT/2 + 100, 160, 60, "Characters", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 6)
    #Nút hướng dẫn chơi game, toàn text với text thôi khỏi đụng.
    Button(0, WIDTH/2 - 735, HEIGHT/2 + 300, 180, 80, "  ", False, buttonFont, WHITE, (0,0,0), (0,0,0),(0,0,0), doNothing, None)
    Button(0, WIDTH/2 - 725, HEIGHT/2 + 310, 160, 60, "How to play?", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), showTutorial, None)
    #Credits cho game - 4 creators
    Button(0, WIDTH/2 - 510, HEIGHT/2 + 300, 180, 80, "   ", False, buttonFont, WHITE, (0,0,0), (0,0,0),(0,0,0), doNothing, None)
    Button(0, WIDTH/2 - 500, HEIGHT/2 + 310, 160, 60, "Credits", False, buttonFont2, WHITE, (64,64,64), (192,192,192), (55,55,55), showCredits, None)
    
    # CHARACTER SELECTION SECTION
    Button(6, WIDTH / 2 - 400, HEIGHT / 2 - 300, 800, 600, "", False, buttonFont, WHITE, (0, 0, 0), (0, 0, 0), (0, 0, 0), doNothing, None)  # Viền ngoài (tăng width từ 500 lên 800)
    Button(6, WIDTH / 2 - 380, HEIGHT / 2 - 280, 760, 560, "", False, buttonFont, WHITE, (32, 32, 32), (32, 32, 32), (32, 32, 32), doNothing, None)  # Nền chính (tăng width từ 460 lên 760)
    # Nút Previous (<)
    Button(6, WIDTH / 2 - 350, HEIGHT / 2 + 150, 50, 50, "<", False, buttonFont2, WHITE, (64, 64, 64), (192, 192, 192), (55, 55, 55), prevCharacter, None)
    # Nút Next (>)
    Button(6, WIDTH / 2 + 300, HEIGHT / 2 + 150, 50, 50, ">", False, buttonFont2, WHITE, (64, 64, 64), (192, 192, 192), (55, 55, 55), nextCharacter, None)
    # Nút Close
    Button(6, WIDTH / 2 - 75, HEIGHT / 2 + 220, 150, 50, "Close", False, buttonFont2, WHITE, (64, 64, 64), (192, 192, 192), (55, 55, 55), goToSection, 0)
    # Nút Select
    Button(6, WIDTH / 2 - 75, HEIGHT / 2 + 160, 150, 50, "Select", False, buttonFont2, WHITE, GREEN_BUTTON, GREEN_OVER, GREEN_PRESSED, selectCharacter, None)
    # Nút Player 1
    global player1Button
    player1Button = Button(6, WIDTH / 2 - 150, HEIGHT / 2 - 250, 100, 40, "Player 1", False, buttonFont, WHITE if selectedPlayer == 1 else BLACK, (64, 64, 64), (192, 192, 192), (55, 55, 55), selectPlayer, 1)
    # Nút Player 2
    global player2Button
    player2Button = Button(6, WIDTH / 2 + 50, HEIGHT / 2 - 250, 100, 40, "Player 2", False, buttonFont, WHITE if selectedPlayer == 2 else BLACK, (64, 64, 64), (192, 192, 192), (55, 55, 55), selectPlayer, 2)
    # Counter
    global characterCounter
    characterCounter = Button(6, WIDTH / 2 - 50, HEIGHT / 2 + 100, 100, 30, f"{currentCharacterIndex + 1}/{len(characterImages)}", False, buttonFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    # Khu vực hiển thị ảnh nhân vật
    Button(6, WIDTH / 2 - 350, HEIGHT / 2 - 200, 300, 300, "", False, buttonFont, WHITE, (32, 32, 32), (32, 32, 32), (32, 32, 32), doNothing, "image1")
    # Thêm tên và mô tả
    global characterNameButton
    global characterDescButton
    characterNameButton = Button(6, WIDTH / 2 - 20, HEIGHT / 2 - 200, 400, 40, characterDetails[currentCharacterIndex]["name"], False, buttonFont2, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    characterDescButton = Button(6, WIDTH / 2 - 20, HEIGHT / 2 - 150, 400, 150, characterDetails[currentCharacterIndex]["description"], False, buttonFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    
    #LOBBY
    global redTeamBox
    global spectatorTeamBox
    global blueTeamBox
    global startButton

    Button( 1, WIDTH/2 - 450, HEIGHT/2 - 275,900,550, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)

    Button( 1, WIDTH/2 - 230 - 60, HEIGHT/2 - 210,120,25, "Red", False, buttonFont, LABEL_RED, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    Button( 1, WIDTH/2 - 60, HEIGHT/2 - 210,120,25, "Spectators", False, buttonFont, WHITE, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    Button( 1, WIDTH/2 + 170, HEIGHT/2 - 210,120,25, "Blue", False, buttonFont, LABEL_BLUE, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    redTeamBox = Button( 1, WIDTH/2 - 340, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)
    spectatorTeamBox = Button( 1, WIDTH/2 - 110, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)
    blueTeamBox = Button( 1, WIDTH/2 + 120, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)

    Button( 1, WIDTH/2 - 445, HEIGHT/2 - 140,100,25, "Add Player", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), addPlayer, None)
    Button( 1, WIDTH/2 + 340, HEIGHT/2 - 265,100,25, "Leave", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 0)

    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 125,150,20, "Time limit", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 150,150,20, "Score limit", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 175,150,20, "Stadium", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    startButton = Button( 1, WIDTH/2 - 65, HEIGHT/2 + 220,130,25, "Start game", False, buttonFont, WHITE, (58,153,51), (70,184,61), (46,122,41), startGame, None)

    timeLimitBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 125,150,20, str(gameHandler.timeLimit), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownTimeLimit, 6)
    scoreLimitBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 150,150,20, str(gameHandler.scoreLimit), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownScoreLimit, 6)
    stadiumBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 175,150,20, str(gameHandler.stadium), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownStadiums, None)

    #GAME
    global abilityKeyBox
    global upKeyBox
    global downKeyBox
    global leftKeyBox
    global rightKeyBox
    global kickKeyBox
    global shootKeyBox


    global scoreBar
    global timeBar
    global overtimeSprite
    global upperShadow
    global lowerShadow
    global upperInfo
    global lowerInfo
    global pauseBar

    Button( 2, WIDTH/2 - 220,0,440,40, "", False, buttonFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    scoreBar = Button( 2, WIDTH/2 - 180,0,50,40, "Score", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    timeBar = Button( 2, WIDTH/2 + 160,0,50,40, "Time", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    overtimeSprite = Button( 2, WIDTH/2 + 35,0,50,40, "", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    upperShadow = Button( 2, WIDTH/2 + 5, HEIGHT/2 - 50 + 5,0,0, "", False, gigaFont, BLACK, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    lowerShadow = Button( 2, WIDTH/2 + 5, HEIGHT/2 + 50 + 5,0,0, "", False, gigaFont, BLACK, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    upperInfo = Button( 2, WIDTH/2, HEIGHT/2 - 50,0,0, "", False, gigaFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    lowerInfo = Button( 2, WIDTH/2, HEIGHT/2 + 50,0,0, "", False, gigaFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    pauseBar = Button( 2, WIDTH/2, HEIGHT/2 + 100,0,10, "", False, buttonFont, WHITE, WHITE, WHITE, WHITE, doNothing, None)

    Button( 2, WIDTH/2 - 215,10,25,25, "", False, buttonFont, WHITE, PLAYER_RED, PLAYER_RED, PLAYER_RED, doNothing, None)
    Button( 2, WIDTH/2 - 120,10,25,25, "", False, buttonFont, WHITE, PLAYER_BLUE, PLAYER_BLUE, PLAYER_BLUE, doNothing, None)

    #SETTINGS
    Button(3, WIDTH / 2 - 167.5, HEIGHT / 2 - 217.5, 335, 435, "", False, buttonFont, WHITE, (0, 0, 0), (0, 0, 0),(0, 0, 0), doNothing, None)  # OUTLINE Cho cái viền
    Button( 3, WIDTH/2 - 150, HEIGHT/2 - 200,300,400, "", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
    Button( 3, WIDTH/2 - 60, HEIGHT/2 - 150,120,60, "Replays: ON", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), switchReplay, None)
    Button( 3, WIDTH/2 - 60, HEIGHT/2 + 50,120,60, "Close", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 0)
    Button( 3, WIDTH/2 - 60, HEIGHT/2 - 50,120,60, "Sounds: ON", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), switchsound, None)
    #PLAYER SETTINGS
    global nickBox

    Button( 4, WIDTH/2 - 150, HEIGHT/2 - 275,300,550, "", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 250,50,60, "Nick:", False, buttonFont, WHITE, (64,64,64), (64,64,64), (64,64,64), doNothing, None)
    nickBox = Button( 4, WIDTH/2 - 60, HEIGHT/2 - 250,180,60, "", True, lightFont, WHITE, (48,48,48), (48,48,48), (48,48,48), changeNick, None)

    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 170,220,60, "Change controls", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), goToPlayerControls, None)
    #Button( 4, WIDTH/2 - 125, HEIGHT/2 + 60,250,90, "avatar (Coming soon..)", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, 1)
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 90,220,60, "Close", False, buttonFont, WHITE,(64,64,64), (192,192,192), (55,55,55), goToSection, 1)
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 10,220,60, "Delete player", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), deletePlayer, None)

    # CONTROLS
    Button(5, WIDTH/2 - 150, HEIGHT/2 - 275, 300, 600, "", False, buttonFont, WHITE, (32,32,32), (32,32,32), (32,32,32), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 - 250, 80, 60, "Up", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 - 170, 80, 60, "Down", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 - 90, 80, 60, "Left", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 - 10, 80, 60, "Right", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 + 70, 80, 60, "Kick", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 + 150, 80, 60, "Skill 1", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 + 230, 80, 60, "Skill 2", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), doNothing, None)
    Button(5, WIDTH/2 - 110, HEIGHT/2 + 310, 220, 60, "Close", False, buttonFont, WHITE, (64,64,64), (192,192,192), (55,55,55), goToSection, 4)

    global upKeyBox, downKeyBox, leftKeyBox, rightKeyBox, kickKeyBox, abilityKeyBox, shootKeyBox
    upKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 - 250, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 0)
    downKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 - 170, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 1)
    leftKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 - 90, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 2)
    rightKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 - 10, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 3)
    kickKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 + 70, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 4)
    abilityKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 + 150, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 5)
    shootKeyBox = Button(5, WIDTH/2 - 30, HEIGHT/2 + 230, 160, 60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 6)
def update(previousKeys, currentKeys, mouseWasPressed, mousePressed, events, win):
    global isDragging
    global dragPointX
    global dragPointY

    global isTyping
    global textBox
    global textBoxUnicode
    global typedObject
    global typedObjectAttribute
    global typedObjectUpdate
    global typeResult
    global typeOnce
    global typeRawInput
    global selectedPlayerBar
    global typedInO
    global typedInTB

    global isDropdownListActive
    global dropdownListBox
    global dropdownSelectedItem

    global redTeamBox
    global blueTeamBox
    global spectatorTeamBox

    mousePos = pygame.mouse.get_pos()

    #FROM GAME TO MENU

    if gameSection == 2 and currentKeys[pygame.K_ESCAPE] and not previousKeys[pygame.K_ESCAPE]:
        goToSection(None, 1)
        gameHandler.pauseMatch()
    elif gameSection == 1 and currentKeys[pygame.K_ESCAPE] and not previousKeys[pygame.K_ESCAPE] and gameHandler.started:
        goToSection(None, 2)
        gameHandler.resumeMatch()

    if gameSection == 2 and currentKeys[pygame.K_p] and not previousKeys[pygame.K_p] and not gameHandler.paused:
        gameHandler.pauseMatch()
    elif gameSection == 2 and currentKeys[pygame.K_p] and not previousKeys[pygame.K_p]:
        gameHandler.resumeMatch()

    #MENU LOGIC
    if isTyping:
        if currentKeys[pygame.K_ESCAPE] or currentKeys[pygame.K_RETURN] or mousePressed[0] and (textBox.x > mousePos[0] or mousePos[0] > textBox.x + textBox.w or textBox.y > mousePos[1] or mousePos[1] > textBox.y + textBox.h):
            isTyping = False
            rsetattr(typedObject, typedObjectAttribute, typeResult)
            typedObjectUpdate()
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if typeRawInput:
                        typedInO = event.key
                    else:
                        typedInO = event.unicode

                    if textBoxUnicode:
                        typedInTB = event.unicode
                    else:
                        typedInTB = pygame.key.name(event.key)

                    if typeOnce:
                        textBox.string = typedInTB
                        typeResult = typedInO
                        rsetattr(typedObject, typedObjectAttribute, typeResult)
                        typedObjectUpdate()
                        isTyping = False
                    else:
                        if event.key == 8:  # backspace
                            textBox.string = textBox.string[0:-1]
                            typeResult = typeResult[0:-1]
                        else:
                            textBox.string += typedInTB
                            typeResult += typedInO
                    textBox.update()

    for button in buttonList:
        if button.visible:  # Chỉ xử lý nút nếu nó đang hiển thị
            button.isOver = False
            if button.section == gameSection and not isDropdownListActive:
                if button.x <= mousePos[0] <= button.x + button.w and button.y <= mousePos[1] <= button.y + button.h:
                    button.isOver = True
                if mouseWasPressed[0] and not mousePressed[0]:  # Khi thả chuột
                    if button.isOver and button.isPressed:
                        button.f(button, button.argument)  # Gọi hàm khi nhấn nút
                        print(f"Button {button.string} clicked!")  # Debug
                    button.isPressed = False
                elif not mouseWasPressed[0] and mousePressed[0] and button.isOver:  # Khi nhấn chuột
                    button.isPressed = True


    if isDropdownListActive and gameSection == 1:
        overDropdownList = False
        for item in dropdownList:
            if item.x <= mousePos[0] and mousePos[0] <= item.x + item.w:
                if item.y <= mousePos[1] and mousePos[1] <= item.y + item.h:
                    dropdownSelectedItem = item
                    overDropdownList = True
                    if mouseWasPressed[0] and not mousePressed[0]:
                        item.f(item.argument)
                        dropdownListBox.string = item.string
                        dropdownListBox.update()
                        isDropdownListActive = False
        if mousePressed[0] and not overDropdownList:
            isDropdownListActive = False

    if isDragging:
        if not mousePressed[0]:
            isDragging = False
            if redTeamBox.isOver or blueTeamBox.isOver or spectatorTeamBox.isOver:
                if selectedPlayerBar.player.team == "RED":
                    gameHandler.redPlayersCount -= 1
                elif selectedPlayerBar.player.team == "NONE":
                    gameHandler.spectatorsCount -= 1
                else:
                    gameHandler.bluePlayersCount -= 1

                for bar in playerBarList:
                    if bar.player.team == selectedPlayerBar.player.team:
                        if bar.pos > selectedPlayerBar.pos:
                            bar.pos -= 1
                            bar.updateCoordinates()
                            bar.updateName()

                if redTeamBox.isOver:
                    gameHandler.redPlayersCount += 1
                    if selectedPlayerBar.player.team != "RED":
                        selectedPlayerBar.player.team = "RED"
                        gameHandler.putPlayerOnPitch(selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.redPlayersCount
                elif spectatorTeamBox.isOver:
                    gameHandler.spectatorsCount += 1
                    if selectedPlayerBar.player.team != "NONE":
                        selectedPlayerBar.player.team = "NONE"
                        gameHandler.putPlayerOnPitch(selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.spectatorsCount
                elif blueTeamBox.isOver:
                    gameHandler.bluePlayersCount += 1
                    if selectedPlayerBar.player.team != "BLUE":
                        selectedPlayerBar.player.team = "BLUE"
                        gameHandler.putPlayerOnPitch(selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.bluePlayersCount

            selectedPlayerBar.updateCoordinates()
            selectedPlayerBar.updateName()
        else:
            selectedPlayerBar.x = mousePos[0] - dragPointX
            selectedPlayerBar.y = mousePos[1] - dragPointY
            selectedPlayerBar.updateName()

    for bar in playerBarList:
        bar.isOver = False
        if bar.x <= mousePos[0] and mousePos[0] <= bar.x + bar.w and not isDragging:
            if bar.y <= mousePos[1] and mousePos[1] <= bar.y + bar.h:
                bar.isOver = True
        if bar == selectedPlayerBar and isDragging:
            bar.isOver = True
        if gameSection == 1 and bar.isOver and mousePressed[0]:
            if mouseWasPressed[0]:
                isDragging = True
                selectedPlayerBar = bar
                playerBarList[playerBarList.index(bar)], playerBarList[len(playerBarList)-1] = playerBarList[len(playerBarList)-1], playerBarList[playerBarList.index(bar)]
                dragPointX = mousePos[0] - bar.x
                dragPointY = mousePos[1] - bar.y

        if bar.isOver and mousePressed[2] and not mouseWasPressed[2]:
            if bar.player.isbot == 0:
                bar.openOptions()
        if bar.isOver and mouseWasPressed[0] and not isDragging:
            bar.player.isbot += 1
            bar.player.isbot %= 4

    # Gọi hàm tutorial để hiển thị text nếu show_tutorial là True
    tutorial(win)
    Credit(win)
