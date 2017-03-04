from set_strats import *
from src.roles import Role
from src.board import BoardStates
from src.game import assign_roles, game
from src.strategies import set_adjust_factor
from src.logging import Log


def main():
    games = 1000

    header = 'Players,Adjust factor,Games,Liberal wins,Fascist wins,HC wins,HS wins,L Policies,' \
             'F Policies,Total Policies,Average Anarchies'
    message = '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}'
    Log.log(header)
    for num_players in range(5, 11):
        for n in [100]:
            f_wins = 0
            l_wins = 0
            f_policies = 0
            l_policies = 0
            h_shot = 0
            h_chanc = 0
            total_anarchies = 0
            set_adjust_factor(n/100)

            for i in range(games):
                players = assign_roles(num_players)
                for name, player in players.items():
                    if player.role is Role.LIBERAL:
                        set_random(player)
                    elif player.role is Role.FASCIST:
                        set_random(player)
                    elif player.role is Role.HITLER:
                        set_random(player)

                Log.allow_logging(False)
                winner, fascist_board, liberal_board, anarchies = \
                    game(num_players, players, allow_shoots=True)
                Log.allow_logging(True)

                total_anarchies += anarchies
                f_policies += fascist_board
                l_policies += liberal_board
                if winner is BoardStates.LIBERAL_WIN:
                    l_wins += 1
                elif winner is BoardStates.FASCIST_WIN:
                    f_wins += 1
                elif winner is BoardStates.HITLER_CHANCELLOR:
                    f_wins += 1
                    h_chanc += 1
                elif winner is BoardStates.HITLER_SHOT:
                    l_wins += 1
                    h_shot += 1
            Log.log(message.format(num_players, n / 100, games, l_wins, f_wins, h_chanc, h_shot,
                                   l_policies, f_policies, l_policies + f_policies,
                                   total_anarchies / games))


if __name__ == '__main__':
    main()
