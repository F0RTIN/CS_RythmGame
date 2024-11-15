import pygame
import sys
import tkinter as tk
import csv

from tkinter import simpledialog,ttk
from random import randrange

pygame.init()

Screen_Width = 545
Screen_Height = 900

screen = pygame.display.set_mode((Screen_Width, Screen_Height))
font = pygame.font.Font(None, 120)

# Load images
start_img = pygame.image.load('GamePython/image/start_btn.png').convert_alpha()
leaderboard_img = pygame.image.load('GamePython/image/leaderboard_btn.png').convert_alpha()
GButton_img = pygame.image.load('GamePython/image/GButton.png').convert_alpha()
BButton_img = pygame.image.load('GamePython/image/BButton.png').convert_alpha()
RButton_img = pygame.image.load('GamePython/image/RButton.png').convert_alpha()
YButton_img = pygame.image.load('GamePython/image/YButton.png').convert_alpha()

# Pressed versions of images
BButton_img_pressed = pygame.image.load('GamePython/image/BButton_pressed.png').convert_alpha()
YButton_img_pressed = pygame.image.load('GamePython/image/YButton_pressed.png').convert_alpha()
GButton_img_pressed = pygame.image.load('GamePython/image/GButton_pressed.png').convert_alpha()
RButton_img_pressed = pygame.image.load('GamePython/image/RButton_pressed.png').convert_alpha()

# Moving tiles
BFrame_img = pygame.image.load('GamePython/image/BFrame.png').convert_alpha()
YFrame_img = pygame.image.load('GamePython/image/YFrame.png').convert_alpha()
GFrame_img = pygame.image.load('GamePython/image/GFrame.png').convert_alpha()
RFrame_img = pygame.image.load('GamePython/image/RFrame.png').convert_alpha()

# Countdown not used in the final product
One_img = pygame.image.load('GamePython/image/1.png').convert_alpha()
Two_img = pygame.image.load('GamePython/image/2.png').convert_alpha()
Three_img = pygame.image.load('GamePython/image/3.png').convert_alpha()
Go_img = pygame.image.load('GamePython/image/GO.png').convert_alpha()



# GameObject base class
class GameObject:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Button class inheriting from GameObject
class Button(GameObject):
    def __init__(self, x, y, image, scale, action=None, pressed_image=None):
        super().__init__(x, y, image, scale)
        self.original_image = self.image
        self.pressed_image = pygame.transform.scale(pressed_image, (self.rect.width, self.rect.height)) if pressed_image else image
        self.pressed = False
        self.action = action
        self.selected = False
        self.blink_timer = 0
        self.visible = True

    def draw(self, screen):
        if self.selected:
            current_time = pygame.time.get_ticks()
            if current_time - self.blink_timer > 500:
                self.blink_timer = current_time
                self.visible = not self.visible
        else:
            self.visible = True

        if self.visible:
            screen.blit(self.pressed_image if self.pressed else self.original_image, (self.rect.x, self.rect.y))

    # Press and release state to change the image of the object
    def press(self):
        self.pressed = True

    def release(self):
        self.pressed = False
        if self.action:
            self.action()

# Player class to stock name and score
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

# Create a Player instance to be able to use it
player = Player(name="Player1", score=0)



# Define actions for buttons
def start_game():
    global current_page
    current_page = "start_page"

def go_to_menu():
    global current_page
    current_page = "menu"

def blue_action():
    if pygame.sprite.collide_rect(start_page_buttons[0], start_page_buttons[4]):
        player.score += 10
    print("Blue button pressed")

def yellow_action():
    if pygame.sprite.collide_rect(start_page_buttons[1], start_page_buttons[5]):
        player.score += 10
    print("Yellow button pressed")

def green_action():
    if pygame.sprite.collide_rect(start_page_buttons[2], start_page_buttons[6]):
        player.score += 10
    print("Green button pressed")

def red_action():
    if pygame.sprite.collide_rect(start_page_buttons[3], start_page_buttons[7]):
        player.score += 10
    print("Red button pressed")



# Functionnality methods
def load_csv_data(treeview, csv_file):
    #Open SCV file
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        # Clean past values
        for item in treeview.get_children():
            treeview.delete(item)
        
        # Get column names
        columns = next(reader)
        treeview["columns"] = columns
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor="w")

        # Getting the data
        data = [row for row in reader]
        
        # Sorting the scores
        data.sort(key=lambda x: int(x[1]), reverse=True)

        # Get that data into the treeview
        for row in data:
            treeview.insert("", "end", values=row)

def show_leaderboard():
    # Create the window
    root = tk.Tk()
    root.title("Leaderboard")
    notebook = ttk.Notebook(root)

    # Create a frame
    leaderboard_frame = ttk.Frame(notebook)
    notebook.add(leaderboard_frame, text="Leaderboard")

    # Create a Treeview widget for leaderboard data
    treeview = ttk.Treeview(leaderboard_frame, show="headings")
    treeview.pack(expand=True, fill="both")

    # Load the CSV data into the Treeview
    csv_file = 'GamePython/leaderboard.csv'
    load_csv_data(treeview, csv_file)

    # Pack the notebook into window
    notebook.pack(expand=True, fill="both")

    root.mainloop()

