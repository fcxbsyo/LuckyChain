import csv


class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

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
                    users[name] = User(name, balance)
        except FileNotFoundError:
            with open(self.filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'balance'])
        return users

    def save_users(self):
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'balance'])
            for user in self.users.values():
                writer.writerow([user.name, user.balance])

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
