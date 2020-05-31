import pygame
import db_connector as dbc

class ListItem():
    def __init__(self, surface, ID):
        self.dbAgent = dbc.DbConnector("Sudoku")
        self.getGames()