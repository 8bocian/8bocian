#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import ctypes
import random as rm
import numpy as np
from cv2 import cv2
import time
import os




class Maze:
    def __init__(self, x=None, y=None, sleep=0):
        self.step = self.time = self.iter = 0
        
        # slow down our entity
        self.sleep = sleep
        self.width_wall = -1
        
        # size of our cell
        self.size = 10
        
        # check if we provided height and length of our maze
        if x is None:
            x = WIDTH / self.size
        if y is None:
            y = HEIGHT / self.size
        self.rows = int(y)
        self.cols = int(x)
        
        # construct our maze grid
        self.maze = [[Cell(position=(r, c)) for c in range(self.cols)] for r in range(self.rows)]
        self.path = self.solution = []
        
        # initiate colours
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.ENTITY = (255, 0, 0)
        self.SOLVER = (75, 0, 150)
        self.CHANGE = (0, 230, 0)
        
        # create our base image for maze visualization
        self.image = np.zeros(shape=[HEIGHT, WIDTH, 4], dtype=np.uint8)
        self.wallpaper_path = os.getcwd()
        
        # create maze according to Hunt and Kill algorithm
        self.createMaze()

    def createMaze(self):
        for r_idx, row in enumerate(self.maze):
            for cell in row:
                for _ in range(2):
                    self.move(cell.position)

    def move(self, currCell):
        hasNeighbour, direction, nextCell = self.hasNeighbours(self.maze[currCell[0]][currCell[1]])
        if self.maze[currCell[0]][currCell[1]].status:
            self.maze[currCell[0]][currCell[1]].color = self.CHANGE
            self.draw_move(currCell)
            self.change_wallpaper()
            self.maze[currCell[0]][currCell[1]].status = False
        self.time += 1

        # change the color of the maze fill
        if self.time % 80 == 0:
            if self.CHANGE[1] < 255 and self.step == 0:
                self.CHANGE = (0, self.CHANGE[1] + 1, self.CHANGE[2])
            else:
                self.step = 1
            if self.CHANGE[2] < 255 and self.step == 1:
                self.CHANGE = (0, self.CHANGE[1], self.CHANGE[2] + 1)
            elif self.step == 1:
                self.step = 2
            if self.CHANGE[1] > 0 and self.step == 2:
                self.CHANGE = (0, self.CHANGE[1] - 1, self.CHANGE[2])
            self.time = 0

        # delete walls of the cell by checking the next transition of our entity
        # e.g. bottom wall of the cell where out entity is now is the upper wall of the cell where out entity will be in the next iteration
        if hasNeighbour:
            self.maze[currCell[0]][currCell[1]].walls[direction] = 0
            if direction == 1:
                direction = 3
            elif direction == 0:
                direction = 2
            elif direction == 2:
                direction = 0
            elif direction == 3:
                direction = 1
            self.maze[nextCell[0]][nextCell[1]].walls[direction] = 0
            self.move(nextCell)

    def hasNeighbours(self, cell):
        # r-row
        # c-column
        r = cell.position[0]
        c = cell.position[1]
        neighbours = []
        direction = []

        # check the status of neighbouring cells if they exist
        if r < self.rows - 1 and self.maze[r + 1][c].status:
                neighbours.append((r + 1, c))
                direction.append(2)
        if c < self.cols - 1 and self.maze[r][c + 1].status:
                neighbours.append((r, c + 1))
                direction.append(1)

        # check the status of neighbouring cells
        if self.maze[r - 1][c].status and r != 0:
            neighbours.append((r - 1, c))
            direction.append(0)
        if self.maze[r][c - 1].status and c != 0:
            neighbours.append((r, c - 1))
            direction.append(3)

        # if there are neighbours then move and don't reset the run
        if len(neighbours) >= 1:
            randomDirection = rm.randint(0, len(neighbours)) - 1
            return True, direction[randomDirection], neighbours[randomDirection]
        else:
            return False, None, None

    def solve_and_show(self, start=None, end=None):
        if start is None:
            start = (0, 0)
        if end is None:
            end = (rm.randint(int(self.rows / 2), self.rows - 1), rm.randint(int(self.cols / 2), self.cols - 1))
        self.solve(start, end)
        self.draw_path()

    def solve(self, start, end):
        # dijkstra algorithm implementation
        unvisited = {}
        for row in self.maze:
            for cell in row:
                unvisited[cell.position] = float('inf')
        unvisited[start] = 0
        visited = {}
        revPath = {}

        while unvisited:
            minNode = min(unvisited, key=unvisited.get)
            visited[minNode] = unvisited[minNode]

            if minNode == end:
                break

            unSureNeighbours = [(minNode[0] - 1, minNode[1]),
                                (minNode[0], minNode[1] + 1),
                                (minNode[0] + 1, minNode[1]),
                                (minNode[0], minNode[1] - 1)]
            SureNeighbours = []
            for w_i, wall in enumerate(self.maze[minNode[0]][minNode[1]].walls):
                if wall == 0:
                    SureNeighbours.insert(w_i, unSureNeighbours[w_i])

            for neighbour in SureNeighbours:
                if neighbour in visited:
                    continue
                if neighbour in unvisited:
                    tempDist = unvisited[minNode] + 1
                    if tempDist < unvisited[neighbour]:
                        unvisited[neighbour] = tempDist
                        revPath[neighbour] = minNode
            unvisited.pop(minNode)

        node = end
        revPathList = [node]
        while node != start:
            revPathList.append(revPath[node])
            node = revPath[node]
        self.solution = revPathList[::-1]

    def draw_move(self, cell_position):
        # draw move of our entity
        self.path.append((cell_position[0], cell_position[1]))
        self.maze[cell_position[0]][cell_position[1]].color = self.CHANGE
        self.draw_entity(self.maze[cell_position[0]][cell_position[1]], self.CHANGE)
        self.draw_cell(self.maze[cell_position[0]][cell_position[1]], self.CHANGE)
        time.sleep(self.sleep)

    def draw_cell(self, cell, color, entity=False):
        # in the future, this will be converted to a smaller size by creating functions for repetitive code
        r, c = cell.position[0], cell.position[1]
        pvColor = co = color
        if cell.walls[0] == 1:
            cv2.rectangle(self.image,
                          (c * self.size + 2, r * self.size - 2),
                          ((c * self.size - 3) + self.size, r * self.size + 1),
                          self.BLACK,
                          thickness=self.width_wall)
        else:
            if entity:
                co = self.maze[r - 1][c].color
            cv2.rectangle(self.image,
                          (c * self.size + 2, r * self.size - 2),
                          ((c * self.size - 3) + self.size, r * self.size + 1),
                          co,
                          thickness=self.width_wall)
        co = pvColor
        if cell.walls[1] == 1:
            cv2.rectangle(self.image,
                          ((c * self.size) + self.size - 2, r * self.size + 4),
                          ((c * self.size) + self.size + 1, (r * self.size) + self.size - 3),
                          self.BLACK,
                          thickness=self.width_wall)
        else:
            if entity:
                co = self.maze[r][c + 1].color
            cv2.rectangle(self.image,
                          ((c * self.size) + self.size - 2, r * self.size + 2),
                          ((c * self.size) + self.size + 1, (r * self.size) + self.size - 3),
                          co,
                          thickness=self.width_wall)
        co = pvColor
        if cell.walls[2] == 1:
            cv2.rectangle(self.image,
                          ((c * self.size + 2), (r * self.size) + self.size - 2),
                          ((c * self.size) + self.size - 3, (r * self.size) + self.size + 1),
                          self.BLACK,
                          thickness=self.width_wall)
        else:
            if entity:
                co = self.maze[r + 1][c].color
            cv2.rectangle(self.image,
                          ((c * self.size + 2), (r * self.size) + self.size - 2),
                          ((c * self.size) + self.size - 3, (r * self.size) + self.size + 1),
                          co,
                          thickness=self.width_wall)
        co = pvColor
        if cell.walls[3] == 1:
            cv2.rectangle(self.image,
                          ((c * self.size), r * self.size),
                          ((c * self.size), (r * self.size) + self.size),
                          self.BLACK,
                          thickness=self.width_wall)
        else:
            if entity:
                co = self.maze[r][c - 1].color
            cv2.rectangle(self.image,
                          ((c * self.size - 2), r * self.size + 2),
                          ((c * self.size + 1), (r * self.size) + self.size - 3),
                          co,
                          thickness=self.width_wall)

    def draw_path(self):
        for step in self.solution:
            self.maze[step[0]][step[1]].color = self.SOLVER
            self.draw_entity(self.maze[step[0]][step[1]], self.SOLVER)
            self.draw_cell(self.maze[step[0]][step[1]], self.maze[step[0]][step[1]].color, True)
            self.change_wallpaper()

    def draw_entity(self, cell, color):
        r, c = cell.position[0], cell.position[1]
        cv2.rectangle(self.image,
                      (c * self.size + 2, r * self.size + 2),
                      (c * self.size - 3 + self.size, r * self.size - 3 + self.size),
                      color,
                      thickness=-1)

    def change_wallpaper(self):
        cv2.imwrite(f'{self.wallpaper_path}\window.png', self.image)
        path = self.wallpaper_path + r'\window.png'
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        self.iter += 1


class Cell:
    def __init__(self, position, walls=None, color=None, status=True):
        if walls is None:
            walls = [1, 1, 1, 1]
        self.walls = walls
        self.position = position
        self.status = status
        self.color = color


def go():
    while 1:
        maze = Maze()
        maze.solve_and_show()


if __name__ == "__main__":
    user32 = ctypes.windll.user32
    WIDTH = user32.GetSystemMetrics(78)
    HEIGHT = user32.GetSystemMetrics(79)
    go()
