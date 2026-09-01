import random
import sys
import pygame

# ============================================================
# INITIALIZE PYGAME
# ============================================================

pygame.init()

WIDTH, HEIGHT = 1200, 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beach Safari Hangman")

clock = pygame.time.Clock()


# ============================================================
# BEACH COLOR PALETTE
# ============================================================

SKY_BLUE = (93, 190, 235)
SKY_LIGHT = (170, 225, 245)

SUN_YELLOW = (255, 225, 90)
SUN_GLOW = (255, 242, 170)

OCEAN_BLUE = (35, 165, 205)
OCEAN_LIGHT = (90, 205, 225)
OCEAN_DARK = (20, 125, 170)

SAND = (244, 214, 145)
SAND_LIGHT = (255, 229, 165)

ISLAND_GREEN = (57, 140, 75)
ISLAND_DARK = (35, 105, 60)

PALM_GREEN = (35, 135, 65)
PALM_DARK = (25, 105, 50)

WOOD_BROWN = (130, 78, 35)
WOOD_LIGHT = (170, 105, 55)

LEAF_GREEN = (45, 150, 70)

WHITE = (255, 255, 255)
BLACK = (20, 25, 25)

DARK_BLUE = (20, 65, 85)
PANEL_BLUE = (15, 65, 82)

BUTTON_BLUE = (35, 125, 190)
BUTTON_HOVER = (55, 155, 215)
BUTTON_DISABLED = (115, 135, 140)

GOLD = (255, 210, 55)

SKIN = (255, 218, 175)
SKIN_SHADOW = (225, 175, 125)

SHIRT_GREEN = (45, 145, 105)
SHIRT_LIGHT = (75, 175, 125)

FLOWER_PINK = (245, 105, 120)
FLOWER_YELLOW = (255, 215, 70)

SHORTS = (175, 145, 85)
SHORTS_DARK = (130, 105, 60)

HAT = (195, 150, 65)
HAT_DARK = (145, 105, 45)

SLIPPER_BLUE = (30, 75, 100)


# ============================================================
# FONTS
# ============================================================

FONT_TITLE = pygame.font.SysFont(
    "georgia", 38, bold=True
)

FONT_WORD = pygame.font.SysFont(
    "courier", 38, bold=True
)

FONT_UI = pygame.font.SysFont(
    "arial", 18, bold=True
)

FONT_HINT = pygame.font.SysFont(
    "georgia", 17, italic=True
)

FONT_SMALL = pygame.font.SysFont(
    "arial", 14, bold=True
)


# ============================================================
# WORD DATABASE
# ============================================================

WORDS = {
    "CHAMELEON":
        "Reptile that changes colour to match surroundings.",

    "REDWOOD":
        "Giant evergreen tree native to coastal forests.",

    "GLACIER":
        "Slowly moving river of ice formed by snow.",

    "PANTHER":
        "Large dark-colored wild forest cat.",

    "CASCADE":
        "Small steep waterfall in nature.",
}


secret_word, hint = random.choice(list(WORDS.items()))

guessed = []

lives = 6


# ============================================================
# KEYBOARD
# ============================================================

RADIUS = 21
GAP = 10

buttons = []

start_x = 75
start_y = 525

