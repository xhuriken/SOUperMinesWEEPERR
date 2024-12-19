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
    "troll": "orange",
}

BUTTON_COLORS = {
    "normal": {"base": "pink", "hover": "deeppink"},
    "troll": {"base": "gold", "hover": "orange"},
}

MUSICS = {
    "normal": "assets/normal.ogg",
    "troll": "assets/sunshine.ogg",
}

TITLES = {
    "normal": "DEMINEUR",
    "troll": "DES MINEURS"
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
    SECRET_BUTTON = Button(image=None,pos=(1150, 650),text_input="SECRET",font=get_font(20),base_color="white",hovering_color="grey"
    )

    play_music(THEME_KEYS[theme_index])  # Démarre la musique initiale

    while True:
        #Mise à jour du fond et des couleurs
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        font_color = FONT_COLORS[current_theme]
        button_colors = BUTTON_COLORS[current_theme]

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Titre
        MENU_TEXT = get_font(100).render(TITLES[current_theme], True, font_color)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #Boutons PLAY et QUIT
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit.png"), pos=(640, 600),
                             text_input="QUIT", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        CREDIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(200, 550),
                             text_input="CREDIT", font=get_font(75),
                             base_color=button_colors["base"], hovering_color=button_colors["hover"])
        SAVED_GAMES_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1080, 550),
                                    text_input="BEBETTER", font=get_font(75),
                                    base_color=button_colors["base"], hovering_color=button_colors["hover"])


        # Dessin des boutons
        for button in [PLAY_BUTTON, QUIT_BUTTON, CREDIT_BUTTON, SAVED_GAMES_BUTTON]:
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
                            base_color=button_colors["base"], hovering_color=button_colors["hover"])
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

            if i == selected_difficulty[0]:
                # Positionner le cercle devant l'option sélectionnée
                pygame.draw.circle(SCREEN, (0, 0, 0), (pos + option_width // 2 - 160, 430), 20)

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
                if CREDIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if current_music:  # Vérifie si une musique est en cours
                        current_music.stop()  # Stoppe la musique
                    credits_screen()
                if SAVED_GAMES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    load_saved_games()
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

def question(grid_content, elapsed_time):
    pseudo = ""  # Stocke le pseudo saisi
    saisie_active = True  # Indique si la saisie est active
    message = "Entrez votre pseudo :"

    font = pygame.font.Font(None, 40)  # Police utilisée pour la saisie du texte

    # Sauvegarde le fond initial (à l'emplacement où le texte apparaît)
    background_snapshot = SCREEN.copy()  # Copie de tout l'écran

    while saisie_active:  # Tant que la saisie est active
        for event in pygame.event.get():  # Boucle pour capturer tous les événements
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Valider avec Entrée
                    saisie_active = False
                    enregistrer_pseudo(pseudo, grid_content, elapsed_time)  # Sauvegarde des données
                    main_menu()  # Retour au menu principal
                elif event.key == pygame.K_BACKSPACE:  # Effacer une lettre
                    pseudo = pseudo[:-1]  # Supprime le dernier caractère
                else:  # Ajouter une lettre ou caractère au pseudo
                    pseudo += event.unicode

        # Réaffiche uniquement l'arrière-plan sous la zone de saisie
        SCREEN.blit(background_snapshot, (0, 0))  # Remet l'état du fond (invisible)

        # Affiche le pseudo et le message adapté
        texte = font.render(f"{message} {pseudo}", True, (0, 0, 0))
        SCREEN.blit(texte, (40, 50))  # Position personnalisée du texte

        pygame.display.update()  # Met à jour l'affichage pour refléter les changements


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
        grid =         Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720, mines_count=15)
    elif selected_difficulty[0] == 1:
        grid =         Grid(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720)
        gridGame = GridGame(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720, mines_count=45)
    else:
        grid =         Grid(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720)
        gridGame = GridGame(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720, mines_count=99)

    grid_content = grid.grid  # Stocker le contenu de la grille

    running = True  # Indicateur pour garder le timer actif
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        button_colors = BUTTON_COLORS[current_theme]

        # Chronomètre : Si le jeu est en cours, afficher le temps écoulé en secondes
        if running:
            elapsed_time = int(time.time() - start_time)  # Temps écoulé en secondes
            timer_text = get_font(35).render(f"Temps : {elapsed_time} s", True, "black")
            SCREEN.blit(timer_text, (1090, 40))  # Affiche le chronomètre en haut à gauche de l'écran

        PLAY_TEXT = get_font(45).render("Le jeu commence !", True, "red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # Dessiner la grille avec les mines et les chiffres
        gridGame.draw(SCREEN)

        # Créer et dessiner le bouton RETOUR
        PLAY_BACK = Button(image=None, pos=(1185, 670),
                           text_input="RETOUR", font=get_font(60), base_color=button_colors["base"], hovering_color=button_colors["hover"])

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        # Détection de fin de partie (victoire ou défaite)
        if gridGame.game_over:  # Si la partie est perdue
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(190, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content, elapsed_time)  # Appeler la fonction question après

        elif gridGame.victory:  # Si la partie est gagnée
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(190, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content, elapsed_time)  # Appeler la fonction question après

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


def credits_screen():
    pygame.init()
    SCREEN = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Crédits")

    # Couleurs et police
    BG_COLOR = "black"
    FONT_COLOR = "white"

    # Polices : une pour les textes normaux, une autre pour les titres en majuscules
    font_large = pygame.font.Font(None, 70)  # Grande police (pour les titres ou mots en majuscules)
    font_small = pygame.font.Font(None, 50)  # Petite police (pour les textes normaux)

    # Charger l'image du logo (bannière)
    logo_image = pygame.image.load("assets/riot.png")
    logo_image = pygame.transform.scale(logo_image, (500, 150))  # Ajuster la taille si nécessaire

    # Charger et jouer la musique des crédits
    pygame.mixer.music.load("assets/skibidi.mp3")  # Charger la musique
    pygame.mixer.music.play(-1)  # Jouer en boucle (-1 pour boucle infinie)

    # Crédits stylisés
    credits = [
        ("- STUDIOS -", "large"),  # 'large' signifie qu'on utilise font_large
        ("AntiMajeur x Riot Games", "small"),
        ("- DEVS -", "large"),
        ("Celestin", "small"),
        ("Antonin", "small"),
        ("Mathys", "small"),
        ("Theo", "small"),
        ("- GRAPHISTES -", "large"),
        ("Chat j'ai pété", "small"),
        ("- TESTEURS -", "large"),
        ("Ines Gangsta", "small"),
        ("- SPECIAL THANKS -", "large"),
        ("Merci aux figurants mineurs d'avoir aidé ", "small"),
        ("au développement de ce projet", "small"),
    ]

    # Variables pour défilement
    scroll_y = 720  # Point de départ en bas de l'écran
    scroll_speed = 0.7  # Vitesse de défilement

    # Boucle principale
    clock = pygame.time.Clock()
    while True:
        SCREEN.fill(BG_COLOR)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Détection clic sur le bouton RETOUR
                mouse_pos = pygame.mouse.get_pos()
                if retour_rect.collidepoint(mouse_pos):
                    pygame.mixer.music.stop()  # Arrêter la musique des crédits
                    play_music(THEME_KEYS[theme_index])  # Relancer la musique du menu principal
                    return  # Retourner au menu principal

        # Afficher le logo (bannière) fixe en haut-centre
        logo_rect = logo_image.get_rect(center=(640, scroll_y - 200))  # Positionner un peu avant les crédits
        SCREEN.blit(logo_image, logo_rect)

        # Affichage des crédits défilants
        for i, (text, size) in enumerate(credits):
            # Sélectionner la taille de la police en fonction du type (large/small)
            if size == "large":
                text_surface = font_large.render(text, True, FONT_COLOR)
            else:
                text_surface = font_small.render(text, True, FONT_COLOR)

            # Calculer la position (chaque élément est espacé verticalement de 80 pixels)
            text_rect = text_surface.get_rect(center=(640, scroll_y + i * 80))
            SCREEN.blit(text_surface, text_rect)

        # Mise à jour de la position verticale pour le défilement
        scroll_y -= scroll_speed

        # Remettre en boucle quand tout est défilé
        if scroll_y + len(credits) * 80 < -100:  # Recommence quand tout est hors de l'écran
            scroll_y = 720

        # Bouton 'Retour' en haut à droite
        retour_font = pygame.font.Font(None, 40)
        retour_text = retour_font.render("RETOUR", True, "white")
        retour_rect = retour_text.get_rect(topright=(1250, 20))  # Positionné en haut-droite
        SCREEN.blit(retour_text, retour_rect)

        # Mise à jour de l'écran
        pygame.display.flip()
        clock.tick(60)


def load_saved_games():
    fichier_json = "pseudo_data.json"
    try:
        with open(fichier_json, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    while True:
        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        button_colors = BUTTON_COLORS[current_theme]

        draw_text("Parties Enregistrees", get_font(50), "black", SCREEN, 640, 50)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(650, 650), text_input="RETOUR", font=get_font(75), base_color=button_colors["base"], hovering_color=button_colors["hover"])

        BACK_BUTTON.changeColor(MENU_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        # Afficher chaque partie
        y_offset = 150  # Position verticale de départ
        buttons = []
        for i, game in enumerate(data):
            pseudo = game["pseudo"]
            niveau = ["Debutant", "Avance", "Expert"][game["niveau"]]
            temps = game["temps"]

            # Texte descriptif de la partie
            draw_text(f"{pseudo} - {niveau} - {temps}s", get_font(30), "black", SCREEN, 640, y_offset)

            # Créer un bouton pour rejouer la partie
            replay_button = Button(image=None,pos=(1000, y_offset), text_input="REJOUER", font=get_font(30), base_color="green", hovering_color="darkgreen")
            replay_button.changeColor(MENU_MOUSE_POS)
            replay_button.update(SCREEN)
            buttons.append((replay_button, game))
            y_offset += 70

        # Gestion des clics
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                for button, game in buttons:
                    if button.checkForInput(MENU_MOUSE_POS):
                        replay_game(game)  # Rejouer la partie

        pygame.display.update()


def replay_game(game):
    start_time = time.time()  # Début du chronomètre

    grid_content = game["grille"]
    niveau = game["niveau"]
    elapsed_time = game["temps"]

    # Configure la grille et GridGame en fonction du niveau
    if niveau == 0:
        grid =         Grid(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720)
        gridGame = GridGame(rows=9, cols=9, cell_size=50, window_width=1280, window_height=720, mines_count=15)
    elif niveau == 1:
        grid =         Grid(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720)
        gridGame = GridGame(rows=16, cols=16, cell_size=45, window_width=1280, window_height=720, mines_count=45)
    else:
        grid =         Grid(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720)
        gridGame = GridGame(rows=30, cols=16, cell_size=30, window_width=1280, window_height=720, mines_count=99)

    grid.grid = grid_content  # Charger la grille sauvegardée
    running = True

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        current_theme = THEME_KEYS[theme_index]
        SCREEN.blit(BACKGROUND_IMAGES[current_theme], (0, 0))
        print(PLAY_MOUSE_POS)
        # Afficher la grille
        gridGame.draw(SCREEN)

        PLAY_BACK = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(1185, 670),
                           text_input="RETOUR", font=get_font(60), base_color="lemonchiffon", hovering_color="deeppink")

        PLAY_BACK.changeColor(pygame.mouse.get_pos())
        PLAY_BACK.update(SCREEN)
        if running:
            elapsed_time = int(time.time() - start_time)  # Temps écoulé en secondes
            timer_text = get_font(35).render(f"Temps : {elapsed_time} s", True, "black")
            SCREEN.blit(timer_text, (1090, 40))  # Affiche le chronomètre en haut à gauche de l'écran

        if gridGame.game_over:  # Si la partie est perdue
            font = pygame.font.Font(None, 100)
            text = font.render("Perdu !", True, "red")
            text_rect = text.get_rect(center=(190, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content, elapsed_time)  # Appeler la fonction question après

        elif gridGame.victory:  # Si la partie est gagnée
            font = pygame.font.Font(None, 100)
            text = font.render("Victoire !", True, "green")
            text_rect = text.get_rect(center=(190, 360))  # Texte centré
            SCREEN.blit(text, text_rect)  # Afficher le texte
            running = False  # Arrêter le chronomètre
            question(grid_content, elapsed_time)  # Appeler la fonction question après

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
