import copy


class Player:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class Match:

    def __init__(self, holes, players):
        if not isinstance(holes, int) or holes <= 0 or not isinstance(players, list) or players == []:
            raise TypeError
        self._holes = holes
        self._players = players
        self._active_players_names = [player._name for player in players]
        self._current_player_index = 0
        self._results = []
        self._current_hole = 0
        self.finished = False
        for _ in range(holes):
            hole_results = []
            for player in players:
                hole_results.append({'player': player._name, 'score': 0})
            self._results.append(hole_results)

    @property
    def finished(self):
        return self._finished

    # функция, меняющая порядок игроков
    def _change_player_order(self):
        self._active_players_names = [player._name for player in self._players]
        tail = self._active_players_names[:self._current_hole % len(self._players)]
        self._active_players_names = self._active_players_names[self._current_hole % len(self._players):] + tail

    @finished.setter
    def finished(self, value):
        self._finished = value

    def hit(self, success):
        pass

    def get_table(self):
        pass

    def get_winners(self):
        if self.finished:
            winners = [{'player': player, 'score': 0} for player in self._players]
            for match in self._results:
                for index, kick in enumerate(match):
                    winners[index]['score'] += kick['score']
            sorted_list_of_dict = self._sort_players(winners)
            result = []
            for res in sorted_list_of_dict:
                if res['score'] == sorted_list_of_dict[0]['score']:
                    result.append(res['player'])
            return result
        else:
            raise RuntimeError

    def _sort_players(self, array):
        pass


class HitsMatch(Match):
    LAST_KICK = 10

    def _check(self, change):
        if not self._active_players_names:
            self._current_player_index = 0
            self._active_players_names = [player._name for player in self._players]

            if self._current_hole + 1 < self._holes:
                self._current_hole += 1
                self._change_player_order()
            else:
                self._active_players_names = []
                self.finished = True

        else:
            if self._current_player_index < len(self._active_players_names) - 1 and not change:
                self._current_player_index += 1
            elif self._current_player_index > len(self._active_players_names) - 1:
                self._current_player_index = 0
            elif not change and self._current_player_index == len(self._active_players_names) - 1:
                self._current_player_index = 0

    def _sort_players(self, array):
        return sorted(array, key=lambda x: x['score'])

    def hit(self, success=False):
        if not self.finished:
            for kick in self._results[self._current_hole]:
                if self._active_players_names[self._current_player_index] == kick['player']:
                    kick['score'] += 1
                    if success:
                        del self._active_players_names[self._current_player_index]
                        break
                    if kick['score'] == HitsMatch.LAST_KICK - 1:
                        del self._active_players_names[self._current_player_index]
                        kick['score'] = HitsMatch.LAST_KICK
                        success = True
                        break
            self._check(success)

        else:
            raise RuntimeError

    def get_table(self):
        res_dict = copy.deepcopy(self._results)
        players_names_tuple = tuple([player._name for player in self._players])
        table = []
        table.append(players_names_tuple)
        for i in range(self._current_hole):
            r = []
            for elem in res_dict[i]:
                r.append(elem['score'])
            table.append(tuple(r))
        arr = []
        for match in res_dict[self._current_hole]:
            if match['player'] in self._active_players_names:
                arr.append(None)
            else:
                arr.append(match['score'])
        table.append(tuple(arr))
        for count_match in range(self._current_hole + 1, self._holes):
            list_for_res = []
            for elem in res_dict[count_match]:
                elem['score'] = None
                list_for_res.append(elem['score'])

            table.append(tuple(list_for_res))
        return table


class HolesMatch(Match):
    LAST_CIRCLE = 10

    def __init__(self, holes, players):
        Match.__init__(self, holes, players)
        self._winners_names = []
        self._number_of_kick = 0
        self._results = []
        for _ in range(holes):
            hole_results = []
            for player in players:
                hole_results.append({'player': player._name, 'score': None})
            self._results.append(hole_results)

    def get_table(self):
        res_dict = copy.deepcopy(self._results)
        players_names_tuple = tuple([player._name for player in self._players])
        table = []
        table.append(players_names_tuple)
        for i in range(self._holes):
            arr = []
            for res in res_dict[i]:
                if i < self._current_hole:
                    arr.append(res['score'])

                elif i == self._current_hole:
                    if res['player'] in self._winners_names:
                        res['score'] = 1

                    elif self._active_players_names.index(res['player']) < self._current_player_index:
                        res['score'] = 0
            arr = [x['score'] for x in res_dict[i]]
            table.append(tuple(arr))

        return table

    def hit(self, success=False):
        if not self.finished:
            for kick in self._results[self._current_hole]:
                if self._active_players_names[self._current_player_index] == kick['player']:
                    if success:
                        winner = self._active_players_names[self._current_player_index]
                        self._winners_names.append(winner)
                        break
            self._check()

        else:
            raise RuntimeError

    def _check(self, ):
        # если все ударили, то смотрим, есть ли кто забил
        if self._current_player_index + 1 == len(self._active_players_names):
            if self._winners_names:
                for player_match in self._results[self._current_hole]:
                    if player_match['player'] in self._winners_names:
                        player_match['score'] = 1
                    else:
                        player_match['score'] = 0
                if self._current_hole + 1 < self._holes:
                    self._current_hole += 1
                    self._number_of_kick = 0
                    self._winners_names = []
                    self._change_player_order()
                    self._current_player_index = 0
                else:
                    self.finished = True
            else:
                if (self._number_of_kick + 1) / len(self._active_players_names) == HolesMatch.LAST_CIRCLE:
                    for player_match in self._results[self._current_hole]:
                        player_match['score'] = 0
                    if self._current_hole + 1 < self._holes:
                        self._current_hole += 1
                        self._number_of_kick = 0
                        self._winners_names = []
                        self._change_player_order()
                        self._current_player_index = 0
                    else:
                        self.finished = True
                else:
                    self._number_of_kick += 1
                    self._current_player_index = 0
        else:
            self._number_of_kick += 1
            self._current_player_index += 1

    def _sort_players(self, array):
        return sorted(array, key=lambda x: x['score'], reverse=True)