for i in range(26):

    x = start_x + (i % 13) * (RADIUS * 2 + GAP)

    y = start_y + (i // 13) * (RADIUS * 2 + GAP)

    buttons.append([
        x,
        y,
        chr(65 + i),
        True
    ])


# ============================================================
# DRAW CLOUD
# ============================================================

def draw_cloud(x, y, scale=1):

    pygame.draw.circle(
        screen,
        WHITE,
        (x, y),
        int(20 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + int(25 * scale), y - int(10 * scale)),
        int(25 * scale)
    )

    pygame.draw.circle(
        screen,
        WHITE,
        (x + int(50 * scale), y),
        int(20 * scale)
    )

    pygame.draw.rect(
        screen,
        WHITE,
        (
            x,
            y,
            int(50 * scale),
            int(20 * scale)
        )
    )


# ============================================================
# DRAW PALM TREE
# ============================================================

def draw_palm_tree(x, y, scale=1):

    # Curved-looking trunk made from lines

    pygame.draw.line(
        screen,
        WOOD_BROWN,
        (x, y),
        (
            x + int(15 * scale),
            y - int(100 * scale)
        ),
        int(12 * scale)
    )

    # Leaves

    top_x = x + int(15 * scale)
    top_y = y - int(100 * scale)

    pygame.draw.line(
        screen,
        PALM_DARK,
        (top_x, top_y),
        (
            top_x - int(65 * scale),
            top_y - int(25 * scale)
        ),
        int(7 * scale)
    )

    pygame.draw.line(
        screen,
        PALM_GREEN,
        (top_x, top_y),
        (
            top_x + int(65 * scale),
            top_y - int(25 * scale)
        ),
        int(7 * scale)
    )

    pygame.draw.line(
        screen,
        PALM_GREEN,
        (top_x, top_y),
        (
            top_x - int(45 * scale),
            top_y + int(35 * scale)
        ),
        int(7 * scale)
    )

    pygame.draw.line(
        screen,
        PALM_DARK,
        (top_x, top_y),
        (
            top_x + int(50 * scale),
            top_y + int(35 * scale)
        ),
        int(7 * scale)
    )

    pygame.draw.line(
        screen,
        PALM_GREEN,
        (top_x, top_y),
        (
            top_x,
            top_y - int(55 * scale)
        ),
        int(7 * scale)
    )


# ============================================================
# DRAW BACKGROUND
# ============================================================

def draw_background():

    # --------------------------------------------------------
    # Sky
    # --------------------------------------------------------

    for y in range(0, 350):

        ratio = y / 350

        r = int(
            SKY_LIGHT[0] * (1 - ratio)
            + SKY_BLUE[0] * ratio
        )

        g = int(
            SKY_LIGHT[1] * (1 - ratio)
            + SKY_BLUE[1] * ratio
        )

        b = int(
            SKY_LIGHT[2] * (1 - ratio)
            + SKY_BLUE[2] * ratio
        )

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )

    # --------------------------------------------------------
    # Sun
    # --------------------------------------------------------

    pygame.draw.circle(
        screen,
        SUN_GLOW,
        (115, 95),
        58
    )

    pygame.draw.circle(
        screen,
        SUN_YELLOW,
        (115, 95),
        42
    )

    # --------------------------------------------------------
    # Clouds
    # --------------------------------------------------------

    draw_cloud(270, 75, 0.8)
    draw_cloud(580, 105, 0.7)

    # --------------------------------------------------------
    # Distant Island
    # --------------------------------------------------------

    pygame.draw.ellipse(
        screen,
        ISLAND_GREEN,
        (580, 275, 280, 90)
    )

    pygame.draw.ellipse(
        screen,
        ISLAND_DARK,
        (625, 265, 100, 70)
    )

    # Small island tree

    pygame.draw.line(
        screen,
        WOOD_BROWN,
        (675, 280),
        (675, 225),
        7
    )

    pygame.draw.circle(
        screen,
        PALM_GREEN,
        (650, 220),
        20
    )

    pygame.draw.circle(
        screen,
        PALM_GREEN,
        (680, 215),
        22
    )

    # --------------------------------------------------------
    # Ocean
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        OCEAN_BLUE,
        (0, 330, WIDTH, 150)
    )

    # Ocean waves

    for y in range(350, 470, 30):

        for x in range(-20, WIDTH, 80):

            pygame.draw.arc(
                screen,
                OCEAN_LIGHT,
                (x, y, 55, 15),
                0,
                3.14,
                3
            )

    # --------------------------------------------------------
    # Beach
    # --------------------------------------------------------

    pygame.draw.rect(
        screen,
        SAND,
        (0, 450, WIDTH, 200)
    )

    pygame.draw.ellipse(
        screen,
        SAND_LIGHT,
        (-100, 420, 700, 170)
    )

    pygame.draw.ellipse(
        screen,
        SAND_LIGHT,
        (350, 430, 700, 170)
    )

    # --------------------------------------------------------
    # Palm Trees
    # --------------------------------------------------------

    draw_palm_tree(35, 400, 1.2)
    draw_palm_tree(825, 410, 1.3)

    # --------------------------------------------------------
    # Small beach plants
    # --------------------------------------------------------

    pygame.draw.circle(
        screen,
        LEAF_GREEN,
        (70, 475),
        18
    )

    pygame.draw.circle(
        screen,
        LEAF_GREEN,
        (830, 480),
        18
    )


