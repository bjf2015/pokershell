import cmd
import time
import re

import prettytable

import minsk.eval.manager as manager
import minsk.eval.simulation as simulation
import minsk.model as model
import minsk.config as config


class MinskShell(cmd.Cmd):
    """Minsk shell"""
    prompt = '(minsk) '

    def do_bf(self, cards):
        """evaluate hand - brute force"""
        cards, _ = self._parse_line(cards)
        simulator = simulation.BruteForceSimulator()
        self.simulate(cards, simulator)

    def do_e(self, cards):
        """evaluate hand"""
        cards, player_num = self._parse_line(cards)
        manager = simulation.SimulatorManager()
        with config.with_config(_player_num=player_num):
            simulator = manager.find_simulator(*cards)
            self.simulate(cards, simulator)

    def _parse_line(self, cards):
        tokens = cards.split()
        player_num = config.player_num
        if re.fullmatch('\d', tokens[-1]):
            player_num = int(tokens[-1])
            tokens = tokens[:-1]
        return model.Card.parse_cards(tokens), player_num

    def do_hmc(self, cards):
        """evaluate hand - hybrid monte carlo"""
        cards, player_num = self._parse_line(cards)
        with config.with_config(_player_num=player_num):
            simulator = simulation.HybridMonteCarloSimulator(
                config.player_num, config.sim_cycles)
            self.simulate(cards, simulator)

    def do_mc(self, cards):
        """evaluate hand - monte carlo"""
        cards, player_num = self._parse_line(cards)
        with config.with_config(_player_num=player_num):
            simulator = simulation.MonteCarloSimulator(config.player_num, config.sim_cycles)
            self.simulate(cards, simulator)

    def do_lu(self, cards):
        """evaluate hand - loop up"""
        cards, player_num = self._parse_line(cards)
        with config.with_config(_player_num=player_num):
            simulator = simulation.LookUpSimulator(config.player_num)
            self.simulate(cards, simulator)

    def simulate(self, cards, simulator):
        self.print_configuration(simulator)
        self.print_input(cards)
        if not simulator:
            print('\nNo simulator found!\n')
            return
        start = time.time()
        result = simulator.simulate(*cards)
        self.print_output(result)
        elapsed = time.time() - start
        print('\nSimulation finished in %.2f seconds\n' % elapsed)

    def do_player_num(self, player_num):
        """set player number"""
        config.player_num = int(player_num)

    def do_sim_cycles(self, sim_cycles):
        """set simulation cycles number"""
        config.sim_cycles = int(sim_cycles)

    def print_configuration(self, simulator):
        print('\nConfiguration :')
        t = prettytable.PrettyTable(['key', 'value'])
        for name in ('player_num', 'sim_cycles'):
            t.add_row([name, getattr(config, name)])
        if simulator:
            t.add_row(['simulator', simulator.name])
        print(t)

    def print_output(self, result):
        print('\nOutput :')
        result_table = prettytable.PrettyTable(['Win', 'Tie', 'Loss'])

        if isinstance(result[0], int):
            total = sum(result)
            result_pct = list(map(lambda x: str(round(x / total * 100, 2)) + '%', result))
            result_table.add_row(result_pct)
            result_table.add_row(result)
        else:
            result_pct = list(map(lambda x: str(round(x, 2)) + '%', result))
            result_table.add_row(result_pct)
        print(result_table)

    def print_input(self, cards):
        print('\nInput :')
        columns = ['Hole']
        row = [' '.join(map(repr, cards[0:2]))]
        if len(cards) >= 5:
            columns.append('Flop')
            row.append(' '.join(map(repr, cards[2:5])))
        if len(cards) >= 6:
            columns.append('Turn')
            row.append(cards[5])
        if len(cards) == 7:
            columns.append('River')
            row.append(cards[6])
        evaluator_manager = manager.EvaluatorManager()
        if len(cards) >= 5:
            hand = evaluator_manager.find_best_hand(*cards)
            columns.append('Hand')
            row.append(hand[0].name)

            columns.append('Ranks')
            row.append(' '.join(map(repr, hand[1])))

        input_table = prettytable.PrettyTable(columns)
        input_table.add_row(row)
        print(input_table)

    def do_EOF(self, line):
        return True


def main():
    MinskShell().cmdloop()


if __name__ == '__main__':
    main()
