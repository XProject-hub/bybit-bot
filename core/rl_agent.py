import json
import os
import random

QTABLE_PATH = "data/qtable.json"

class RLAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=0.2):
        self.q_table = {}
        self.alpha = alpha  # learning rate
        self.gamma = gamma  # discount factor
        self.epsilon = epsilon  # exploration rate
        self.load()

    def _discretize(self, rsi, macd, bb_width):
        rsi_zone = int(rsi // 10)
        macd_trend = 1 if macd > 0 else 0
        vol = "low" if bb_width < 0.5 else "high"
        return f"rsi:{rsi_zone}|macd:{macd_trend}|vol:{vol}"

    def choose_action(self, rsi, macd, bb_width):
        state = self._discretize(rsi, macd, bb_width)
        if state not in self.q_table:
            self.q_table[state] = {"BUY": 0, "HOLD": 0}

        if random.random() < self.epsilon:
            return random.choice(["BUY", "HOLD"])
        return max(self.q_table[state], key=self.q_table[state].get)

    def update(self, rsi, macd, bb_width, action, reward):
        state = self._discretize(rsi, macd, bb_width)
        if state not in self.q_table:
            self.q_table[state] = {"BUY": 0, "HOLD": 0}

        current_q = self.q_table[state][action]
        best_future_q = max(self.q_table[state].values())
        new_q = current_q + self.alpha * (reward + self.gamma * best_future_q - current_q)
        self.q_table[state][action] = new_q
        self.save()

    def save(self):
        os.makedirs("data", exist_ok=True)
        with open(QTABLE_PATH, "w") as f:
            json.dump(self.q_table, f, indent=2)

    def load(self):
        if os.path.exists(QTABLE_PATH):
            with open(QTABLE_PATH, "r") as f:
                self.q_table = json.load(f)
