import pygame, sys
from button import Button
from grid import Grid

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/backkground.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def play():
    grid = Grid(rows=10, cols=10, cell_size=50, window_width=1280, window_height=720)  # Crée une grille 10x10
    grid.populate_mines(mine_count=15)  # Place 15 mines
    grid.calculate_adjacent_numbers()  # Calcule les nombres des cases adjacentes

    #grid.debug_display()  # Optionnel : Affiche la grille dans la console pour vérification

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")  # Fond noir

        # Dessiner la grille avec les mines et les chiffres
        grid.draw(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 670),
                           text_input="RETOUR", font=get_font(50), base_color="White", hovering_color="yellow")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Détecter les clics de souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si le clic est sur le bouton retour
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

                # Vérifier si le clic est sur une cellule de la grille
                cell = grid.get_cell_from_position(*PLAY_MOUSE_POS)
                if cell:  # Si une cellule est cliquée
                    row, col = cell
                    print(f"Cellule cliquée : {row}, {col}")  # Afficher les indices de la cellule cliquée
                    # Ajoutez ici toute logique pour interagir avec la grille
                    # Par exemple, révéler une cellule ou marquer une mine

        pygame.display.update()



def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("DES MINEURS", True, "red")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="lemonchiffon", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550),
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