# ============================================================
# DRAW BEACH GALLows
# ============================================================

def draw_gallows():

    # Main wooden post

    pygame.draw.rect(
        screen,
        WOOD_BROWN,
        (175, 145, 20, 280),
        border_radius=5
    )

    # Horizontal branch

    pygame.draw.rect(
        screen,
        WOOD_BROWN,
        (175, 145, 170, 18),
        border_radius=5
    )

    # Wooden support

    pygame.draw.line(
        screen,
        WOOD_LIGHT,
        (190, 165),
        (240, 215),
        8
    )

    # Rope

    pygame.draw.line(
        screen,
        WOOD_BROWN,
        (330, 160),
        (330, 190),
        4
    )

    # Small leaves around gallows

    pygame.draw.circle(
        screen,
        LEAF_GREEN,
        (175, 140),
        18
    )

    pygame.draw.circle(
        screen,
        LEAF_GREEN,
        (200, 135),
        15
    )


# ============================================================
# DRAW CHARACTER
# ============================================================

def draw_character(lives_left):

    # Character is intentionally smaller

    center_x = 330

    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------

    if lives_left <= 5:

        # Head

        pygame.draw.circle(
            screen,
            SKIN,
            (center_x, 220),
            17
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (center_x, 220),
            17,
            2
        )

        # ----------------------------------------------------
        # EARS
        # ----------------------------------------------------

        pygame.draw.circle(
            screen,
            SKIN,
            (center_x - 17, 220),
            5
        )

        pygame.draw.circle(
            screen,
            SKIN,
            (center_x + 17, 220),
            5
        )

        # ----------------------------------------------------
        # SAFARI HAT
        # ----------------------------------------------------

        pygame.draw.ellipse(
            screen,
            HAT,
            (center_x - 25, 193, 50, 13)
        )

        pygame.draw.rect(
            screen,
            HAT,
            (center_x - 15, 180, 30, 22),
            border_radius=5
        )

        pygame.draw.ellipse(
            screen,
            HAT_DARK,
            (center_x - 16, 195, 32, 8)
        )

        # Hat top

        pygame.draw.arc(
            screen,
            HAT_DARK,
            (center_x - 13, 179, 26, 15),
            3.14,
            6.28,
            2
        )

        # ----------------------------------------------------
        # ROUND SUNGLASSES
        # ----------------------------------------------------

        pygame.draw.circle(
            screen,
            BLACK,
            (center_x - 7, 216),
            7
        )

        pygame.draw.circle(
            screen,
            BLACK,
            (center_x + 7, 216),
            7
        )

        pygame.draw.line(
            screen,
            BLACK,
            (center_x - 1, 216),
            (center_x + 1, 216),
            2
        )

        # Sunglasses reflection

        pygame.draw.circle(
            screen,
            WHITE,
            (center_x - 9, 214),
            2
        )

        pygame.draw.circle(
            screen,
            WHITE,
            (center_x + 5, 214),
            2
        )

        # ----------------------------------------------------
        # FACE
        # ----------------------------------------------------

        if lives_left > 0:

            # Happy smile

            pygame.draw.arc(
                screen,
                BLACK,
                (
                    center_x - 7,
                    220,
                    14,
                    10
                ),
                3.14,
                6.28,
                2
            )

        else:

            # ------------------------------------------------
            # DEAD FACE
            # Smile disappears
            # ------------------------------------------------

            # Remove smile by covering mouth area

            pygame.draw.line(
                screen,
                SKIN,
                (
                    center_x - 8,
                    226
                ),
                (
                    center_x + 8,
                    226
                ),
                4
            )

            # Sad mouth

            pygame.draw.arc(
                screen,
                BLACK,
                (
                    center_x - 6,
                    225,
                    12,
                    8
                ),
                0,
                3.14,
                2
            )

    # --------------------------------------------------------
    # BODY / PRINTED SHIRT
    # --------------------------------------------------------

    if lives_left <= 4:

        pygame.draw.rect(
            screen,
            SHIRT_GREEN,
            (
                center_x - 13,
                238,
                26,
                40
            ),
            border_radius=5
        )

        # Shirt collar

        pygame.draw.line(
            screen,
            WHITE,
            (
                center_x - 6,
                240
            ),
            (
                center_x,
                250
            ),
            2
        )

        pygame.draw.line(
            screen,
            WHITE,
            (
                center_x + 6,
                240
            ),
            (
                center_x,
                250
            ),
            2
        )

        # Tropical flower prints

        pygame.draw.circle(
            screen,
            FLOWER_PINK,
            (center_x - 7, 257),
            4
        )

        pygame.draw.circle(
            screen,
            FLOWER_YELLOW,
            (center_x + 7, 268),
            4
        )

        pygame.draw.circle(
            screen,
            FLOWER_PINK,
            (center_x + 6, 248),
            3
        )

    # --------------------------------------------------------
    # LEFT ARM
    # --------------------------------------------------------

    if lives_left <= 3:

        pygame.draw.line(
            screen,
            SHIRT_GREEN,
            (
                center_x - 12,
                243
            ),
            (
                center_x - 27,
                270
            ),
            6
        )

        pygame.draw.circle(
            screen,
            SKIN,
            (
                center_x - 27,
                270
            ),
            4
        )

    # --------------------------------------------------------
    # RIGHT ARM
    # --------------------------------------------------------

    if lives_left <= 2:

        pygame.draw.line(
            screen,
            SHIRT_GREEN,
            (
                center_x + 12,
                243
            ),
            (
                center_x + 27,
                270
            ),
            6
        )

        pygame.draw.circle(
            screen,
            SKIN,
            (
                center_x + 27,
                270
            ),
            4
        )

    # --------------------------------------------------------
    # SAFARI SHORTS
    # --------------------------------------------------------

    if lives_left <= 1:

        # Shorts

        pygame.draw.rect(
            screen,
            SHORTS,
            (
                center_x - 14,
                278,
                28,
                25
            ),
            border_radius=4
        )

        # Left cargo pocket

        pygame.draw.rect(
            screen,
            SHORTS_DARK,
            (
                center_x - 18,
                282,
                8,
                12
            ),
            border_radius=2
        )

        # Right cargo pocket

        pygame.draw.rect(
            screen,
            SHORTS_DARK,
            (
                center_x + 10,
                282,
                8,
                12
            ),
            border_radius=2
        )

        # ----------------------------------------------------
        # LEFT LEG
        # ----------------------------------------------------

        pygame.draw.line(
            screen,
            SKIN,
            (
                center_x - 6,
                302
            ),
            (
                center_x - 10,
                328
            ),
            6
        )

        # ----------------------------------------------------
        # LEFT SLIPPER
        # ----------------------------------------------------

        pygame.draw.ellipse(
            screen,
            SLIPPER_BLUE,
            (
                center_x - 18,
                326,
                18,
                9
            )
        )

    # --------------------------------------------------------
    # RIGHT LEG
    # --------------------------------------------------------

    if lives_left == 0:

        pygame.draw.line(
            screen,
            SKIN,
            (
                center_x + 6,
                302
            ),
            (
                center_x + 10,
                328
            ),
            6
        )

        # Right slipper

        pygame.draw.ellipse(
            screen,
            SLIPPER_BLUE,
            (
                center_x + 1,
                326,
                18,
                9
            )
        )


