import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана и цветов
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Гонки на автомобиле")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Параметры игры
CAR_WIDTH, CAR_HEIGHT = 50, 100
FPS = 40

# Загрузка изображений
car_image = pygame.image.load("car.png")
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))
obstacle_image = pygame.image.load("obstacle.png")
obstacle_image = pygame.transform.scale(obstacle_image, (50, 50))
boost_image = pygame.image.load("boost.png")
boost_image = pygame.transform.scale(boost_image, (30, 30))

# Функции для создания объектов игры
def create_obstacle():
    x = random.randint(0, WIDTH - 50)
    y = random.randint(-100, -50)
    return pygame.Rect(x, y, 50, 50)

def create_boost():
    x = random.randint(0, WIDTH - 30)
    y = random.randint(-200, -100)
    return pygame.Rect(x, y, 30, 30)

# Основной класс игры
class Game:
    def __init__(self):
        self.car = pygame.Rect(WIDTH // 2, HEIGHT - CAR_HEIGHT - 10, CAR_WIDTH, CAR_HEIGHT)
        self.speed = 5
        self.health = 3
        self.score = 0
        self.obstacles = [create_obstacle() for _ in range(5)]
        self.boosts = [create_boost() for _ in range(3)]
        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

    def draw_text(self, text, x, y, color=BLACK):
        label = self.font.render(text, True, color)
        screen.blit(label, (x, y))

    def move_obstacles(self):
        for obs in self.obstacles:
            obs.y += self.speed
            if obs.y > HEIGHT:
                obs.y = random.randint(-100, -50)
                obs.x = random.randint(0, WIDTH - 50)
                self.score += 1

    def move_boosts(self):
        for boost in self.boosts:
            boost.y += self.speed
            if boost.y > HEIGHT:
                boost.y = random.randint(-200, -100)
                boost.x = random.randint(0, WIDTH - 30)

    def check_collisions(self):
        # Проверка столкновений с препятствиями
        for obs in self.obstacles:
            if self.car.colliderect(obs):
                self.health -= 1
                obs.y = random.randint(-100, -50)
                obs.x = random.randint(0, WIDTH - 50)
                if self.health == 0:
                    return True  # Игра окончена

        # Проверка столкновений с бонусами
        for boost in self.boosts:
            if self.car.colliderect(boost):
                self.speed += 1  # Ускорение автомобиля
                self.boosts.remove(boost)
                self.boosts.append(create_boost())
        return False

    def run(self):
        running = True
        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Управление автомобилем
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.car.x - self.speed > 0:
                self.car.x -= self.speed
            if keys[pygame.K_RIGHT] and self.car.x + self.speed < WIDTH - CAR_WIDTH:
                self.car.x += self.speed
            if keys[pygame.K_UP] and self.car.y - self.speed > 0:
                self.car.y -= self.speed
            if keys[pygame.K_DOWN] and self.car.y + self.speed < HEIGHT - CAR_HEIGHT:
                self.car.y += self.speed

            # Движение препятствий и бонусов
            self.move_obstacles()
            self.move_boosts()

            # Проверка столкновений
            if self.check_collisions():
                self.draw_text("Игра окончена!", WIDTH // 2 - 100, HEIGHT // 2, RED)
                pygame.display.flip()
                pygame.time.wait(2000)
                break

            # Отображение объектов на экране
            screen.blit(car_image, (self.car.x, self.car.y))
            for obs in self.obstacles:
                screen.blit(obstacle_image, (obs.x, obs.y))
            for boost in self.boosts:
                screen.blit(boost_image, (boost.x, boost.y))

            # Отображение счёта и здоровья
            self.draw_text(f"Счёт: {self.score}", 10, 10)
            self.draw_text(f"Здоровье: {self.health}", 10, 40)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
