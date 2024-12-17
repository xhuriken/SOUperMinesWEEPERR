import pygame, sys, time
from button import Button
from grid import Grid
from gridGame import GridGame

pygame.init()

# Configuration de la fenêtre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Chargement des assets
BG = pygame.image.load("assets/background.png")
sunshine_song = pygame.mixer.Sound("assets/sunshine.ogg")
sunshine_song.play()


def get_font(size):
    return pygame.font.Font("assets/norwester.otf", size)

# Fonction pour dessiner du texte
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Fonction de décompte
def afficher_decompte():
    for i in range(3, 0, -1):
        SCREEN.fill("lemonchiffon")  # Efface l'écran avec du blanc
        draw_text(str(i), get_font(100), "red", SCREEN, 640, 360)
        pygame.display.flip()  # Met à jour l'écran
        time.sleep(1)  # Pause de 1 seconde
    SCREEN.fill("lemonchiffon")
    draw_text("Perd pas encule", get_font(100), "green", SCREEN, 640, 360)
    pygame.display.flip()
    time.sleep(1)  # Pause avant de lancer le jeu


def play():
    #afficher_decompte()  # Affiche le décompte avant de démarrer le jeu
    grid = Grid(rows=10, cols=10, cell_size=50, window_width=1280, window_height=720)
    gridGame = GridGame(rows=10, cols=10, cell_size=50, window_width=1280, window_height=720)# Crée une grille 10x10
    grid.populate_mines(mine_count=15)  # Place 15 mines
    grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes
    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")  # Fond noir

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        # Dessiner la grille avec les mines et les chiffres
        gridGame.draw(SCREEN)

        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 670),
                           text_input="RETOUR", font=get_font(75), base_color="lemonchiffon", hovering_color="red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Détecter les clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Vérifier si le clic est sur le bouton retour
                    if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                        main_menu()

                    # Vérifier si le clic est sur une cellule de la grille
                    cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                    if cell:  # Si une cellule est cliquée
                        row, col = cell
                        gridGame.changeValue(row, col, grid)
        pygame.display.update()

# Fonction pour gérer le menu principal
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("DES MINEURS", True, "red")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="lemonchiffon", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="lemonchiffon", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()