# ============================================================
# DRAW TITLE
# ============================================================

def draw_title():

    # Main title

    title = FONT_TITLE.render(
        "BEACH SAFARI HANGMAN",
        True,
        WHITE
    )

    # Shadow

    shadow = FONT_TITLE.render(
        "BEACH SAFARI HANGMAN",
        True,
        DARK_BLUE
    )

    screen.blit(
        shadow,
        (
            WIDTH // 2 - shadow.get_width() // 2 + 3,
            17
        )
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            14
        )
    )


# ============================================================
# DRAW GAME PANEL
# ============================================================

def draw_game_panel():

    # Dark blue transparent panel

    panel = pygame.Surface(
        (430, 300),
        pygame.SRCALPHA
    )

    panel.fill(
        (10, 55, 70, 225)
    )

    screen.blit(
        panel,
        (430, 145)
    )

    # Border

    pygame.draw.rect(
        screen,
        WHITE,
        (430, 145, 430, 300),
        2,
        border_radius=20
    )

    # --------------------------------------------------------
    # Hint
    # --------------------------------------------------------

    hint_label = FONT_HINT.render(
        "Hint:",
        True,
        GOLD
    )

    screen.blit(
        hint_label,
        (450, 170)
    )

    hint_text = FONT_SMALL.render(
        hint,
        True,
        WHITE
    )

    screen.blit(
        hint_text,
        (450, 200)
    )

    # --------------------------------------------------------
    # Lives
    # --------------------------------------------------------

    lives_text = FONT_UI.render(
        f"Lives Left: {lives} / 6",
        True,
        WHITE
    )

    screen.blit(
        lives_text,
        (450, 240)
    )

    # Life circles

    for i in range(6):

        x = 600 + i * 38

        if i < lives:

            pygame.draw.circle(
                screen,
                GOLD,
                (x, 249),
                10
            )

        else:

            pygame.draw.circle(
                screen,
                BUTTON_DISABLED,
                (x, 249),
                10
            )

    # --------------------------------------------------------
    # Hidden Word
    # --------------------------------------------------------

    display_str = " ".join(
        [
            c if c in guessed else "_"
            for c in secret_word
        ]
    )

    word_text = FONT_WORD.render(
        display_str,
        True,
        WHITE
    )

    screen.blit(
        word_text,
        (
            430 + (430 - word_text.get_width()) // 2,
            320
        )
    )


