import pygame
import sys
import random
import os
import math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Disaster Response & Survival Hub")

clock = pygame.time.Clock()

# ------------------ ANIMATION GLOBALS ------------------
fade_alpha = 0
subtitle_offset = 0

# ------------------ LOAD SOUNDS ------------------
def load_sound(path):
    try:
        if os.path.exists(path):
            return pygame.mixer.Sound(path)
        else:
            print(f"⚠️ WARNING: Sound file not found at '{path}'")
            return None
    except Exception as e:
        print(f"⚠️ ERROR loading sound '{path}': {e}")
        return None

click_sound    = load_sound("assets/sounds/click.wav")
quake_sound    = load_sound("assets/sounds/earthquake.wav")
fail_sound     = load_sound("assets/sounds/fail.wav")
success_sound  = load_sound("assets/sounds/success.wav")
bad_ending_1_sound = load_sound("assets/sounds/bad_ending.mp3")
good_ending_1_sound = load_sound("assets/sounds/good_ending.mp3")

if click_sound:
    click_sound.set_volume(0.8)

def safe_play(sound):
    if sound:
        sound.play()

# ------------------ LOAD IMAGES ------------------
def load_img(path):
    try:
        if os.path.exists(path):
            img = pygame.image.load(path)
            return pygame.transform.scale(img, (WIDTH, HEIGHT))
        else:
            print(f"⚠️ ERROR: Image file not found at '{path}'")
            surf = pygame.Surface((WIDTH, HEIGHT))
            surf.fill((40, 40, 80))
            return surf
    except Exception as e:
        print(f"⚠️ ERROR loading image '{path}': {e}")
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill((40, 40, 80))
        return surf

default_bg = pygame.Surface((WIDTH, HEIGHT))
default_bg.fill((20, 20, 40))

menu_bg = load_img("assets/menu.png") if os.path.exists("assets/menu.png") else default_bg

image_cache = {}

# ------------------ FONTS ------------------
title_font    = pygame.font.SysFont("Georgia", 50, bold=True)
font          = pygame.font.SysFont("Georgia", 27, bold=True)
small_font    = pygame.font.SysFont("Georgia", 21)
subtitle_font = pygame.font.SysFont("Georgia", 23, bold=True, italic=True)
level_font    = pygame.font.SysFont("Georgia", 20, bold=True)

# ------------------ COLORS ------------------
INDIGO      = (75, 0, 130)
DARK_INDIGO = (45, 0, 90)
BTN_BLUE    = (30, 100, 220)
GREEN_BTN   = (30, 160, 60)
RED_BTN     = (190, 40, 40)
GRAY_BTN    = (90, 90, 90)
GOLD        = (220, 180, 0)
WHITE       = (255, 255, 255)
BLACK       = (0,   0,   0)

# ------------------ GAME STATES ------------------
state             = "menu"
selected_mode     = None
scene             = "start_journey"
last_scene        = None
outcome_triggered = False

# ------------------ TEXT ANIMATION ------------------
displayed_text = ""
text_index     = 0
text_timer     = 0
TEXT_SPEED     = 2

def reset_text():
    global displayed_text, text_index, text_timer
    displayed_text = ""
    text_index     = 0
    text_timer     = 0

def update_text(full_text):
    global displayed_text, text_index, text_timer
    text_timer += 1
    if text_timer >= TEXT_SPEED and text_index < len(full_text):
        displayed_text += full_text[text_index]
        text_index += 1
        text_timer = 0

