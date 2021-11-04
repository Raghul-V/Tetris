import pygame
import sys
import time
import random
import numpy as np


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

NUM_OF_ROW = 20
NUM_OF_COL = 10
TOP_SPACING = 85
SIDE_SPACING = 300
SQUARE_SIZE = (SCREEN_WIDTH - 2*SIDE_SPACING) // NUM_OF_COL


class Block:
    """
    a class to represent each tetriminos block
    
    """
    
    # colors for the random tetriminos block
    colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), 
        (0, 255, 255), (150, 75, 0), (255, 165, 0), (255, 70, 0), 
        (255, 180, 195), (128, 0, 128), (255, 215, 0), (205, 0, 205), 
        (155, 50, 255), (255, 155, 50), (255, 128, 0), (255, 0, 128), 
        (0, 255, 128), (0, 128, 255), (128, 255, 0), (128, 0, 255)
    ]

    # all seven tetriminos rotated in all 4 directions as coordinates
    blocks = [
        [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, -1), (0, 0), (1, 0), (2, 0)], [(0, 0), (1, 0), (0, 1), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)], [(0, 0), (0, 1), (0, 2), (-1, 2)],
        [(0, 0), (1, 0), (2, 0), (2, -1)], [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (2, 0)], [(-1, 0), (0, 0), (0, 1), (0, 2)],
        [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)], [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, -1), (2, -1)], [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, -1), (2, -1)], [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, -1), (1, -1), (1, -2)],
        [(0, 0), (1, 0), (1, 1), (2, 1)], [(0, 0), (0, -1), (1, -1), (1, -2)],
        [(0, 0), (1, 0), (1, -1), (2, 0)], [(0, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (2, 0)], [(0, 0), (0, 1), (-1, 1), (0, 2)]
    ]

    def __init__(self, center):
        self.center = center
        self.block = random.choice(Block.blocks)
        # if any part of the block is out of the screen, the block is adjusted
        for x, y in self.block:
            if center[0] + x >= NUM_OF_COL:
                self.center[0] = NUM_OF_COL - (x+1)
            elif center[0] + x < 0:
                self.center[0] = -x
        self.color = random.choice(Block.colors)

    def move_left(self, grid):
        for x, y in self.block:
            # check whether the block is in the left most edge
            if x + self.center[0] - 1 < 0:
                return False
            # check whether the left square is blocked or out of grid
            elif grid[y + self.center[1], x + self.center[0] - 1] == "X":
                return False
        self.center[0] -= 1

    def move_right(self, grid):
        for x, y in self.block:
            # check whether the block is in the right most edge
            if x + self.center[0] + 1 >= NUM_OF_COL:
                return False
            # check whether the right square is blocked or out of grid
            elif grid[y + self.center[1], x + self.center[0] + 1] == "X":
                return False
        self.center[0] += 1

    def move_down(self, grid):
        for x, y in self.block:
            # check whether the block has landed or not
            if y + self.center[1] + 1 >= NUM_OF_ROW:
                return False
            # check whether the block is on top of some other landed block
            elif y + self.center[1] + 1 >= 0:
                if grid[y + self.center[1] + 1, x + self.center[0]] == "X":
                    return False
        self.center[1] += 1
        return True

    def display(self, surface):
        i, j = self.center
        for x, y in self.block:
            # display parts which are within the visible grid
            if all([i+x >= 0, i+x < NUM_OF_COL, j+y >= 0, j+y < NUM_OF_ROW]):
                pygame.draw.rect(surface, self.color, (
                    SIDE_SPACING + (i + x)*SQUARE_SIZE + 1, 
                    TOP_SPACING + (j + y)*SQUARE_SIZE + 1, 
                    SQUARE_SIZE - 2, SQUARE_SIZE - 2
                ))


def save_score(score_, file_):
    with open(file_, "w") as f:
        f.write(str(score_))


