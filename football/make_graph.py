"""
A script to take the winners and losers of football games and their conferences
and make a dot file out of them.

@author Kevin Wilson - khwilson@gmail.com
@license Apache 2.0
"""
import io
import re
import sys

from football.base import get_games, get_teams_to_conference, in_and_cross_conference_edges


# Bad dot file characters
BAD_CHARS = re.compile(r'[ +.()-]')


def transform_name(name):
    """
    Given a team name, return its canonical short form.

    :param str name: The name
    :return: The canonical short name
    :rtype: str
    """
    return BAD_CHARS.sub('', name)


class Indenter(object):
    """
    A wrapper class for an output stream that allows for easy pretty printing of
    variably indented lines.
    """

    def __init__(self, stream):
        """
        :param io.IOBase stream: An output stream
        """
        self.stream = stream
        self._indent = 0
        self.tab = ' ' * 4

    def indent(self):
        """ Increase the current indent """
        self._indent += 1

    def dedent(self):
        """ Decrease the current indent, but not below 0 """
        self._indent -= 1
        if self._indent < 0: self._indent = 0

    def write_line(self, line=''):
        """ Write the passed line, which if empty, just writes a new line with no tabs """
        if line:
            self.stream.write(self.tab * self._indent)
            self.stream.write(line)
        self.stream.write('\n')


def make_graph(games, conferences, output):
    """
    Given a list of games, a map from team to conference, and an output file handle, output the
    graph of winners and losers.

    :param list[Game] games: The list of games
    :param dict[str, str] conferences: Dictionary of team to conference
    :param io.IOBase output: The output handle
    """
    indenter = Indenter(output)
    in_conference, cross_conference = in_and_cross_conference_edges(games, conferences)

    indenter.write_line('digraph G {')
    indenter.indent()
    indenter.write_line('node[shape=point];')
    for conference, these_games in in_conference.viewitems():
        indenter.write_line('subgraph cluster_%s {' % transform_name(conference))
        indenter.indent()
        indenter.write_line('label="%s"' % conference)
        indenter.write_line('color=lightgrey')
        for game in these_games:
            indenter.write_line(' -> '.join(map(transform_name, game)) + ';')
        indenter.dedent()
        indenter.write_line('}')
        indenter.write_line()

    for game in cross_conference:
        indenter.write_line(' -> '.join(map(transform_name, game)) + ';')

    indenter.dedent()
    indenter.write_line('}')


def main():
    games_file = sys.argv[1] if len(sys.argv) > 1 else 'cfb2013lines.csv'
    conferences_file = sys.argv[2] if len(sys.argv) > 2 else 'conferences.csv'
    output_file = sys.argv[3] if len(sys.argv) > 3 else 'output.dot'
    with open(games_file, 'r') as games:
        games = get_games(games)
    with open(conferences_file, 'r') as confs:
        conferences = get_teams_to_conference(confs)

    with open(output_file, 'w') as output:
        make_graph(games, conferences, output)

if __name__ == '__main__':
    main()