# ------------------ STORY ------------------
story = {
    "start_journey": {
        "dialogues": [
            {"text": "Jack leaves his home and meets Emily. They ride their bicycles to school.",
             "voice": "assets/sounds/voices/start_journey.mp3",
             "image": "assets/scenes/start_journey.png"}
        ],
        "next": "class_entry"
    },
    "class_entry": {
        "dialogues": [
            {"text": "Jack and Emily enter the classroom and sit with their classmates.",
             "voice": "assets/sounds/voices/class_entry.mp3",
             "image": "assets/scenes/class_entry.png"}
        ],
        "next": "teacher_entry"
    },
    "teacher_entry": {
        "dialogues": [
            {"text": "The teacher enters the classroom.",
             "voice": "assets/sounds/voices/teacher_entry_1.mp3",
             "image": "assets/scenes/teacher_entry_1.png"},
            {"text": "Everyone: Good Morning, Ma'am!",
             "voice": "assets/sounds/voices/teacher_entry_2.mp3",
             "image": "assets/scenes/teacher_entry_3.png"}
        ],
        "next": "teaching"
    },
    "teaching": {
        "dialogues": [
            {"text": "The teacher starts teaching the lesson. Everything is calm.",
             "voice": "assets/sounds/voices/teaching.mp3",
             "image": "assets/scenes/teaching.png"}
        ],
        "next": "teacher_call"
    },
    "teacher_call": {
    "dialogues": [
        {"text": "The teacher suddenly receives a phone call.",
         "voice": "assets/sounds/voices/teacher_call_1.mp3",
         "image": "assets/scenes/teacher_call_1.png"},
        {"text": "She leaves the classroom urgently.",
         "voice": "assets/sounds/voices/teacher_call_2.mp3",
         "image": "assets/scenes/teacher_call_2.png"}
        ],
        "next": "earthquake_start"
    },
    "earthquake_start": {
        "dialogues": [
            {"text": "Suddenly, the building starts shaking violently!",
             "voice": "assets/sounds/voices/earthquake_start.mp3",
             "image": "assets/scenes/earthquake_start_1.png"}
        ],
        "next": "panic_scene"
    },
    "panic_scene": {
        "dialogues": [
            {"text": "Students panic and start shouting in fear!",
             "voice": "assets/sounds/voices/panic_1.mp3",
             "image": "assets/scenes/earthquake_start_2.png"},
            {"text": "Emily: Jack, what should we do?!",
             "voice": "assets/sounds/voices/panic_2.mp3",
             "image": "assets/scenes/panic.png"}
        ],
        "next": "decision"
    },
    "decision": {
        "dialogues": [
            {"text": "Jack shouts: EVERYONE!! EVERYONE!",
             "voice": "assets/sounds/voices/decision.mp3",
             "image": "assets/scenes/panic.png"}
        ],
        "choices": [
            ("Run Outside",       "bad_ending"),
            ("Hide Under Bench",  "good_ending")
        ]
    },
    "bad_ending": {
        "dialogues": [
            {"text": "Run outside!! outside!",
             "voice": "assets/sounds/voices/run_away.mp3",
             "image": "assets/scenes/bad_ending.png"},
            {"text": "Students rush outside in panic... Falling objects injure many students.",
             "voice": "assets/sounds/voices/bad_ending.mp3",
             "image": "assets/scenes/bad_ending.png"}
        ]
    },
    "good_ending": {
        "dialogues": [
            {"text": "Hide under the bench!! under the bench!",
             "voice": "assets/sounds/voices/hide_under.mp3",
             "image": "assets/scenes/good_ending.png"},
            {"text": "Students quickly hide under their desks. The earthquake stops. Everyone is safe!",
             "voice": "assets/sounds/voices/good_ending.mp3",
             "image": "assets/scenes/good_ending.png"}
        ]
    }
}

# ------------------ AUDIO ------------------
dialogue_index = 0
current_sound  = None

def play_dialogue():
    global current_sound
    data = story[scene]["dialogues"][dialogue_index]
    pygame.mixer.stop()
    
    voice_path = data.get("voice", "")
    if os.path.exists(voice_path):
        try:
            current_sound = pygame.mixer.Sound(voice_path)
            current_sound.play()
        except:
            current_sound = None
    else:
        current_sound = None
        
    reset_text()

