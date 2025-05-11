import csv
import os
from collections import defaultdict


class User:
    def __init__(self, name, balance=0, jackpot_count=0):
        self.name = name
        self.balance = balance
        self.jackpot_count = jackpot_count

    def top_up(self, amount):
        self.balance += amount
        print(f"Your new balance is: {self.balance}")


class UserManager:
    def __init__(self, filename='user_data.csv'):
        self.filename = filename
        self.users = self.load_users()

    def load_users(self):
        users = {}
        try:
            with open(self.filename, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['name']
                    balance = float(row['balance'])
                    jackpot_count = int(row.get('jackpot_count', 0))

                    user = User(name, balance, jackpot_count)
                    users[name] = user
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'balance', 'jackpot_count'])
        return users

    def save_users(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'balance', 'jackpot_count'])
            for name, user in self.users.items():
                writer.writerow([user.name, user.balance, user.jackpot_count])

    def get_user(self, name):
        if name in self.users:
            print(f"Welcome back, {name}! Your balance is {self.users[name].balance}")
            return self.users[name]
        else:
            print(f"Creating new user: {name} (balance = 0)")
            user = User(name)
            self.users[name] = user
            self.save_users()
            return user

    def top_up_user(self, user):
        if user.balance > 0:
            print(f"Your balance is already {user.balance}. No need to top up.")
            return

        print("Please choose a top-up amount:")
        options = [100, 300, 500, 1000, 2500, 5000]
        for idx, amount in enumerate(options, 1):
            print(f"{idx}. {amount}")

        choice = int(input("Enter choice number: "))
        amount_selected = options[choice - 1]
        user.top_up(amount_selected)
        self.save_users()


def log_gameplay_data(player_name, bet_amount, spin_result, coin_balance,
                      session_winnings, session_spins, streak_length, difficulty_state):
    file_path = "gameplay_log.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                'player_name', 'bet_amount', 'spin_result',
                'coin_balance', 'session_winnings', 'session_spins',
                'streak_length', 'difficulty_state'
            ])
        writer.writerow([
            player_name, bet_amount, spin_result,
            coin_balance, session_winnings, session_spins,
            streak_length, difficulty_state
        ])


def generate_player_summary(log_file='gameplay_log.csv', output_file='player_summary.csv'):
    stats = defaultdict(lambda: {
        'sessions': 0,
        'total_spins': 0,
        'total_winnings': 0,
        'total_streak': 0
    })

    with open(log_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if 'player_name' not in row:
                continue

            name = row['player_name']
            stats[name]['sessions'] += 1

            try:
                stats[name]['total_spins'] += float(row['session_spins'])
                stats[name]['total_winnings'] += float(row['session_winnings'])
                stats[name]['total_streak'] += float(row['streak_length'])
            except ValueError:
                print(f"⚠️ Skipped bad row: {row}")
                continue

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'player_name', 'total_sessions', 'total_spins',
            'avg_spins_per_session', 'total_winnings',
            'avg_winnings_per_spin', 'avg_max_streak'
        ])

        for name, data in stats.items():
            avg_spins = data['total_spins'] / data['sessions'] if data['sessions'] else 0
            avg_win_per_spin = data['total_winnings'] / data['total_spins'] if data['total_spins'] else 0
            avg_streak = data['total_streak'] / data['sessions'] if data['sessions'] else 0

            writer.writerow([
                name,
                data['sessions'],
                data['total_spins'],
                round(avg_spins, 2),
                round(data['total_winnings'], 2),
                round(avg_win_per_spin, 2),
                round(avg_streak, 2)
            ])