# ============================================================
# DRAW KEYBOARD
# ============================================================

def draw_keyboard():

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for x, y, letter, active in buttons:

        # Hover effect

        if active:

            distance = (
                (x - mouse_x) ** 2
                +
                (y - mouse_y) ** 2
            ) ** 0.5

            if distance < RADIUS:

                color = BUTTON_HOVER

            else:

                color = BUTTON_BLUE

        else:

            color = BUTTON_DISABLED

        # Button

        pygame.draw.circle(
            screen,
            color,
            (x, y),
            RADIUS
        )

        # Button outline

        pygame.draw.circle(
            screen,
            WHITE,
            (x, y),
            RADIUS,
            2
        )

        # Letter

        label = FONT_UI.render(
            letter,
            True,
            WHITE
        )

        screen.blit(
            label,
            (
                x - label.get_width() // 2,
                y - label.get_height() // 2
            )
        )


# ============================================================
# RENDER EVERYTHING
# ============================================================

def render_ui():

    draw_background()

    draw_gallows()

    draw_character(lives)

    draw_title()

    draw_game_panel()

    draw_keyboard()

    pygame.display.update()


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True

while running:

    clock.tick(60)

    render_ui()

    for event in pygame.event.get():

        # ----------------------------------------------------
        # CLOSE WINDOW
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            running = False

        # ----------------------------------------------------
        # MOUSE CLICK
        # ----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:

            mx, my = pygame.mouse.get_pos()

            for btn in buttons:

                x, y, letter, active = btn

                if active:

                    distance = (
                        (x - mx) ** 2
                        +
                        (y - my) ** 2
                    ) ** 0.5

                    if distance < RADIUS:

                        # Disable button

                        btn[3] = False

                        # Add guessed letter

                        guessed.append(letter)

                        # Wrong guess

                        if letter not in secret_word:

                            lives -= 1

    # --------------------------------------------------------
    # WIN / LOSE
    # --------------------------------------------------------

    if all(
        c in guessed
        for c in secret_word
    ):

        render_ui()

        pygame.time.delay(2500)

        break

    if lives == 0:

        render_ui()

        pygame.time.delay(2500)

        break


# ============================================================
# EXIT
# ============================================================

pygame.quit()

sys.exit()