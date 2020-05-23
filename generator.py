#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import random

class Sudoku:
    def __init__(self, N, K):

        # N - number of columns/rows
        # K - number of missing digits

        self.N = N
        self.K = K
        self.numberList = [1,2,3,4,5,6,7,8,9]
        
        # create a desired size board
        self.Board = []
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.Board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.fillGrid()
        self.removeKDigits()


    # A function to check if the board is full
    def checkGrid(self):
        for row in range(0, self.N):
            for col in range(0, self.N):
                if self.Board[row][col] == 0:
                    return False
        # We have a complete board!
        return True


    # A backtracking function to check all possible combinations of numbers until a solution is found
    def solveGrid(self):
        # Find next empty cell
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.Board[row][col] == 0:
                for value in range(1, 10):
                    # Check that this value has not already be used on this row
                    if not value in self.Board[row]:
                         # Check that this value has not already be used on this column
                        if not value in (self.Board[0][col],self.Board[1][col],self.Board[2][col],self.Board[3][col],self.Board[4][col],self.Board[5][col],self.Board[6][col],self.Board[7][col],self.Board[8][col]):
                            # Identify which of the 9 squares we are working on
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(0, 3)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(3, 6)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(6, 9)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(6, 9)]

                            # Check that this value has not already be used on this 3x3 square
                            if not value in square[0] + square[1] + square[2]:
                                self.Board[row][col] = value
                                if self.checkGrid():
                                    break
                                else:
                                    if self.solveGrid(self.Board):
                                        return True
                break
        self.Board[row][col] = 0


    # A backtracking/recursive function to check all possible combinations of numbers until a solution is found
    def fillGrid(self):
        # Find next empty cell
        for i in range(0, 81):
            row = i // 9
            col = i % 9
            if self.Board[row][col] == 0:
                random.shuffle(self.numberList)
                for value in self.numberList:
                    # Check that this value has not already be used on this row
                    if not value in self.Board[row]:
                        # Check that this value has not already be used on this column
                        if not value in (self.Board[0][col],self.Board[1][col],self.Board[2][col],self.Board[3][col],self.Board[4][col],self.Board[5][col],self.Board[6][col],self.Board[7][col],self.Board[8][col]):
                            # Identify which of the 9 squares we are working on
                            square = []
                            if row < 3:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(0, 3)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(0, 3)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(0, 3)]
                            elif row < 6:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(3, 6)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(3, 6)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(3, 6)]
                            else:
                                if col < 3:
                                    square = [(self.Board[i])[0:3] for i in range(6, 9)]
                                elif col < 6:
                                    square = [(self.Board[i])[3:6] for i in range(6, 9)]
                                else:
                                    square = [(self.Board[i])[6:9] for i in range(6, 9)]

                            # Check that this value has not already be used on this 3x3 square
                            if not value in square[0] + square[1] + square[2]:
                                self.Board[row][col] = value
                                if self.checkGrid():
                                    return True
                                else:
                                    if self.fillGrid():
                                        return True
                break
        self.Board[row][col] = 0
        
    # Remove the K no. of digits to complete game 
    def removeKDigits(self):
        count = self.K 
        while (count != 0): 
            cellId = random.randint(0, 81)-1
            row = int(cellId/self.N)
            col = int(cellId%9)
            if (self.Board[row][col] != 0):
                count -= 1
                self.Board[row][col] = 0


    def printSudoku(self):
        for row in range(self.N):
            if row % 3 == 0 and row != 0:
                print("- - - - - - - - - - - -")
            for col in range(self.N):
                if col % 3 == 0 and col!=0:
                    print(" | ", end="")
                if col == 8:
                    print(self.Board[row][col])
                else:
                    print(str(self.Board[row][col]) + " ", end="")

    def returnBoard(self):
        return self.Board
    

if __name__ == "__main__":
    N = 9
    K = 43
    sudoku = Sudoku(N, K)
    sudoku.printSudoku()