def handle_game():

    global speed1, speed2, speed3,speed4, start_time, current_page, username_entered

    #Handling time, score display and saving the score and username
    if ((pygame.time.get_ticks() - start_time) / 1000 > 20) and not username_entered:
        screen.fill((202, 228, 241))
        for button in start_page_buttons:
            button.draw(screen)

        if 0 <= player.score < 100:
            text_surface = font.render(str(player.score), True, (0, 0, 0))
            screen.blit(text_surface, (240, 300))
        elif player.score >= 100:
            text_surface = font.render(str(player.score), True, (0, 0, 0))
            screen.blit(text_surface, (120, 300))
        else:
            text_surface = font.render(str(player.score), True, (0, 0, 0))
            screen.blit(text_surface, (255, 300))

        # Show username input dialog
        root = tk.Tk()
        root.withdraw()
        player.name = simpledialog.askstring("username", "Enter your username")
        print(player.name)

        if player.name:
            with open('GamePython/leaderboard.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([player.name, player.score])

            # I had issue with loops so I set a flag to prevent re-entering username
            username_entered = True
            # Go back to menu page
            current_page = "menu"


    # Check and reset the position of each tile if needed and assign a new random individual speed
    if start_page_buttons[4].rect.y >= 850:
        start_page_buttons[4].rect.y = 100
        speed1=randrange(4,8)

    if start_page_buttons[5].rect.y >= 850:
        start_page_buttons[5].rect.y = 100
        speed2=randrange(4,8) 

    if start_page_buttons[6].rect.y >= 850:
        start_page_buttons[6].rect.y = 100
        speed3=randrange(4,8)  

    if start_page_buttons[7].rect.y >= 850:
        start_page_buttons[7].rect.y = 100
        speed4=randrange(4,8)

    # Move each tile down by its respective speed
    start_page_buttons[4].rect.y += speed1
    start_page_buttons[5].rect.y += speed2
    start_page_buttons[6].rect.y += speed3
    start_page_buttons[7].rect.y += speed4

    # Draw the score on the screen depending on the size of the score
    if(player.score>=0 & player.score<100):
        text_surface = font.render(str(player.score), True, (0, 0, 0))
        screen.blit(text_surface, (240, 300))

    elif(player.score>=100):
        text_surface = font.render(str(player.score), True, (0, 0, 0))
        screen.blit(text_surface, (120, 300))

    else:
        text_surface = font.render(str(player.score), True, (0, 0, 0))
        screen.blit(text_surface, (255, 300))

    
# Button instances for the menu
menu_buttons = [
    Button(90, 200, start_img, 2.2, action=start_game),
    Button(150, 500, leaderboard_img, 0.5,action=show_leaderboard)
]

# Button instances for the game page
start_page_buttons = [
    Button(50, 800, BButton_img, 0.1, action=blue_action, pressed_image=BButton_img_pressed),
    Button(170, 800, YButton_img, 0.1, action=yellow_action, pressed_image=YButton_img_pressed),
    Button(290, 800, GButton_img, 0.1, action=green_action, pressed_image=GButton_img_pressed),
    Button(410, 800, RButton_img, 0.1, action=red_action, pressed_image=RButton_img_pressed),
    GameObject(50, 100, BFrame_img, 0.11),
    GameObject(170, 100, YFrame_img, 0.11),
    GameObject(290, 100, GFrame_img, 0.11),
    GameObject(410, 100, RFrame_img, 0.11)
]

# Initialize first selected button
current_button_index = 0
menu_buttons[current_button_index].selected = True

# Track the current page
current_page = "menu"

# Game time initialization
clock = pygame.time.Clock()
start_time=None

# Assign initial random speeds for each tile independently
speed1=randrange(4,8) 
speed2=randrange(4,8) 
speed3=randrange(4,8) 
speed4=randrange(4,8)

# Add a flag to track if the username has been recorded (had issue with infinite loops)
username_entered = False

# Main game loop
run = True
while run:
    screen.fill((202, 228, 241))

    if current_page == "menu":
        for button in menu_buttons:
            button.draw(screen)
    elif current_page == "start_page":
        for button in start_page_buttons:
            button.draw(screen)

        if start_time is None:
            start_time = pygame.time.get_ticks()  # Record start time


        handle_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if current_page == "menu":
                if event.key == pygame.K_UP:
                    menu_buttons[current_button_index].selected = False
                    current_button_index = (current_button_index + 1) % len(menu_buttons)
                    menu_buttons[current_button_index].selected = True
                elif event.key == pygame.K_DOWN:
                    menu_buttons[current_button_index].selected = False
                    current_button_index = (current_button_index - 1) % len(menu_buttons)
                    menu_buttons[current_button_index].selected = True
                elif event.key == pygame.K_RETURN:
                    menu_buttons[current_button_index].release()
            elif current_page == "start_page":
                if event.key == pygame.K_c:
                    start_page_buttons[0].press()
                elif event.key == pygame.K_v:
                    start_page_buttons[1].press()
                elif event.key == pygame.K_b:
                    start_page_buttons[2].press()
                elif event.key == pygame.K_n:
                    start_page_buttons[3].press()
            elif current_page == "leaderbard" and event.key==pygame.K_ESCAPE:
                go_to_menu()
                
        elif event.type == pygame.KEYUP:
            if current_page == "start_page":
                if event.key == pygame.K_c:
                    start_page_buttons[0].release()
                    print(player.score)
                elif event.key == pygame.K_v:
                    start_page_buttons[1].release()
                elif event.key == pygame.K_b:
                    start_page_buttons[2].release()
                elif event.key == pygame.K_n:
                    start_page_buttons[3].release()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
