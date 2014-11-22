"""
Basic manipulations for the football csvs.

@author Kevin Wilson - khwilson@gmail.com
@license Apache 2.0
"""
from collections import defaultdict, namedtuple
import csv
import io


# A namedtuple that represents the summary statistics of a game
Game = namedtuple('Game', ['date', 'home', 'home_score', 'visitor', 'visitor_score'])


def get_teams_to_conference(the_file):
    """
    Read a CSV whose first column is a team name and whose second column is its conference
    and return a dictionary from team name to conference

    :param io.IOBase the_file: The file which will be read
    :return: Dictionary from team to conference
    :rtype: dict[str, str]
    """
    reader = csv.reader(the_file)
    return {team: conference for team, conference in reader}


def get_games(the_file):
    """
    Read a CSV whose columns are

    date_of_game, home_team, home_team_score, visiting_team, visiting_team_score, line

    which has headers and return a list of the rows translated to Game objects.

    :param io.IOBase the_file: The file which will be read
    :return: A list of games
    :rtype: list[Game]
    """
    reader = csv.reader(the_file)
    next(reader)
    return [Game(date=date, home=home, home_score=int(home_score),
                 visitor=visitor, visitor_score=int(visitor_score))
            for date, home, home_score, visitor, visitor_score, _ in reader]


def win_or_lose(game):
    """
    Given a Game, return a pair of team names, with winner of the game in the 0th position
    and the loser in the 1st position.

    :param Game game: A game
    :return: The winner and loser in that order
    :rtype: (str, str)
    """
    if game.home_score > game.visitor_score:
        return (game.home, game.visitor)
    return (game.visitor, game.home)


def in_and_cross_conference_edges(games, conferences):
    in_conference = defaultdict(list)
    cross_conference = []
    for game in games:
        home_conf = conferences[game.home]
        visit_conf = conferences[game.visitor]
        if home_conf == visit_conf:
            in_conference[home_conf].append(win_or_lose(game))
        else:
            cross_conference.append(win_or_lose(game))
    return in_conference, cross_conference
