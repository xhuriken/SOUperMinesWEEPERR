import pygame

import grid
from grid import Grid

class GridGame:
    def __init__(self, rows, cols, cell_size, window_width, window_height):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = self.generate_empty_grid()
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]  # Pour suivre les cases révélées
        self.flags = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.offset_x = (window_width - (cols * cell_size)) // 2
        self.offset_y = (window_height - (rows * cell_size)) // 2
        self.game_over = False
        self.victory = False

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
                            # Point supérieur central
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + self.cell_size // 4),

                            # Point supérieur droit
                            (self.offset_x + col * self.cell_size + 3 * self.cell_size // 4,
                             self.offset_y + row * self.cell_size + self.cell_size // 3),

                            # Point inférieur droit
                            (self.offset_x + col * self.cell_size + 3 * self.cell_size // 4,
                             self.offset_y + row * self.cell_size + 2 * self.cell_size // 3),

                            # Point inférieur central
                            (self.offset_x + col * self.cell_size + self.cell_size // 2,
                             self.offset_y + row * self.cell_size + 3 * self.cell_size // 4),

                            # Point inférieur gauche
                            (self.offset_x + col * self.cell_size + self.cell_size // 4,
                             self.offset_y + row * self.cell_size + 2 * self.cell_size // 3),

                            # Point supérieur gauche
                            (self.offset_x + col * self.cell_size + self.cell_size // 4,
                             self.offset_y + row * self.cell_size + self.cell_size // 3),
                        ]
                    )
                else:
                    # Cases non révélées : affichage coloré
                    color = "purple"  # Exemple : bleu pour les cases non révélées
                    pygame.draw.rect(surface, color, rect)
                    pygame.draw.rect(surface, "white", rect, 1)  # Bordure blanche

    def changeValue(self, row, col, grid_instance):
        """Révèle une case si elle ne comporte pas de drapeau ni que le jeu est terminé."""
        if self.flags[row][col] or self.game_over or self.victory:
            return  # Ne rien faire si la case contient un drapeau, si le jeu est terminé ou si on a gagné

        # Vérifier si la case est une bombe
        if grid_instance.grid[row][col] == -1:
            self.grid[row][col] = grid_instance.grid[row][col]  # Révéler la bombe
            self.revealed[row][col] = True  # Marquer la case comme révélée
            self.game_over = True  # Marquer la partie comme perdue
            return

        # Révéler la case si ce n'est pas une bombe
        self.grid[row][col] = grid_instance.grid[row][col]
        self.revealed[row][col] = True

        # Vérifier si le joueur a gagné après cette action
        self.check_victory(grid_instance)

    def toggle_flag(self, row, col):
        """Ajoute ou enlève un drapeau sur une case."""
        if not self.revealed[row][col]:  # Ne pas permettre le placement de drapeaux sur une case déjà révélée
            self.flags[row][col] = not self.flags[row][col]

    def generate_empty_grid(self):
        """Génère une grille vide de la taille spécifiée."""
        grid = []
        for _ in range(self.rows):
            row = []
            for _ in range(self.cols):
                row.append(0)
            grid.append(row)
        return grid

    def check_victory(self, grid_instance):
        """Vérifie si toutes les cases non-minées ont été révélées."""
        for row in range(self.rows):
            for col in range(self.cols):
                # Vérifier les cases non-minées (≠ -1)
                if grid_instance.grid[row][col] != -1:
                    # Si une case non-minée n'est ni révélée ni marquée par un drapeau, la victoire n'est pas atteinte
                    if not self.revealed[row][col]:
                        return False
        self.victory = True  # Toutes les cases non-minées ont été révélées (ou les mines marquées avec un drapeau)
        return True