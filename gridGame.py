import pygame

import grid
from grid import Grid

class GridGame:
    def __init__(self, rows, cols, cell_size, window_width, window_height):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.generate_empty_grid()
        self.offset_x = (window_width - (cols * cell_size)) // 2
        self.offset_y = (window_height - (rows * cell_size)) // 2

    def generate_empty_grid(self):
        """Génère une grille vide de la taille spécifiée."""
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(0)
            grid.append(row)
        return grid

    def draw(self, surface):
        """Affiche la grille avec les cases, les mines et les chiffres."""
        font = pygame.font.Font(None, 40)  # Police pour afficher les chiffres
        for row in range(self.rows):
            for col in range(self.cols):
                # Dessiner les contours des cellules
                rect = pygame.Rect(
                    self.offset_x + col * self.cell_size,
                    self.offset_y + row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(surface, "white", rect, 1)  # Dessine la bordure des cellules

                # Si la cellule contient une mine (-1), dessine un cercle rouge
                if self.grid[row][col] == -1:
                    pygame.draw.circle(
                        surface,
                        "red",  # Couleur rouge pour les mines
                        (
                        self.offset_x + col * self.cell_size + self.cell_size // 2,
                        self.offset_y + row * self.cell_size + self.cell_size // 2),
                        self.cell_size // 3
                    )
                # Si la cellule contient un chiffre > 0, affiche le chiffre
                elif self.grid[row][col] > 0:
                    text = font.render(str(self.grid[row][col]), True, "yellow")  # Texte jaune
                    text_rect = text.get_rect(center=(
                        self.offset_x + col * self.cell_size + self.cell_size // 2,
                        self.offset_y + row * self.cell_size + self.cell_size // 2
                    ))
                    surface.blit(text, text_rect)

    def changeValue(self, row, col):
