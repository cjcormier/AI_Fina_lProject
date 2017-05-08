from src.roles import Role


class Log:
    can_log = True
    can_log_probs = False

    def __init__(self):
        self.l_pres = 0
        self.f_pres = 0
        self.h_pres = 0
        self.l_chanc = 0
        self.f_chanc = 0
        self.h_chanc = 0

    @staticmethod
    def allow_logging(new_log):
        Log.can_log = new_log

    @staticmethod
    def allow_prob_logging(new_log_prob):
        Log.can_log_probs = new_log_prob

    @staticmethod
    def log_probs(probs_message):
        if Log.can_log_probs:
            Log.log(probs_message)

    @staticmethod
    def log_all_probs(players):
        if Log.can_log_probs:
            Log.log('\nProbabilities (Fascist/Hitler)')
            names = players.keys()
            header = '\t\t'+'\t\t\t'.join([str(x) for x in names])
            Log.log(header)
            for row in names:
                probs = players[row].probabilities
                temp = '{} ({})'.format(row, players[row].role.name[0])
                msg = temp + '\t'
                for entry in names:
                    temp = '{:.2}/{:.2}'.format(probs[entry][0], probs[entry][1])
                    padding = '\t'*(3 - int(len(temp)/4))
                    msg += temp + padding
                Log.log(msg)


    @staticmethod
    def log(*args):
        string = ''
        for element in args:
            string += str(element)
            string += ' '
        if Log.can_log:
            print(string[0:-1])

    def record_gov(self, president, chancellor):
        if president.role is Role.LIBERAL:
            self.l_pres += 1
        elif president.role is Role.FASCIST:
            self.f_pres += 1
        elif president.role is Role.HITLER:
            self.h_pres += 1

        if chancellor.role is Role.LIBERAL:
            self.l_chanc += 1
        elif chancellor.role is Role.FASCIST:
            self.f_chanc += 1
        elif chancellor.role is Role.HITLER:
            self.h_chanc += 1

    def log_game_results(self, rounds):
        message = '\n{} rounds:\n{} liberal presidents, {} fascist presidents and {} hitler ' \
                  'presidents\n{} liberal chancellors, {} fascist chancellors and {} hitler ' \
                  'chancellors.'
        message = message.format(rounds, self.l_pres, self.f_pres, self.h_pres, self.l_chanc,
                                 self.f_chanc, self.h_chanc)
        Log.log(message)

    @staticmethod
    def log_new_round():
        message = '\n------------------------\nNew Round\n'
        Log.log(message)

    @staticmethod
    def log_anarchy():
        message = 'Anarchy!!!!!\n'
        Log.log(message)

    @staticmethod
    def log_next_policy(policy):
        message = 'Next Policy: {}'
        Log.log(message.format(policy))

    @staticmethod
    def log_votes(president, chancellor, ja, nay):
        message = 'Voting on new government. President: {} Chancellor: {} ({},{})'
        Log.log(message.format(president.name, chancellor.name, president.role, chancellor.role))
        message = 'Votes in favor: {}, Votes against: {}  ({},{})'
        Log.log(message.format(ja, nay, len(ja), len(nay)))

    @staticmethod
    def log_vote_results(vote_passed, rounds):
        if vote_passed:
            message = 'Vote Passed'
        else:
            message = 'Vote Failed, number of consecutive failed votes:'
        Log.log(message.format(rounds))

    @staticmethod
    def log_valid_chancellors(valid_chancellors):
        Log.log('Valid chancellors: {}'.format(valid_chancellors))

    @staticmethod
    def log_elected_chancellor(chancellor, fascist_track):

        if 4 <= fascist_track:
            message = 'Late game Fascism; if the chancellor is Hitler, the Fascists win.'
            Log.log(message)
            if chancellor.role is Role.HITLER:
                message = 'Chancellor {} is Hitler, fascists win!'.format(chancellor.name)
            else:
                message = 'Chancellor {} not is Hitler, you live to play another day!'
                message = message.format(chancellor.name)
            Log.log(message)

    @staticmethod
    def log_policy(drawn_policies, p_pick, c_pick):
        message = '\nDrawn Cards:{}\nPres Pick: {}, Canc Pick: {}'
        Log.log(message.format(drawn_policies, p_pick, c_pick))

    @staticmethod
    def log_shot_players(president, player_shot):
        ps_name = player_shot.name
        message = 'President {} shot player {}.'.format(president.name, ps_name)
        Log.log(message)
        if player_shot.role is Role.HITLER:
            message = 'Player {} is Hitler, liberals win!'.format(ps_name)
        else:
            message = 'Player {0} is not Hitler. ({0} was {1} instead and {2} was {3}.)'
            message = message.format(ps_name, player_shot.role, president.name, president.role)
        Log.log(message)


__all__ = ['Log']
