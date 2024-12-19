import pygame
import random

class Grid:
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

    def populate_mines(self, mine_count):
        """Ajoute un certain nombre de mines aléatoirement dans la grille."""
        for _ in range(mine_count):
            while True:
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                if self.grid[row][col] == 0:  # Si la cellule est vide
                    self.grid[row][col] = -1  # Une mine est représentée par -1
                    break

    def populate_mines_avoiding(self, avoid_row, avoid_col, mine_count):

        placed_mines = 0
        while placed_mines < mine_count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)

            # Éviter la case cliquée, les cases révélées et les cellules déjà minées
            if self.grid[row][col] == 0 and (row != avoid_row and col != avoid_col):
                self.grid[row][col] = -1  # Ajouter une mine
                placed_mines += 1

    def calculate_adjacent_numbers(self):
        """Remplit la grille avec les nombres correspondant au nombre de mines adjacentes."""
        for row in range(self.rows):
            for col in range(self.cols):
                # Si la cellule contient une mine (-1), on ignore
                if self.grid[row][col] == -1:
                    continue

                # Compter les mines dans les cases adjacentes
                mine_count = 0
                for r in range(row - 1, row + 2):  # Parcourt les lignes adjacentes (-1, 0, +1)
                    for c in range(col - 1, col + 2):  # Parcourt les colonnes adjacentes (-1, 0, +1)
                        # Vérifie que la cellule adjacente est valide (dans les limites de la grille)
                        if 0 <= r < self.rows and 0 <= c < self.cols:
                            if self.grid[r][c] == -1:  # Si c'est une mine
                                mine_count += 1

                # Ajouter le nombre de mines adjacentes dans la cellule
                self.grid[row][col] = mine_count

    def get_cell_from_position(self, x, y):
        """Retourne la cellule (ligne, colonne) depuis une position x, y."""
        col = (x - self.offset_x) // self.cell_size
        row = (y - self.offset_y) // self.cell_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            print(row, col)
            return row, col
        return None  # Retourne None si le clic est hors de la grille
