import pygame, sys, time
from button import Button

pygame.init()

# Configuration de la fenêtre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Chargement des assets
BG = pygame.image.load("assets/background.png")
sunshine_song = pygame.mixer.Sound("assets/sunshine.ogg")
sunshine_song.play()


# Fonction pour obtenir une police
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
    afficher_decompte()  # Affiche le décompte avant de démarrer le jeu
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("lemonchiffon")

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 460),
                           text_input="RETOUR", font=get_font(75), base_color="lemonchiffon", hovering_color="red")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

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
