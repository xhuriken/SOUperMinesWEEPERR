import pygame, sys, time
from button import Button
from grid import Grid
from gridGame import GridGame

pygame.init()

#Fenetre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

#Change background
BACKGROUND_IMAGES = {
    "normal": pygame.image.load("assets/fond.png"),
    "troll": pygame.image.load("assets/backkground.png"),
}

FONT_COLORS = {
    "normal": "deeppink",
    "troll": "yellow",
}

BUTTON_COLORS = {
    "normal": {"base": "pink", "hover": "deeppink"},
    "troll": {"base": "lemonchiffon", "hover": "yellow"},
}

MUSICS = {
    "normal": "assets/normal.ogg",
    "troll": "assets/sunshine.ogg",
}

THEME_KEYS = list(BACKGROUND_IMAGES.keys())  # Liste des thèmes
theme_index = 0  # Index du thème actuel (commence à 0)
current_music = None  # Musique actuellement en lecture


#Jouer musique
def play_music(theme):
    global current_music
    if current_music:
        current_music.stop()
    current_music = pygame.mixer.Sound(MUSICS[theme])
    current_music.play(-1)  # -1 pour jouer en boucle


#Police
def get_font(size):
    return pygame.font.Font("assets/norwester.otf", size)


#Texte
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)
#Changer theme
def changer_theme():
    global theme_index
    theme_index = (theme_index + 1) % len(THEME_KEYS)  # Passe au thème suivant
    play_music(THEME_KEYS[theme_index])  # Change la musique


#Menu principal
def main_menu():
    bouton_secret_visible = False  # Le bouton est invisible au début
    SECRET_KEY = pygame.K_t  # Touche pour révéler le bouton

    #Bouton secret
    SECRET_BUTTON = Button(
        image=None,
        pos=(1150, 650),
        text_input="SECRET",
        font=get_font(20),
        base_color="white",
        hovering_color="grey"
    )

    play_music(THEME_KEYS[theme_index])  # Démarre la musique initiale

    while True:
        #Mise à jour du fond et des couleurs
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        font_color = FONT_COLORS[current_theme]
        button_colors = BUTTON_COLORS[current_theme]

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        #Titre
        MENU_TEXT = get_font(100).render("DES MINEURS", True, font_color)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #Boutons PLAY et QUIT
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])

        #Dessin des boutons
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        #Affichage du bouton secret
        if bouton_secret_visible:
            SECRET_BUTTON.changeColor(MENU_MOUSE_POS)
            SECRET_BUTTON.update(SCREEN)

        #Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == SECRET_KEY:
                    bouton_secret_visible = True  # Révélation du bouton secret
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if bouton_secret_visible and SECRET_BUTTON.checkForInput(MENU_MOUSE_POS):
                    changer_theme()  # Change le thème

        pygame.display.update()


#Decompte
def afficher_decompte():
    current_theme = THEME_KEYS[theme_index]  # Récupère le thème actuel
    for i in range(3, 0, -1):
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        draw_text(str(i), get_font(100), "black", SCREEN, 640, 360)
        pygame.display.flip()
        time.sleep(1)

def play():
    # Créez une grille de jeu
    grid = Grid(rows=5, cols=5, cell_size=50, window_width=1280, window_height=720)
    gridGame = GridGame(rows=5, cols=5, cell_size=50, window_width=1280,
                        window_height=720)  # Grille de gestion de jeu
    grid.populate_mines(mine_count=1)  # Place 15 mines
    grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes

    # **Ajoutez cet appel ici**
    #gridGame.initialize_grid(grid)

    # DEBUG : Affichez la grille de jeu avec les mines
    print("Grille après ajout des mines :")
    for row in grid.grid:
        print(row)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")  # Nettoyer l'écran avec un fond noir

        # Dessiner la grille et son contenu
        gridGame.draw(SCREEN)

        # Créer et dessiner le bouton RETOUR
        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 670),
                           text_input="RETOUR", font=get_font(75), base_color="lemonchiffon", hovering_color="red")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # **Texte de fin de partie**
        if gridGame.game_over:  # Si la partie est perdue
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(640, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte

        elif gridGame.victory:  # Si la partie est gagnée
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(640, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Détecter les clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Si on clique sur le bouton RETOUR
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                # Bloquer les interactions avec la grille après la victoire ou la défaite
                if not gridGame.game_over and not gridGame.victory:
                    if event.button == 1:  # Clic gauche
                        cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                        if cell:  # Si une cellule a été cliquée
                            row, col = cell
                            if not gridGame.revealed[row][col]:
                                gridGame.changeValue(row, col, grid)

                    elif event.button == 3:  # Clic droit
                        cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                        if cell:
                            row, col = cell
                            gridGame.toggle_flag(row, col)

        pygame.display.update()

#Lancement menu
main_menu()
