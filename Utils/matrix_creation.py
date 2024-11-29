import chess
import chess.pgn
import pandas as pd
import numpy as np


def list_epd_per_move(pgn):

    """
    Permet de récupérer les epd (statut du plateau) après chaque coup à partir de la liste des coups inclus dans le pgn.
    """
    pgn=pgn.split()
    board = chess.Board() # initialise le board à 0
    list_epd=[]
    for move in pgn:
        # transforme le coup SAN en départ / arrivée
        m=board.parse_san(move)

        # réalise le mouvement
        board.push(m)

        # sort le fen (un état du board dans la partie)
        epd=board.epd()

        # epd cleaning
        epd=epd.split()[0]
        epd=epd.split("/")

        # tous les états de la partie
        list_epd.append(epd)

    return list_epd


def create_matrice_from_pgn(pgn,n):

    """
    permet de créer n matrices (1,2,12)  après chaque coup à partir de la liste des coups inclus dans le pgn.
    """

    list_epd= list_epd_per_move(pgn)

        # DEF PGN
    weights={"R":[5,5,1],
        "N":[3,3,1],
        "B":[4,4,1],
        "Q":[9,9,1],
        "K":[100,100,1],
        "P":[1,1,1],
        "r":[-5,5,1],
        "n":[-3,3,1],
        "b":[-4,4,1],
        "q":[-9,9,1],
        "k":[-100,100,1],
        "p":[-1,1,1]
        }

    matrice_12={"R":0,
        "N":1,
        "B":2,
        "Q":3,
        "K":4,
        "P":5,
        "r":6,
        "n":7,
        "b":8,
        "q":9,
        "k":10,
        "p":11
        }

    list_matrices=[]

    for epd in list_epd:
        matrice= np.zeros((n,8,8), dtype=float)
        if n==1:
            for i, row in enumerate(epd):
                k=0
                for j, char in enumerate(row):
                    if char.isdigit():
                        k+=int(char)-1
                    else:
                        matrice[0,i,j+k]=weights[char][0]
            list_matrices.append(matrice)
        elif n==2:
            for i, row in enumerate(epd):
                k=0
                for j, char in enumerate(row):
                    if char.isdigit():
                        k+=int(char)-1
                    else:
                        if char.islower():
                            matrice[1,i,j+k]=weights[char][1]
                        else:
                            matrice[0,i,j+k]=weights[char][1]
            list_matrices.append(matrice)
        elif n==12:
            for i, row in enumerate(epd):
                k=0
                for j, char in enumerate(row):
                    if char.isdigit():
                        k+=int(char)-1
                    else:
                        if char.islower():
                            matrice[matrice_12[char],i,j+k]=weights[char][2]
                        else:
                            matrice[matrice_12[char],i,j+k]=weights[char][2]
            list_matrices.append(matrice)
        else:
            return "n doit être égale à 1, 2 ou 12"

    return list_matrices