def update_screen(surface, font1, font2, moving, stable, score, 
        high_score, game_state):
    surface.fill((20, 20, 20))

    title = font1.render("TETRIS", True, (255, 255, 255))
    surface.blit(title, (SCREEN_WIDTH/2 - 72, TOP_SPACING/2 - 19))

    # draws the grid lines
    for i in range(NUM_OF_ROW):
        for j in range(NUM_OF_COL):
            pygame.draw.rect(surface, (150, 150, 150), (
                    SIDE_SPACING + j*SQUARE_SIZE, TOP_SPACING + i*SQUARE_SIZE, 
                    SQUARE_SIZE, SQUARE_SIZE), width=1
            )

    # displays all blocks within grid on the screen
    for block in stable:
        block.display(surface)

    if game_state == "play":
        moving[0].display(surface)

    # red color outline for the enrire grid
    pygame.draw.rect(surface, (255, 0, 0), (
        SIDE_SPACING, TOP_SPACING, SQUARE_SIZE*NUM_OF_COL, SQUARE_SIZE*NUM_OF_ROW
    ), width=3)

    color = (220, 220, 220)
    high_score_text = font2.render(f"HIGH SCORE: {high_score}", True, color)
    surface.blit(high_score_text, high_score_text.get_rect(
        center=(SIDE_SPACING/2 + 5, SCREEN_HEIGHT/2 - 45)))
    
    score_text = font2.render(f"SCORE: {score}", True, color)
    surface.blit(score_text, score_text.get_rect(
        center=(SIDE_SPACING/2 + 5, SCREEN_HEIGHT/2 + 15)))
    
    next_block_text = font2.render("NEXT BLOCK", True, color)
    surface.blit(next_block_text, next_block_text.get_rect(
        center=(SCREEN_WIDTH - SIDE_SPACING/2, SCREEN_HEIGHT/2 - 4*SQUARE_SIZE)))

    # displays the upcoming block beside the grid
    next_block = moving[(0 if game_state == "start" else 1)]
    x_coors, y_coors = zip(*next_block.block)
    mid_x = (min(x_coors)+max(x_coors)) / 2
    mid_y = (min(y_coors)+max(y_coors)) / 2

    # centers the block
    for x, y in next_block.block:
        x -= mid_x + 1/2
        y -= mid_y + 1/2
        pygame.draw.rect(surface, next_block.color, (
            SCREEN_WIDTH - (SIDE_SPACING/2) + x*SQUARE_SIZE + 1, 
            SCREEN_HEIGHT/2 + y*SQUARE_SIZE + 1,
            SQUARE_SIZE - 2, SQUARE_SIZE - 2
        ))

    pygame.display.update()


def end_game(high_score):
    save_score(high_score, "high_score.txt")
    pygame.quit()
    sys.exit()


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("TETRIS GAME")

    clock = pygame.time.Clock()

    large_font = pygame.font.Font("freesansbold.ttf", 38)
    small_font = pygame.font.Font("freesansbold.ttf", 32)

    grid = np.full((NUM_OF_ROW, NUM_OF_COL), " ")
    game_state = "start"

    moving_blocks = [Block([random.randint(0, NUM_OF_COL-1), -3]) for _ in range(3)]
    stable_blocks = []

    high_score = 0
    # if there exists a previous highscore, it is taken
    with open("high_score.txt") as file:
        old_high_score = file.read().strip()
        high_score = int(old_high_score) if old_high_score.isdigit() else 0
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game(high_score)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    end_game(high_score)
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    game_state = "play"
                elif game_state == "play":
                    if event.key == pygame.K_RIGHT:
                        moving_blocks[0].move_right(grid)
                    elif event.key == pygame.K_LEFT:
                        moving_blocks[0].move_left(grid)
                    elif event.key == pygame.K_DOWN:
                        moving_blocks[0].move_down(grid)

        if game_state == "play":
            # if there is a part of block on the first row, the game is over
            if "X" in grid[0]:
                time.sleep(2.5)
                end_game(high_score)
            # if the last row is completely filled with blocks, it gets down
            # and a new row is seen on the top
            elif " " not in grid[-1]:
                grid = np.delete(grid, -1, axis=0)
                grid = np.insert(grid, 0, [" "], axis=0)

                for block in stable_blocks:
                    block.center[1] += 1

            current_block = moving_blocks[0]

            # if the block has landed, turns it stable and adds a new block to the end
            # also updates the score and highscore
            if not current_block.move_down(grid):
                curr = moving_blocks.pop(0)
                for x, y in curr.block:
                    grid[y + curr.center[1], x + curr.center[0]] = "X"
                stable_blocks.append(curr)
                new_block = Block([random.randint(0, NUM_OF_COL - 1), -3])
                moving_blocks.append(new_block)
                score += 1

            high_score = max(score, high_score)

        update_screen(screen, large_font, small_font, moving_blocks, 
            stable_blocks, score, high_score, game_state)
        clock.tick(3)


if __name__ == "__main__":
    main()