# =====================================================================
#  UI HELPERS WITH ANIMATIONS
# =====================================================================
def draw_button(text, x, y, w, h, color=BTN_BLUE, text_color=WHITE,
                border_color=BLACK, border_w=3, radius=13, fnt=None, is_pulsing=False):
    if fnt is None:
        fnt = font
        
    mx, my = pygame.mouse.get_pos()
    is_hovered = x < mx < x + w and y < my < y + h

    visual_x, visual_y, visual_w, visual_h = x, y, w, h

    # Smooth Hover & Pulse effects
    if is_hovered:
        visual_x -= 4
        visual_y -= 4
        visual_w += 8
        visual_h += 8
        color = (min(color[0]+35, 255), min(color[1]+35, 255), min(color[2]+35, 255))
    elif is_pulsing:
        pulse = math.sin(pygame.time.get_ticks() * 0.005) * 3
        visual_x -= pulse
        visual_y -= pulse
        visual_w += pulse * 2
        visual_h += pulse * 2

    pygame.draw.rect(screen, color, (visual_x, visual_y, visual_w, visual_h), border_radius=radius)
    pygame.draw.rect(screen, border_color, (visual_x, visual_y, visual_w, visual_h), border_w, border_radius=radius)
    surf = fnt.render(text, True, text_color)
    rect = surf.get_rect(center=(visual_x + visual_w // 2, visual_y + visual_h // 2))
    screen.blit(surf, rect)

def hovered(mx, my, x, y, w, h):
    return x < mx < x + w and y < my < y + h

def wrap_text(text, fnt, max_w):
    words, lines, current = text.split(), [], ""
    for word in words:
        test = current + (" " if current else "") + word
        if fnt.size(test)[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

# ---- Layout constants ----
NEXT_X, NEXT_Y, NEXT_W, NEXT_H = 760, 530, 120, 50

# =====================================================================
#  DRAW SUBTITLE BOX
# =====================================================================
def draw_subtitle(text):
    global subtitle_offset
    PAD = 15
    LINE_SP = 5
    SUB_X = 20
    SUB_W = NEXT_X - SUB_X - 15  
    
    lines = wrap_text(text, subtitle_font, SUB_W - PAD * 2)
    line_h = subtitle_font.get_height()
    total_text_h = len(lines) * line_h + max(0, len(lines) - 1) * LINE_SP
    
    SUB_H = total_text_h + (PAD * 2)
    SUB_Y = (NEXT_Y + NEXT_H) - SUB_H
    
    # Smoothly animate the subtitle box sliding up
    if subtitle_offset > 0:
        subtitle_offset = max(0, subtitle_offset - 4)
    
    animated_y = SUB_Y + subtitle_offset

    pygame.draw.rect(screen, INDIGO, (SUB_X, animated_y, SUB_W, SUB_H), border_radius=18)
    pygame.draw.rect(screen, BLACK,  (SUB_X, animated_y, SUB_W, SUB_H), 3, border_radius=18)

    sy = animated_y + PAD
    for i, line in enumerate(lines):
        ly = sy + i * (line_h + LINE_SP)
        sh = subtitle_font.render(line, True, (20, 0, 50))
        screen.blit(sh, (SUB_X + PAD + 2, ly + 2))
        tx = subtitle_font.render(line, True, WHITE)
        screen.blit(tx, (SUB_X + PAD, ly))

# =====================================================================
#  DRAW CHOICE BUTTONS 
# =====================================================================
CORRECT_CHOICE = "Hide Under Bench"

def draw_choices():
    btn_w, btn_h = 255, 55
    gap          = 40
    total_w      = btn_w * 2 + gap
    
    sx = (WIDTH - total_w) // 2
    sy = 450 

    choices = story["decision"]["choices"]
    for i, (label, _) in enumerate(choices):
        cx    = sx + i * (btn_w + gap)
        color = GREEN_BTN if label == CORRECT_CHOICE else RED_BTN
        draw_button(label, cx, sy, btn_w, btn_h, color=color)

def get_choice_btn_rects():
    btn_w, btn_h = 255, 55
    gap          = 40
    total_w      = btn_w * 2 + gap
    sx           = (WIDTH - total_w) // 2
    sy           = 450 
    return [(sx, sy, btn_w, btn_h), (sx + btn_w + gap, sy, btn_w, btn_h)]

# =====================================================================
#  OUTCOME SCREENS
# =====================================================================
def draw_overlay():
    ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 155))
    screen.blit(ov, (0, 0))

def outcome_button_rects():
    btn_w, btn_h = 180, 55
    gap          = 40
    total_w      = btn_w * 2 + gap
    sx           = WIDTH // 2 - total_w // 2
    return [(sx, 360, btn_w, btn_h), (sx + btn_w + gap, 360, btn_w, btn_h)]

def draw_outcome_bad():
    draw_overlay()
    t1 = title_font.render("LEVEL FAILED", True, (230, 50, 50))
    t2 = font.render("Running during an earthquake is dangerous!", True, WHITE)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 190))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 270))
    r1, r2 = outcome_button_rects()
    draw_button("Try Again", *r1, color=(200, 100, 20), is_pulsing=True)
    draw_button("Menu",      *r2, color=INDIGO)

