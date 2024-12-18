import pygame
import random

import grid
from grid import Grid


class GridGame:
    def __init__(self, rows, cols, cell_size, window_width, window_height):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.generate_empty_grid()
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.offset_x = (window_width - (cols * cell_size)) // 2
        self.offset_y = (window_height - (rows * cell_size)) // 2
        self.game_over = False
        self.victory = False
        self.first_click = True  # État du premier clic (initialement True)
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions (haut, bas, gauche, droite)
        self.diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonales

    def propagate_zeros(self, row, col, grid_instance):
        """
        Propage toutes les cases de valeur 0 autour d'une case initiale
        et révèle également les chiffres aux bordures des zones propagées.
        """
        all_directions = self.directions + self.diagonal_directions
        cells_to_check = [(row, col)]
        visited = set()

        while cells_to_check:
            current_row, current_col = cells_to_check.pop(0)

            # Ignorez les cases déjà visitées
            if (current_row, current_col) in visited:
                continue

            visited.add((current_row, current_col))

            # Révéler la case si elle est valide
            if 0 <= current_row < self.rows and 0 <= current_col < self.cols:
                self.revealed[current_row][current_col] = True
                self.grid[current_row][current_col] = grid_instance.grid[current_row][current_col]

                # Si la case est un 0, ajoutez ses voisins à la pile pour la propagation
                if grid_instance.grid[current_row][current_col] == 0:
                    for dr, dc in self.directions:
                        neighbor_row, neighbor_col = current_row + dr, current_col + dc
                        if (neighbor_row, neighbor_col) not in visited:
                            cells_to_check.append((neighbor_row, neighbor_col))

                # Révéler les chiffres autour des bordures
                for dr, dc in all_directions:
                    border_row, border_col = current_row + dr, current_col + dc
                    if (border_row, border_col) not in visited and 0 <= border_row < self.rows and 0 <= border_col < self.cols:
                        if grid_instance.grid[border_row][border_col] > 0:  # Révéler uniquement les chiffres
                            self.revealed[border_row][border_col] = True
                            self.grid[border_row][border_col] = grid_instance.grid[border_row][border_col]

    def draw(self, surface):
        """Affiche la grille avec les cases colorées, révélées et les drapeaux."""
        font = pygame.font.Font(None, 40)  # Police pour afficher les chiffres
        for row in range(self.rows):
            for col in range(self.cols):
                # Coordonnées de l'emplacement de la case
                rect = pygame.Rect(
                    self.offset_x + col * self.cell_size,
                    self.offset_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                if self.revealed[row][col]:
                    # Cases révélées : affichage transparent + contenu
                    color = "black"  # Couleur de fond
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)  # Bordure blanche

                    # Contenu de la case
                    if self.grid[row][col] == -1:  # Mine détectée
                        pygame.draw.circle(
                            surface,
                            "red",  # Couleur de la mine
                            (
                                self.offset_x + col * self.cell_size + self.cell_size // 2,
                                self.offset_y + row * self.cell_size + self.cell_size // 2),
                            self.cell_size // 3
                        )
                    elif self.grid[row][col] > 0:  # Nombre détecté
                        text = font.render(str(self.grid[row][col]), True, "yellow")  # Texte jaune
                        text_rect = text.get_rect(center=(
                            self.offset_x + col * self.cell_size + self.cell_size // 2,
                            self.offset_y + row * self.cell_size + self.cell_size // 2
                        ))
                        surface.blit(text, text_rect)
                elif self.flags[row][col]:
                    # Cases avec un drapeau
                    color = "purple"  # Couleur de fond des cases non révélées
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)  # Bordure blanche

                    # Dessiner un drapeau
                    pygame.draw.polygon(
                        surface,
                        "red",  # Couleur du drapeau
                        [
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + self.cell_size // 4),
                            (self.offset_x + col * self.cell_size + 3 * self.cell_size // 4,
                             self.offset_y + row * self.cell_size + self.cell_size // 3),
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + self.cell_size // 2),
                        ]
                    )
                else:
                    # Cases non révélées : affichage coloré
                    color = "purple"
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)  # Bordure blanche

    def changeValue(self, row, col, grid_instance):
        """Gère le clic sur une case, génère la grille lors du premier clic."""
        if self.flags[row][col] or self.game_over or self.victory:
            return  # Ignorer si la case est déjà marquée avec un drapeau ou si la partie est terminée

        if self.first_click:
            self.first_click = False  # Marque le premier clic comme effectué

            # Générer les mines après le clic initial
            grid_instance.populate_mines_avoiding(row, col, mine_count=10)

            # Calculer les chiffres autour des mines
            grid_instance.calculate_adjacent_numbers()

        # Propagez des 0 à partir de la case cliquée (si c'est un 0)
        if grid_instance.grid[row][col] == 0:
            self.propagate_zeros(row, col, grid_instance)
        else:
            # Révéler la case cliquée directement
            self.grid[row][col] = grid_instance.grid[row][col]
            self.revealed[row][col] = True

        # Si la case cliquée contient une bombe
        if grid_instance.grid[row][col] == -1:
            self.game_over = True
            return

        # Vérifier si la victoire est atteinte
        self.check_victory(grid_instance)

    def generate_empty_grid(self):
        """Génère une grille vide de la taille spécifiée."""
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def check_victory(self, grid_instance):
        """Vérifie si toutes les cases non-minées ont été révélées."""
        for row in range(self.rows):
            for col in range(self.cols):
                if grid_instance.grid[row][col] != -1 and not self.revealed[row][col]:
                    return False
        self.victory = True
        return True
