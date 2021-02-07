# D4 connectivity shortest path finding
# change box_width for larger board
import pygame
import random

pygame.init()
clock = pygame.time.Clock()
# make sure it's over 2
box_width = 50
width, height = int(1200 / box_width), int(900 / box_width)
screen_width, screen_height = box_width * width, box_width * height
screen = pygame.display.set_mode((screen_width, screen_height + 30))
pygame.display.set_caption("pathy box")
small_font = pygame.font.Font("freesansbold.ttf", 30)

smallest_font = pygame.font.Font("freesansbold.ttf", 14)
screen_width_boxes = int(screen_width / box_width)
screen_height_boxes = int(screen_height / box_width)


class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_pix = x * box_width
        self.y_pix = y * box_width
        self.distance = None

    def draw_box(self, colour):
        pygame.draw.rect(screen, colour, (self.x_pix + 1, self.y_pix + 1, box_width - 2, box_width - 2))


def get_click_pos(click):
    x = None
    y = None
    for i in range(screen_width_boxes):
        for j in range(screen_height_boxes):
            cur_box = grid[i][j]
            if cur_box.x_pix < click[0] <= cur_box.x_pix + box_width:
                if cur_box.y_pix < click[1] <= cur_box.y_pix + box_width:
                    x, y = i, j
    return x, y


def get_neighbours(x, y):
    neighbourslist = []
    if x - 1 >= 0:
        neighbourslist.append(grid[x - 1][y])
    if x + 1 <= screen_width_boxes - 1:
        neighbourslist.append(grid[x + 1][y])
    if y - 1 >= 0:
        neighbourslist.append(grid[x][y - 1])
    if y + 1 <= screen_height_boxes - 1:
        neighbourslist.append(grid[x][y + 1])
    return neighbourslist


def update_neighbours(x, y):
    global closed
    distance = grid[x][y].distance
    neighbours_dist = distance + 1
    neighbours = get_neighbours(x, y)

    for neigh in neighbours:
        if neigh.distance is None:
            neigh.distance = neighbours_dist
            closed = False
        elif neigh.distance != 10000:
            if neigh.distance > neighbours_dist:
                neigh.distance = neighbours_dist
                closed = False


def check_if_filled():
    global status
    global total_dist
    filled = True
    for i in range(screen_width_boxes):
        for j in range(screen_height_boxes):
            if grid[i][j].distance is None:
                filled = False
    if filled:
        status = "pathfind"
        total_dist = grid[end[0]][end[1]].distance
        print("Total distance: " + str(total_dist))


def show_status_text():
    text = small_font.render("Status: " + status, True, (200, 200, 200))
    screen.blit(text, (10, screen_height))
    right_text = smallest_font.render("", True, (200, 200, 200))
    down_text = smallest_font.render("Press T to restart", True, (200, 200, 200))
    if status in ["start", "end"]:
        right_text = smallest_font.render("Press R to randomize ", True, (200, 200, 200))
    if status == "obstacles":
        right_text = smallest_font.render("R to randomize, Space when done", True, (200, 200, 200))
        down_text = smallest_font.render("Rightclick to remove, T restart", True, (200, 200, 200))
    if status == "filling":
        right_text = smallest_font.render("Filling distance map", True, (200, 200, 200))
    if status == "closed":
        right_text = smallest_font.render("Could not find a path", True, (200, 200, 200))
    if status == "pathfind":
        right_text = smallest_font.render("Finding shortest path", True, (200, 200, 200))
    if status == "done":
        right_text = smallest_font.render("Distance: " + str(total_dist) + " blocks", True, (200, 200, 200))
    screen.blit(right_text, (300, screen_height))
    screen.blit(down_text, (300, screen_height + 15))


def generate_random_obstacles():
    n = int(width * height / 10)
    for i in range(n):
        x = random.randint(0, screen_width_boxes - 1)
        y = random.randint(0, screen_height_boxes - 1)
        grid[x][y].distance = 10000


running = True
initiated = False