def draw_outcome_good():
    draw_overlay()
    t1 = title_font.render("LEVEL COMPLETED!", True, (50, 220, 80))
    t2 = font.render("Drop, Cover, Hold – You saved everyone!", True, WHITE)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 190))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 270))
    r1, r2 = outcome_button_rects()
    draw_button("Next Level", *r1, color=GREEN_BTN, is_pulsing=True)
    draw_button("Menu",       *r2, color=INDIGO)

# =====================================================================
#  MENU PAGE
# =====================================================================
def draw_menu():
    screen.blit(menu_bg, (0, 0))
    
    line1_text = "Disaster Response"
    shadow1 = title_font.render(line1_text, True, BLACK)
    title1  = title_font.render(line1_text, True, GOLD)
    tx1 = WIDTH // 2 - title1.get_width() // 2
    screen.blit(shadow1, (tx1 + 3, 133))
    screen.blit(title1,  (tx1, 130))

    line2_text = "& Survival Hub"
    shadow2 = title_font.render(line2_text, True, BLACK)
    title2  = title_font.render(line2_text, True, GOLD)
    tx2 = WIDTH // 2 - title2.get_width() // 2
    screen.blit(shadow2, (tx2 + 3, 193))
    screen.blit(title2,  (tx2, 190))

    draw_button("Start", WIDTH//2 - 100, 300, 200, 55, color=BTN_BLUE, is_pulsing=True)
    draw_button("Exit",  WIDTH//2 - 100, 375, 200, 55, color=RED_BTN)

# =====================================================================
#  MODE SELECT PAGE
# =====================================================================
MODES      = ["Easy", "Medium", "Hard"]
MODE_BTN_W, MODE_BTN_H = 175, 58
MODE_GAP  = 38

def mode_btn_rects():
    total_w = len(MODES) * MODE_BTN_W + (len(MODES)-1) * MODE_GAP
    sx      = WIDTH // 2 - total_w // 2
    sy      = HEIGHT // 2 - MODE_BTN_H // 2
    return [(sx + i*(MODE_BTN_W + MODE_GAP), sy, MODE_BTN_W, MODE_BTN_H)
            for i in range(len(MODES))]

def draw_mode_select():
    screen.blit(menu_bg, (0, 0))
    rects = mode_btn_rects()
    
    title_y = rects[0][1] - 60 
    
    h = title_font.render("Select Mode", True, GOLD)
    sh= title_font.render("Select Mode", True, BLACK)
    hx = WIDTH//2 - h.get_width()//2
    
    screen.blit(sh, (hx+3, title_y+3))
    screen.blit(h, (hx, title_y))
    
    for i, m in enumerate(MODES):
        draw_button(m, *rects[i], color=INDIGO)
    draw_button("Back", 20, HEIGHT-65, 110, 45, color=GRAY_BTN, fnt=small_font)

# =====================================================================
#  LEVEL SELECT PAGE
# =====================================================================
CELL  = 88
CGAP  = 13
COLS  = 5
ROWS  = 3
GX    = (WIDTH  - (COLS * CELL + (COLS-1)*CGAP)) // 2
GY    = (HEIGHT - (ROWS * CELL + (ROWS-1)*CGAP)) // 2 + 30

def cell_rect(lvl):
    idx = lvl - 1
    r, c = idx // COLS, idx % COLS
    x = GX + c * (CELL + CGAP)
    y = GY + r * (CELL + CGAP)
    return x, y, CELL, CELL

def draw_level_select():
    screen.blit(menu_bg, (0, 0))
    label = selected_mode.upper() if selected_mode else ""
    
    title_y = GY - 60
    
    h  = title_font.render(f"{label}  —  Select Level", True, GOLD)
    sh = title_font.render(f"{label}  —  Select Level", True, BLACK)
    hx = WIDTH//2 - h.get_width()//2
    
    screen.blit(sh, (hx+3, title_y+3))
    screen.blit(h, (hx, title_y))

    for lvl in range(1, 16):
        x, y, w, h = cell_rect(lvl)
        unlocked = (selected_mode == "easy" and lvl == 1)
        color    = GREEN_BTN if unlocked else (85, 85, 85)

        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=12)
        pygame.draw.rect(screen, BLACK, (x, y, w, h), 3, border_radius=12)

        ns = level_font.render(str(lvl), True, WHITE)
        screen.blit(ns, ns.get_rect(center=(x+w//2, y+h//2)))

        if not unlocked:
            ov = pygame.Surface((w, h), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 80))
            screen.blit(ov, (x, y))
            p = 18
            pygame.draw.line(screen, (220,50,50), (x+p, y+p), (x+w-p, y+h-p), 4)
            pygame.draw.line(screen, (220,50,50), (x+w-p, y+p), (x+p, y+h-p), 4)

    draw_button("Back", 20, HEIGHT-65, 110, 45, color=GRAY_BTN, fnt=small_font)

# =====================================================================
#  MAIN LOOP
# =====================================================================
running = True

while running:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            safe_play(click_sound)

            if state == "menu":
                if hovered(mx, my, WIDTH//2-100, 300, 200, 55):
                    state = "mode_select"
                if hovered(mx, my, WIDTH//2-100, 375, 200, 55):
                    pygame.quit(); sys.exit()

            elif state == "mode_select":
                for i, m in enumerate(MODES):
                    rx, ry, rw, rh = mode_btn_rects()[i]
                    if hovered(mx, my, rx, ry, rw, rh):
                        selected_mode = m.lower()
                        state = "level_select"
                if hovered(mx, my, 20, HEIGHT-65, 110, 45):
                    state = "menu"

            elif state == "level_select":
                for lvl in range(1, 16):
                    cx, cy, cw, ch = cell_rect(lvl)
                    if hovered(mx, my, cx, cy, cw, ch):
                        if selected_mode == "easy" and lvl == 1:
                            scene = "start_journey"
                            last_scene = None
                            dialogue_index = 0
                            outcome_triggered = False
                            state = "game"
                if hovered(mx, my, 20, HEIGHT-65, 110, 45):
                    state = "mode_select"

            elif state == "game":
                if outcome_triggered:
                    if scene == "bad_ending":
                        r1, r2 = outcome_button_rects()
                        if hovered(mx, my, *r1):
                            scene = "decision"; last_scene = None; dialogue_index = 0; outcome_triggered = False; play_dialogue()
                        if hovered(mx, my, *r2):
                            state = "menu"
                    elif scene == "good_ending":
                        r1, r2 = outcome_button_rects()
                        if hovered(mx, my, *r2):
                            state = "menu"

                elif scene == "decision":
                    cr = get_choice_btn_rects()
                    if hovered(mx, my, *cr[0]):
                        scene = "bad_ending"; last_scene = None; dialogue_index = 0; outcome_triggered = False
                        play_dialogue()
                    if hovered(mx, my, *cr[1]):
                        scene = "good_ending"; last_scene = None; dialogue_index = 0; outcome_triggered = False
                        play_dialogue()

                else:
                    if hovered(mx, my, NEXT_X, NEXT_Y, NEXT_W, NEXT_H):
                        if scene in story and "next" in story[scene]:
                            scene = story[scene]["next"]
                            last_scene = None; dialogue_index = 0; outcome_triggered = False; play_dialogue()

        if event.type == pygame.KEYDOWN and state == "game":
            if scene not in ("decision", "bad_ending", "good_ending"):
                if scene in story and "next" in story[scene]:
                    scene = story[scene]["next"]
                    last_scene = None; dialogue_index = 0; outcome_triggered = False; play_dialogue()

    if state == "menu":
        draw_menu()
    elif state == "mode_select":
        draw_mode_select()
    elif state == "level_select":
        draw_level_select()
    elif state == "game":
        sx, sy = 0, 0
        
        # Cinematic Multi-directional Shake
        if scene == "earthquake_start" or scene == "panic_scene":
            t = pygame.time.get_ticks()
            sx = int(math.sin(t * 0.05) * 8 + math.cos(t * 0.03) * 4)
            sy = int(math.cos(t * 0.06) * 6 + math.sin(t * 0.04) * 3)
            
            if scene == "earthquake_start" and dialogue_index == 0:
                safe_play(quake_sound)

        # GET THE CURRENT DYNAMIC BACKGROUND IMAGE
        safe_idx = min(dialogue_index, len(story[scene]["dialogues"]) - 1)
        bg_path = story[scene]["dialogues"][safe_idx].get("image", "")
        
        if bg_path:
            if bg_path not in image_cache:
                image_cache[bg_path] = load_img(bg_path)
            screen.blit(image_cache[bg_path], (sx, sy))
        else:
            screen.fill((40, 40, 80))

        # Scene Transitions
        if scene != last_scene:
            last_scene     = scene
            dialogue_index = 0
            outcome_triggered = False
            fade_alpha = 255          # Trigger fade-in
            subtitle_offset = 60      # Trigger text slide-in
            play_dialogue()

        # Audio Progression
        if not pygame.mixer.get_busy():
            if dialogue_index + 1 < len(story[scene]["dialogues"]):
                dialogue_index += 1
                subtitle_offset = 30  # Slide up for new dialogue
                play_dialogue()
            else:
                if scene in ["bad_ending", "good_ending"] and not outcome_triggered:
                    outcome_triggered = True
                    if scene == "bad_ending":
                        safe_play(bad_ending_1_sound)
                        safe_play(fail_sound)
                    else:
                        safe_play(good_ending_1_sound)
                        safe_play(success_sound)

        if outcome_triggered:
            if scene == "bad_ending":
                draw_outcome_bad()
            elif scene == "good_ending":
                draw_outcome_good()
        else:
            safe_idx  = min(dialogue_index, len(story[scene]["dialogues"]) - 1)
            full_text = story[scene]["dialogues"][safe_idx]["text"]
            update_text(full_text)
            draw_subtitle(displayed_text)

            if scene == "decision":
                draw_choices()
            else:
                draw_button("Next", NEXT_X, NEXT_Y, NEXT_W, NEXT_H, color=BTN_BLUE, fnt=small_font, is_pulsing=True)

    # Draw Global Fade Transition
    if fade_alpha > 0:
        fade_surf = pygame.Surface((WIDTH, HEIGHT))
        fade_surf.fill((0, 0, 0))
        fade_surf.set_alpha(fade_alpha)
        screen.blit(fade_surf, (0, 0))
        fade_alpha = max(0, fade_alpha - 15)

    pygame.display.flip()

pygame.quit()
sys.exit()
