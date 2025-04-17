import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
import numpy as np
import random

# Set up figure
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.patch.set_facecolor("black")

# Game state variables
ship = None
bullets = []
enemies = []
keys_pressed = set()
score = 0
game_over = False
enemy_speed = 0.3  # Easier

# UI elements
score_text = None
game_over_text = None
instruction_text = None

# Restart button setup (always hidden)
restart_ax = plt.axes([0.4, 0.05, 0.2, 0.075])
restart_button = Button(restart_ax, 'Restart', color='black', hovercolor='black')  # Hidden


# --- Event Handlers ---
def on_key(event):
    keys_pressed.add(event.key)


def on_key_release(event):
    keys_pressed.discard(event.key)


fig.canvas.mpl_connect("key_press_event", on_key)
fig.canvas.mpl_connect("key_release_event", on_key_release)


# --- Game Functions ---
def create_ship():
    return patches.Polygon([[50, 5], [47, 0], [53, 0]], color="white")


def create_enemy():
    x = random.randint(10, 90)
    enemy = patches.Circle((x, 100), 4, color="red")  # Larger target
    ax.add_patch(enemy)
    enemies.append(enemy)


def hide_restart_button():
    restart_button.ax.set_facecolor('black')       # Match background
    restart_button.hovercolor = 'black'            # Prevent hover color
    restart_button.label.set_color('black')        # Hide text
    fig.canvas.draw_idle()


def show_restart_button():
    restart_button.ax.set_facecolor('lightgray')   # Make visible
    restart_button.hovercolor = 'lightblue'        # Hover effect
    restart_button.label.set_color('black')        # Show text
    fig.canvas.draw_idle()


def reset_game(event=None):
    global ship, bullets, enemies, score, game_over
    ax.clear()
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    fig.patch.set_facecolor("black")

    bullets.clear()
    enemies.clear()
    keys_pressed.clear()
    score = 0
    game_over = False

    # Create player ship
    ship = create_ship()
    ax.add_patch(ship)

    # Create UI
    global score_text, game_over_text, instruction_text
    score_text = ax.text(5, 95, f"Score: {score}", color="white", fontsize=12)
    game_over_text = ax.text(50, 50, "", color="red", fontsize=20, ha="center")
    instruction_text = ax.text(50, 90, "← → to move, SPACE to shoot", color="lightblue", fontsize=10, ha="center")

    hide_restart_button()


def update(frame):
    global score, game_over

    if game_over:
        return

    # Move ship
    ship_xy = ship.get_xy()
    if "left" in keys_pressed and ship_xy[0][0] > 0:
        ship.set_xy([[p[0] - 1, p[1]] for p in ship_xy])
    if "right" in keys_pressed and ship_xy[2][0] < 100:
        ship.set_xy([[p[0] + 1, p[1]] for p in ship_xy])

    # Shoot
    if " " in keys_pressed:
        x = ship.get_xy()[0][0]
        bullet = patches.Rectangle((x - 1, 6), 2, 6, color="yellow")  # Bigger bullets
        ax.add_patch(bullet)
        bullets.append(bullet)
        keys_pressed.discard(" ")

    # Move bullets
    for bullet in bullets[:]:
        bullet.set_y(bullet.get_y() + 2)
        if bullet.get_y() > 100:
            bullet.remove()
            bullets.remove(bullet)

    # Spawn enemies
    if random.random() < 0.02:
        create_enemy()

    # Move enemies
    for enemy in enemies[:]:
        x, y = enemy.center
        enemy.center = (x, y - enemy_speed)
        if y < 0:
            game_over = True
            game_over_text.set_text("GAME OVER!")
            show_restart_button()
            break

    # Collision detection
    for bullet in bullets[:]:
        bx, by = bullet.get_x(), bullet.get_y()
        for enemy in enemies[:]:
            ex, ey = enemy.center
            if abs(bx - ex) < 4 and abs(by - ey) < 4:
                bullet.remove()
                bullets.remove(bullet)
                enemy.remove()
                enemies.remove(enemy)
                score += 1
                score_text.set_text(f"Score: {score}")
                break


# --- Launch Game ---
restart_button.on_clicked(reset_game)
reset_game()
ani = FuncAnimation(fig, update, interval=30)
plt.show()
