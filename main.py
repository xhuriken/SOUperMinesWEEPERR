import pygame, sys, time
from button import Button
from grid import Grid
from gridGame import GridGame

pygame.init()

# Fenêtre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

# Change background
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

# Niveau de difficulté
selected_difficulty = [0]  # Débutant par défaut

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

        options = ["Debutant(9x9)", "Avance(16x16)", "Expert(30x16)"]
        num_options = len(options)
        option_width = 350  # Largeur de chaque option
        total_width = num_options * option_width  # Largeur totale de toutes les options
        start_x = (1280 - total_width) // 2  # Calcul de la position de départ pour centrer les options

        draw_text("Selectionnez une difficulte", get_font(50), font_color, SCREEN, 640, 350)

        for i, (text, pos) in enumerate(zip(options, range(start_x, start_x + total_width, option_width))):
            button = Button(image=None, pos=(pos + option_width // 2, 425),
                            text_input=text, font=get_font(40),
                            base_color="pink", hovering_color="deeppink")
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            if i == selected_difficulty[0]:
                # Positionner le cercle devant l'option sélectionnée
                pygame.draw.circle(SCREEN, (255, 20, 147), (pos + option_width // 2 - 160, 430), 20)

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
                    # Sélectionner une difficulté
                for i, pos in enumerate(range(start_x, start_x + total_width, option_width)):
                    if (MENU_MOUSE_POS[0] - (pos + option_width // 2)) ** 2 + (
                            MENU_MOUSE_POS[1] - 425) ** 2 <= 20 ** 2:
                        selected_difficulty[0] = i  # Met à jour la difficulté

        pygame.display.update()


#Decompte
def afficher_decompte():
    current_theme = THEME_KEYS[theme_index]  # Récupère le thème actuel
    for i in range(3, 0, -1):
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        draw_text(str(i), get_font(100), "black", SCREEN, 640, 360)
        pygame.display.flip()
        time.sleep(1)

#Jouer
def play():
    afficher_decompte()
    print(f"Niveau de difficulté choisi: {['Debutant', 'Avance', 'Expert'][selected_difficulty[0]]}")
    # Créez une grille de jeu
    if selected_difficulty[0] == 0:
        grid = Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)# Crée une grille 10x10
        grid.populate_mines(mine_count=10)  # Place 15 mines
        grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes
    elif selected_difficulty[0] == 1:
        grid = Grid(rows=16, cols=16, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=16, cols=16, cell_size=45, window_width=1280,
                            window_height=720)  # Crée une grille 10x10
        grid.populate_mines(mine_count=40)  # Place 40 mines
        grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes
    else :
        grid = Grid(rows=30, cols=16, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=30, cols=16, cell_size=30, window_width=1280,
                            window_height=720)  # Crée une grille 10x10
        grid.populate_mines(mine_count=99)  # Place 15 mines
        grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes

    # **Ajoutez cet appel ici**
    #gridGame.initialize_grid(grid)

    # DEBUG : Affichez la grille de jeu avec les mines
    print("Grille après ajout des mines :")
    for row in grid.grid:
        print(row)

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)
        # Dessiner la grille avec les mines et les chiffres
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
