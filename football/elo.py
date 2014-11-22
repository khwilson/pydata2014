"""
A simple implementation of Elo's method to be used with scipy's optimize
functionality

@author Kevin Wilson - khwilson@gmail.com
@license Apache 2.0
"""
import itertools as its
import math

import numpy as np


def convert_edges(edges):
    """
    Given a list of pairs of team names, winners in the first slot and losers in the second,
    return a dictionary of team name to the index in sorted order, the indices of the winners,
    and the indices of the losers

    :param list[(str, str)] edges: The pairs of winners and losers
    :return: The relevant indices
    :rtype: dict[str, int], list[int], list[int]
    """
    teams = sorted(set(its.chain(*edges)))
    team_to_idx = {team: i for i, team in enumerate(teams)}
    int_winners = [team_to_idx[winner] for winner, _ in edges]
    int_losers = [team_to_idx[loser] for _, loser in edges]

    return team_to_idx, int_winners, int_losers


def make_elo_neg_likelihood(int_winners, int_losers):
    """
    Given indices of winners and losers into the array of awesomenesses, return a function
    to be used by scipy to minimize

    :param list[int] int_winners: Winners' indices in the same order as int_losers
    :param list[int] int_losers: Losers' indices in the same order as int_winners
    :return: The Elo likelihood function
    :rtype: function
    """
    def likelihood(thetas):
        return np.sum(1.0 + np.exp(thetas[int_losers] - thetas[int_winners]))

    return likelihood