while running:

    if not initiated:

        grid = []
        for i in range(screen_width_boxes):
            grid.append([])
        for i in range(screen_width_boxes):
            for j in range(screen_height_boxes):
                grid[i].append(Box(x=i, y=j))

        status = "start"
        start = None
        end = None
        closed = False
        tickrate = 1000
        total_dist = -1
        initiated = True

    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            click_x, click_y = get_click_pos(pos)
            if status == "start":
                start = (click_x, click_y)
                grid[click_x][click_y].distance = 0
                status = "end"
            elif status == "end":
                if not start == (click_x, click_y):
                    end = (click_x, click_y)
                    curr_path = grid[end[0]][end[1]]
                    status = "obstacles"
        if pygame.mouse.get_pressed(num_buttons=3)[0] and status == "obstacles":
            pos = pygame.mouse.get_pos()
            click_x, click_y = get_click_pos(pos)
            try:
                grid[click_x][click_y].distance = 10000
            except:
                pass
        if pygame.mouse.get_pressed(num_buttons=3)[2] and status == "obstacles":
            pos = pygame.mouse.get_pos()
            click_x, click_y = get_click_pos(pos)
            try:
                grid[click_x][click_y].distance = None
            except:
                pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if status == "start":
                    x = random.randint(0, screen_width_boxes - 1)
                    y = random.randint(0, screen_height_boxes - 1)
                    start = (x, y)
                    grid[x][y].distance = 0
                    status = "end"
                if status == "end":
                    x = random.randint(0, screen_width_boxes - 1)
                    y = random.randint(0, screen_height_boxes - 1)
                    end = (x, y)
                    curr_path = grid[end[0]][end[1]]
                    status = "obstacles"
                if status == "obstacles":
                    generate_random_obstacles()

            if event.key == pygame.K_SPACE and status == "obstacles":
                status = "filling"
                tickrate = 10
                grid[start[0]][start[1]].distance = 0
                grid[end[0]][end[1]].distance = None

            if event.key == pygame.K_t:
                initiated = False
                break

    if status == "filling":
        closed = True
        for i in range(screen_width_boxes):
            for j in range(screen_height_boxes):
                cur_box = grid[i][j]
                if cur_box.distance is not None and cur_box.distance != 10000:
                    update_neighbours(i, j)
        if closed:
            if grid[end[0]][end[1]].distance is None:
                status = "closed"
            else:
                status = "pathfind"
                total_dist = grid[end[0]][end[1]].distance
                print("Total distance: " + str(total_dist))
        check_if_filled()

    if status == "pathfind":
        tickrate = 15
        if curr_path.distance > 0:
            grid[curr_path.x][curr_path.y].distance = 999
            path_neighbours = get_neighbours(curr_path.x, curr_path.y)
            next_neighbour = curr_path
            for neigh in path_neighbours:
                if neigh.distance < next_neighbour.distance:
                    next_neighbour = neigh
            curr_path = next_neighbour
        else:
            status = "done"

    for i in range(screen_width_boxes):
        for j in range(screen_height_boxes):
            if grid[i][j].distance == 10000:
                col = (0, 0, 150)
            elif grid[i][j].distance is None:
                col = (0, 0, 0)
            elif grid[i][j].distance == 999:
                col = (0, 255, 0)
            else:  # colortable
                coeff = box_width/1
                c = grid[i][j].distance * coeff
                if c > 255 * 9:
                    c %= 9*255
                if c > 255 * 8:
                    col = (0, 255 * 9 - c, 0)
                elif c > 255 * 7:
                    col = (255 * 8 - c, c - 255 * 7, 255 * 8 - c)
                elif c > 255 * 6:
                    col = (c - 255 * 6, 0, 255)
                elif c > 255 * 5:
                    col = (0, 255 * 6 - c, 255)
                elif c > 255 * 4:
                    col = (255 * 5 - c, 255, 255)
                elif c > 255 * 3:
                    col = (255, 255, 255)
                elif c > 255 * 2:
                    col = (255, 255, c - 255 * 2)
                elif c > 255:
                    col = (255, c - 255, 0)
                else:
                    col = (c, 0, 0)

            grid[i][j].draw_box(col)

    if start is not None:
        grid[start[0]][start[1]].draw_box((0, 200, 0))
    if end is not None:
        grid[end[0]][end[1]].draw_box((200, 0, 200))

    show_status_text()

    clock.tick(tickrate)

    pygame.display.update()
