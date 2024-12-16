import pygame
import random


class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.generate_empty_grid()

    def generate_empty_grid(self):
        """Génère une grille vide de la taille spécifiée."""
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(0)
            grid.append(row)
        return grid

    def populate_mines(self, mine_count):
        """Ajoute un certain nombre de mines aléatoirement dans la grille."""
        for _ in range(mine_count):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if self.grid[row][col] == 0:  # Si la cellule est vide
                    self.grid[row][col] = -1  # Une mine est représentée par -1
                    break

    def draw(self, surface):
        """Affiche la grille sur l'écran, avec options pour afficher les mines."""
        for row in range(self.rows):
            for col in range(self.cols):
                # Dessine les contours des cellules
                rect = pygame.Rect(
                    col * self.cell_size,  # Position X
                    row * self.cell_size,  # Position Y
                    self.cell_size,  # Largeur
                    self.cell_size  # Hauteur
                )
                pygame.draw.rect(surface, "white", rect, 1)  # Bordure des cases

                # Si la cellule contient une mine (-1), dessine un cercle rouge
                if self.grid[row][col] == -1:
                    pygame.draw.circle(
                        surface,
                        "red",  # Couleur de la mine
                        (col * self.cell_size + self.cell_size // 2,  # Centre X
                         row * self.cell_size + self.cell_size // 2),  # Centre Y
                        self.cell_size // 3  # Rayon du cercle
                    )