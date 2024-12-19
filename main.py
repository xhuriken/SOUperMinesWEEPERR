import pygame, sys, time
from button import Button
from grid import Grid
from gridGame import GridGame
import json

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

        # Dessin des boutons
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

def question(grid_content,elapsed_time):
    pseudo = ""  # Stocke le pseudo saisi
    saisie_active = True  # Indique si la saisie est active
    message = "Entrez votre pseudo :"
    while saisie_active:  # Tant que la saisie est active
        for event in pygame.event.get():  # Boucle pour capturer tous les événements
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Valider avec Entrée
                    saisie_active = False
                    message = f"Pseudo enregistré : {pseudo}"
                    enregistrer_pseudo(pseudo,grid_content,elapsed_time)
                elif event.key == pygame.K_BACKSPACE:  # Effacer le dernier caractère
                    pseudo = pseudo[:-1]
                else:  # Ajouter la lettre tapée au pseudo
                    pseudo += event.unicode

            font = pygame.font.Font(None, 75)
            texte = font.render(f"{message} {pseudo}", True, (255, 255, 255))  # Afficher le pseudo
            SCREEN.blit(texte, (40, 50))

        pygame.display.update()

def enregistrer_pseudo(pseudo,grid_content,elapsed_time):
    fichier_json = "pseudo_data.json"
    try:
        with open(fichier_json, "r") as f:
            data = json.load(f)  # Lire les données existantes
    except (FileNotFoundError, json.JSONDecodeError):  # Si le fichier n'existe pas ou est vide
        data = []
    data.append({"pseudo": pseudo,
    "niveau": selected_difficulty[0],
    "temps": elapsed_time,
    "grille": grid_content})
    with open(fichier_json, "w") as f:
        json.dump(data, f, indent=4)

#Jouer
def play():
    afficher_decompte()  # Appel au décompte avant le début du jeu

    # Initialisation du timer
    start_time = time.time()  # Début du chronomètre

    print(f"Niveau de difficulté choisi: {['Debutant', 'Avance', 'Expert'][selected_difficulty[0]]}")

    # Créez une grille de jeu
    if selected_difficulty[0] == 0:
        grid = Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720, mines_count=15)
    elif selected_difficulty[0] == 1:
        grid = Grid(rows=15, cols=15, cell_size=45, window_width=1280, window_height=720)
        gridGame = GridGame(rows=15, cols=15, cell_size=45, window_width=1280, window_height=720, mines_count=45)
    else:
        grid = Grid(rows=15, cols=32, cell_size=30, window_width=1280, window_height=720)
        gridGame = GridGame(rows=15, cols=32, cell_size=30, window_width=1280, window_height=720, mines_count=99)

    grid_content = grid.grid  # Stocker le contenu de la grille

    running = True  # Indicateur pour garder le timer actif
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))

        # Chronomètre : Si le jeu est en cours, afficher le temps écoulé en secondes
        if running:
            elapsed_time = int(time.time() - start_time)  # Temps écoulé en secondes
            timer_text = get_font(35).render(f"Temps : {elapsed_time} s", True, "black")
            SCREEN.blit(timer_text, (50, 50))  # Affiche le chronomètre en haut à gauche de l'écran

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Dessiner la grille avec les mines et les chiffres
        gridGame.draw(SCREEN)

        # Créer et dessiner le bouton RETOUR
        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1185, 670),
                           text_input="RETOUR", font=get_font(60), base_color="lemonchiffon", hovering_color="deeppink")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Détection de fin de partie (victoire ou défaite)
        if gridGame.game_over:  # Si la partie est perdue
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(640, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content,elapsed_time)  # Appeler la fonction question après

        elif gridGame.victory:  # Si la partie est gagnée
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(640, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content,elapsed_time)  # Appeler la fonction question après

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
