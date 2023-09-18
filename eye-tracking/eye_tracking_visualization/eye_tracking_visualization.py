#!/bin/python
import pygame
import win32gui
import win32con
import win32api
import time


# Setting the given window to be always on top
def set_window_topmost(handle_window):
    win32gui.SetWindowPos(handle_window, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE)


# Saving the given data to a segmentation log file
def save_to_segm(t_start, t_now, x_pos, y_pos):
    logs = f"{t_now-t_start}, {x_pos}, {y_pos}\n"

    with open("segm_logs.txt", "a") as file:
        file.write(logs)


# Initializing Pygame
pygame.init()

# Creating a fullscreen window
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Getting the window handle
hwnd = pygame.display.get_wm_info()["window"]

# Setting the window to be transparent, click-through, and always on top
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                       | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(255, 255, 255), 200, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)

# Getting the window size
win_width, win_height = pygame.display.get_surface().get_size()
print(f'w{win_width}m h{win_height}')

# Setting up a clock for controlling the animation speed
clock = pygame.time.Clock()
fps = 120
frame = 0

# Setting the font for displaying the timestamp
font = pygame.font.SysFont('Arial', 18)

# Reading data from the eye tracker log file
with open('toby_logs.log', 'r') as f:
    data = f.readlines()

# Parsing the data into lists of timestamps, x, and y coordinates
timestamps = []
x_coords = []
y_coords = []
for line in data:
    timestamp, x, y = line.strip().split(',')
    timestamps.append(float(timestamp))
    x_coords.append(int(float(x)))
    y_coords.append(int(float(y)))

# Determining the range of x and y coordinates
min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)

# Calculating the scale factors to fit the coordinates onto the window
scale_x = win_width / (max_x - min_x)
scale_y = win_height / (max_y - min_y)

# Storing the start time
time_start = time.time()

# Main loop
while True:
    time_now = time.time()

    # Handling Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clearing the screen
    win.fill((255, 255, 255, 0))

    # Getting the current frame data
    timestamp = timestamps[frame]
    x = x_coords[frame]
    y = y_coords[frame]

    # Scaling the coordinates to fit the window
    x_scaled = int((x - min_x) * scale_x)
    y_scaled = int((y - min_y) * scale_y)

    # Drawing the timestamp and pointer
    text = font.render(str(timestamp), True, (0, 0, 0))
    win.blit(text, (10, 10))
    pygame.draw.circle(win, (255, 0, 0), (x_scaled, y_scaled), 30, width=4)

    # Incrementing the frame counter and looping back to the first frame if the end of the data is reached
    frame += 1
    if frame == len(timestamps):
        frame = 0

    # Manually setting the window to be on top again
    set_window_topmost(hwnd)

    # Updating the screen
    pygame.display.update()

    # Saving the current frame data to the segmentation log file
    save_to_segm(time_start, time_now, x, y)

    # Controlling the animation speed
    clock.tick(fps)
