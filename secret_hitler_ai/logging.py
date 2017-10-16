from secret_hitler_ai.role import Role


class Log:
    can_log = True
    can_log_probs = False
    file = None

    def __init__(self):
        self.l_pres = 0
        self.f_pres = 0
        self.h_pres = 0
        self.l_chanc = 0
        self.f_chanc = 0
        self.h_chanc = 0

    @staticmethod
    def set_file(file: str):
        Log.file = open(file, 'w+')

    @staticmethod
    def close_file():
        if Log.file is not None:
            Log.file.close()

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
    def log_all_probs(active_players, all_players):
        if Log.can_log_probs and Log.can_log:
            Log.log('\nProbabilities (Fascist/Hitler)')
            names = active_players.keys()
            all_names = all_players.keys()
            header = '\t\t'+'\t\t\t\t\t'.join([str(x) for x in names])
            Log.log(header)

            for row in all_names:
                temp = '{} ({})'.format(row, all_players[row].role.name[0])
                msg = [temp, '\t']
                for entry in names:
                    probs = active_players[entry].probabilities
                    temp = '{0.fascist:.4}/{0.hitler:.4}'.format(probs[row])
                    padding = '\t'*(5 - int(len(temp)/4))
                    msg += [temp, padding]
                Log.log(''.join(msg))
            msg = ['Total:', '\t']
            for entry in names:
                probs = active_players[entry].probabilities
                ftotal = sum([x.fascist for x in probs.values()])
                htotal = sum([x.hitler for x in probs.values()])
                temp = '{:.2}/{:.2}'.format(ftotal, htotal)
                padding = '\t'*(5 - int(len(temp)/4))
                msg += [temp, padding]
            Log.log(''.join(msg))

    @staticmethod
    def log(msg: str, args=()):
        if Log.can_log:
            msg = str(msg)
            try:
                msg = msg.format(*args)
            except:
                msg = msg.format(args)
            print(msg)
            if Log.file is not None:
                Log.file.write(msg + '\n')

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
        message = '\n{} rounds:\n{} liberal presidents, {} fascist presidents and {} ' \
                  'hitler presidents\n{} liberal chancellors, {} fascist chancellors ' \
                  'and {} hitler chancellors.'
        args =(rounds, self.l_pres, self.f_pres, self.h_pres, self.l_chanc,
                                 self.f_chanc, self.h_chanc)
        Log.log(message, args)

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
        Log.log(message, (policy))

    @staticmethod
    def log_votes(president, chancellor, ja, nay):
        message = 'Voting on new government. President: {} Chancellor: {} ({},{})'
        args = (president.name, chancellor.name, president.role, chancellor.role)
        Log.log(message, args)
        message = 'Votes in favor: {}, Votes against: {}  ({},{})'
        Log.log(message, (ja, nay, len(ja), len(nay)))

    @staticmethod
    def log_vote_results(vote_passed, rounds):
        if vote_passed:
            message = 'Vote Passed'
        else:
            message = 'Vote Failed, number of consecutive failed votes:'
        Log.log(message, rounds)

    @staticmethod
    def log_valid_chancellors(valid_chancellors):
        Log.log('Valid chancellors: {}', valid_chancellors)

    @staticmethod
    def log_elected_chancellor(chancellor, fascist_track):
        if 4 <= fascist_track:
            message = 'Late game Fascism; if the chancellor is Hitler, the Fascists win.'
            Log.log(message)
            if chancellor.role is Role.HITLER:
                message = 'Chancellor {} is Hitler, fascists win!'
            else:
                message = 'Chancellor {} not is Hitler, you live to play another day!'
            Log.log(message, chancellor.name)

    @staticmethod
    def log_policy(drawn_policies, p_pick, c_pick):
        message = '\nDrawn Cards:{}\nPres Pick: {}, Canc Pick: {}'
        Log.log(message.format(drawn_policies, p_pick, c_pick))

    @staticmethod
    def log_shot_players(president, player_shot):
        ps_name = player_shot.name
        Log.log('President {} shot player {}.', (president.name, ps_name))
        if player_shot.role is Role.HITLER:
            message = 'Player {} is Hitler, liberals win!'
            args = ps_name
        else:
            message = 'Player {0} is not Hitler. ({0} was {1} instead and {2} was {3}.)'
            args = (ps_name, player_shot.role, president.name, president.role)
        Log.log(message, args)


__all__ = ['Log']
