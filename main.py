import pygame
import time
import keyboard

pygame.init()

screen = pygame.display.set_mode((600, 500))
screen.fill((255, 255, 255))
pygame.display.update()


class Clicker:
    def __init__(self):
        self.score = 0
        self.click_multiplier = 1
        self.passive_multiplier = 0

    def passive_cost(self):
        return (self.passive_multiplier + 2) ** 3

    def click_cost(self):
        return (self.click_multiplier + 1) ** 2


def button(position, text, size, colors="white on blue"):
    fg, bg = colors.split(" on ")
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, True, fg)
    x, y, w, h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w, y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w, y + h), [x + w, y], 5)
    pygame.draw.rect(screen, bg, (x, y, w, h))
    return screen.blit(text_render, (x, y))


def update(font_score, font_stats, clicker):
    b_exit = button((526, 0), "Exit", 55, "red on yellow")
    b_per_second = button((0, 250), "+1 per second", 50, "red on yellow")
    b_per_click = button((390, 250), "+1 per click", 50, "red on yellow")
    b_click = button((250, 420), "Click!", 50, "red on yellow")

    img = font_score.render("Score: " + str(clicker.score), True, (0, 244, 0))
    img_clicks_per_second = font_stats.render("Clicks per second: " + str(clicker.passive_multiplier), True,
                                              (0, 244, 0))
    img_clicks_per_click = font_stats.render("Clicks per click: " + str(clicker.click_multiplier), True,
                                             (0, 244, 0))
    img_cost_per_second = font_stats.render("Cost: " + str(clicker.passive_cost()), True, (0, 244, 0))
    img_cost_per_click = font_stats.render("Cost: " + str(clicker.click_cost()), True, (0, 244, 0))

    screen.blit(img, (0, 0))
    screen.blit(img_clicks_per_second, (0, 220))
    screen.blit(img_clicks_per_click, (390, 220))
    screen.blit(img_cost_per_second, (0, 330))
    screen.blit(img_cost_per_click, (390, 330))


def click(clicker, font_score, font_stats, player_click):
    screen.fill((255, 255, 255))
    if player_click:
        clicker.score += clicker.click_multiplier
    else:
        clicker.score += clicker.passive_multiplier
    update(font_score, font_stats, clicker)


def buy_per_sec(clicker, font_score, font_stats):
    if clicker.score < clicker.passive_cost():
        return
    screen.fill((255, 255, 255))
    clicker.score -= clicker.passive_cost()
    clicker.passive_multiplier += 1
    update(font_score, font_stats, clicker)


def buy_per_click(clicker, font_score, font_stats):
    if clicker.score < clicker.click_cost():
        return
    screen.fill((255, 255, 255))
    clicker.score -= clicker.click_cost()
    clicker.click_multiplier += 1
    update(font_score, font_stats, clicker)


def menu():
    b_exit = button((526, 0), "Exit", 55, "red on yellow")
    b_click = button((250, 420), "Click!", 50, "red on yellow")
    b_per_second = button((0, 250), "+1 per second", 50, "red on yellow")
    b_per_click = button((390, 250), "+1 per click", 50, "red on yellow")
    clicker = Clicker()
    font_score = pygame.font.SysFont(None, 100)
    img_score = font_score.render("Score: " + str(clicker.score), True, (0, 244, 0))
    font_stats = pygame.font.SysFont(None, 30)
    img_clicks_per_second = font_stats.render("Clicks per second: " + str(clicker.passive_multiplier), True,
                                              (0, 244, 0))
    img_clicks_per_click = font_stats.render("Clicks per click: " + str(clicker.click_multiplier), True,
                                              (0, 244, 0))
    img_cost_per_second = font_stats.render("Cost: " + str(clicker.passive_cost()),True, (0, 244, 0))
    img_cost_per_click = font_stats.render("Cost: " + str(clicker.click_cost()),True, (0, 244, 0))
    screen.blit(img_score, (0, 0))
    screen.blit(img_clicks_per_second, (0, 220))
    screen.blit(img_clicks_per_click, (390, 220))
    screen.blit(img_cost_per_second, (0, 330))
    screen.blit(img_cost_per_click, (390, 330))

    last = time.time()

    keyboard.add_hotkey('Space', click, [clicker, font_score, font_stats, True], True, 1, True)

    while True:
        now = time.time()
        if (now - last >= 1):
            click(clicker, font_score, font_stats, False)
            last = now
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b_click.collidepoint(pygame.mouse.get_pos()):
                    click(clicker, font_score, font_stats, True)
                elif b_exit.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                elif b_per_second.collidepoint(pygame.mouse.get_pos()):
                    buy_per_sec(clicker, font_score, font_stats)
                elif b_per_click.collidepoint(pygame.mouse.get_pos()):
                    buy_per_click(clicker, font_score, font_stats)
        pygame.display.update()


menu()
