from set_strats import *
from src.roles import Role
from src.board import BoardStates
from src.game import assign_roles, game
from src.strategies import set_adjust_factor
from src.logging import Log


def main():
    games = 1000
    # for num_players in range(5,11):
    for num_players in [8]:
        for n in range(0, 31, 1):
        # for n in [10]:
            f_wins = 0
            l_wins = 0
            f_policies = 0
            l_policies = 0
            h_shot = 0
            h_chanc = 0
            total_anarchies = 0
            set_adjust_factor(n/10)

            for i in range(games):
                players = assign_roles(num_players)
                # for name, player in players.items():
                #     if player.role is Role.LIBERAL:
                #         set_liberal_strats(player)
                #     elif player.role is Role.FASCIST:
                #         set_fascist_strats(player)
                #     elif player.role is Role.HITLER:
                #         set_hitler_strats(player)
                for name, player in players.items():
                    if player.role is Role.LIBERAL:
                        set_liberal_strats(player, p_cards=1)
                    elif player.role is Role.FASCIST:
                        set_fascist_strats(player, choose_c=2)
                    elif player.role is Role.HITLER:
                        set_hitler_strats(player, choose_c=1, p_cards=0, c_cards=0, vote=0)

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
            message = 'Adjust Factor: {7}, Liberal Wins: {0}/{2}, Fascist Wins {1}/{2}, ' \
                      'Hitler Chancellor Wins {8}/{2}, Hitler Shot: {9}/{2}, ' \
                      'Liberal Policies: {3}/{5}, Fascist Policies {4}/{5}, Average Anarchies: {6}'
            Log.log(message.format(l_wins, f_wins, l_wins+f_wins, l_policies, f_policies,
                                   l_policies + f_policies, total_anarchies/games,
                                   n/10, h_chanc, h_shot))


if __name__ == '__main__':
    main()
