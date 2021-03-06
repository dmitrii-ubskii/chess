#!/usr/bin/env python3

import random

from math import inf

from board import Board, Move
from board import get_piece_owner


def random_bot(board: Board) -> Move:
    return random.choice(list(board.get_all_legal_moves()))


def dummy_bot(board: Board) -> Move:
    PIECE_VALUES = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}
    def eval_board(board: Board) -> int:
        mobility_advantage = len(board.get_all_legal_moves()) - len(board._flip_player_copy().get_all_legal_moves())
        if board.is_mated():
            mobility_advantage -= 1000
        piece_advantage = 0
        for piece in board._board:
            if piece == '.':
                continue
            if get_piece_owner(piece) == board._active_player:
                piece_advantage += PIECE_VALUES[piece.upper()]
            else:
                piece_advantage -= PIECE_VALUES[piece.upper()]
        return mobility_advantage + piece_advantage
    return min(board.get_all_legal_moves(), key=lambda m: eval_board(board.make_move_copy(m)))


def minmax_bot(board: Board, depth: int = 2) -> Move:
    PIECE_VALUES = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}
    def eval_board(board: Board, player) -> int:
        mobility_advantage = len(board.get_all_legal_moves()) - len(board._flip_player_copy().get_all_legal_moves())
        piece_advantage = 0
        for piece in board._board:
            if piece == '.':
                continue
            if get_piece_owner(piece) == board._active_player:
                piece_advantage += PIECE_VALUES[piece.upper()]
            else:
                piece_advantage -= PIECE_VALUES[piece.upper()]
        if player == board._active_player:
            return mobility_advantage + piece_advantage
        else:
            return -(mobility_advantage + piece_advantage)

    def alphabeta(board: Board, player, depth: int, alpha=-inf, beta=inf, maximize: bool = True) -> int:
        if board.is_mated():
            if player == board._active_player:
                return -inf
            else:
                return inf
        if depth == 0:
            return eval_board(board, player)
        if maximize:
            value = -inf
            for m in board.get_all_legal_moves():
                value = max(value, alphabeta(board.make_move_copy(m), player, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = inf
            for m in board.get_all_legal_moves():
                value = min(value, alphabeta(board.make_move_copy(m), player, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    return max(board.get_all_legal_moves(), key=lambda m: alphabeta(board.make_move_copy(m), board._active_player, depth-1))
