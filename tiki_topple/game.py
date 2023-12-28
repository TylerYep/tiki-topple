from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import override

from tiki_topple.const import ID, STARTING_ACTIONS, TIKI_GROUPS, Goal
from tiki_topple.enums import Action, Tiki


def play_game(users: list[int]) -> None:
    players = [Player(i) for i in range(4)]
    for index in users:
        players[index].is_user = True
    game = Game(players, players[0].player_id)
    while (winner := game.get_winning_player()).score < 35:
        game.start_new_round()
        while len(game.tikis) != 3:
            print(game)
            player = game.get_next_player()
            action, index = player.choose_action(game.tikis)
            game.execute_action(action, index)
        game.increment_scores()

    print(f"The winner is: {winner}")


def generate_tikis() -> list[Tiki]:
    groups: list[list[Tiki]] = [list(group) for group in TIKI_GROUPS]
    random.shuffle(groups)
    tikis = []
    for group in groups:
        random.shuffle(group)
        tikis += group
    return tikis


def generate_goal() -> Goal:
    groups: list[list[Tiki]] = [list(group) for group in TIKI_GROUPS]
    random.shuffle(groups)
    return (
        random.choice(groups[0]),
        random.choice(groups[1]),
        random.choice(groups[2]),
    )


def score(goal: Goal, tikis: list[Tiki]) -> int:
    assert len(tikis) == 3
    total = 0
    if goal[0] == tikis[0]:
        total += 9
    if goal[1] in tikis[:1]:
        total += 5
    if goal[2] in tikis:
        total += 2
    return total


@dataclass(slots=True)
class Player:
    player_id: ID
    is_user: bool = False
    score: int = 0
    goal: Goal = (Tiki.NANI, Tiki.NUI, Tiki.KAPU)
    actions: list[Action] = field(default_factory=list)

    def choose_action(self, tikis: list[Tiki]) -> tuple[Action, int]:
        if self.is_user:
            print(f"Your goal: {self.goal}")
            print(
                "\n".join([f"{i}: {action}" for i, action in enumerate(self.actions)])
            )
            action_index, tiki_index = -1, -1
            while not 0 <= action_index < len(self.actions):
                user_input = ""
                while not user_input.isdigit():
                    user_input = input(
                        f"Which action index (0 - {len(self.actions) - 1})? "
                    )
                action_index = int(user_input)

            if self.actions[action_index] != Action.TIKI_TOAST:
                while not 0 <= tiki_index < len(tikis):
                    user_input = ""
                    while not user_input.isdigit():
                        user_input = input(f"Which tiki index (0 - {len(tikis) - 1})? ")
                    tiki_index = int(user_input)
        else:
            action_index = random.randrange(len(self.actions))
            tiki_index = len(tikis) - 1
        return self.actions.pop(action_index), tiki_index


@dataclass(slots=True)
class Game:
    players: list[Player]
    current_turn: ID
    tikis: list[Tiki] = field(default_factory=list)

    @override
    def __str__(self) -> str:
        tikis = " | ".join([tiki.value for tiki in self.tikis])
        return f"Tikis: {tikis}"

    def start_new_round(self) -> None:
        self.current_turn = self.players[0].player_id
        self.tikis = generate_tikis()
        for player in self.players:
            player.actions = list(STARTING_ACTIONS)
            player.goal = generate_goal()
        print("\nScores:")
        for player in self.players:
            print(f"Player {player.player_id}: {player.score}")
        print()

    def get_winning_player(self) -> Player:
        return max(self.players, key=lambda player: player.score)

    def get_next_player(self) -> Player:
        self.current_turn = (self.current_turn + 1) % len(self.players)
        return self.players[self.current_turn]

    def execute_action(self, action: Action, index: int) -> None:
        if action == Action.UP_ONE:
            assert index >= 1
            print(f"Moving {self.tikis[index]} up by 1.\n")
            self.tikis.insert(index - 1, self.tikis.pop(index))
        elif action == Action.UP_TWO:
            assert index >= 2
            print(f"Moving {self.tikis[index]} up by 2.\n")
            self.tikis.insert(index - 2, self.tikis.pop(index))
        elif action == Action.UP_THREE:
            assert index >= 3
            print(f"Moving {self.tikis[index]} up by 3.\n")
            self.tikis.insert(index - 3, self.tikis.pop(index))
        elif action == Action.TIKI_TOPPLE:
            print(f"Moving {self.tikis[index]} to the bottom.\n")
            self.tikis.append(self.tikis.pop(index))
        elif action == Action.TIKI_TOAST:
            print(f"Toasting {self.tikis[index]}.\n")
            self.tikis.pop()
        else:
            raise RuntimeError(f"Action not handled: {action}")

    def increment_scores(self) -> None:
        for player in self.players:
            player.score += score(player.goal, self.tikis)
