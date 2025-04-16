#  LuckyChain Slot Machine

LuckyChain is a visually engaging, data-aware slot machine game built with Python and Pygame.  

---

##  Project Structure – What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Main launcher and Pygame-based UI for Welcome, Login, and Menu screens |
| `main.py` | Core game loop – handles rendering, timing, input, and transitions |
| `machine.py` | Controls reel spawning, spinning logic, win payouts, and Markov integration |
| `reel.py` | Manages individual reel behavior and symbol spawning |
| `symbol.py`  | Defines how each symbol behaves and animates |
| `markovchain.py` | Controls difficulty progression using Markov Chain logic |
| `player.py` | Tracks in-game player state: balance, bets, wins/losses, jackpots |
| `statistics.py` | Tracks spin data, win/loss ratios, and jackpot stats for reporting |
| `ui.py` | Renders in-game UI elements (balance, bet, win banner, etc.) |
| `bot.py` | (If used) Simulates player behavior or auto-spins for testing |
| `user_manager.py` | Manages user data, registration, saving/loading balances from CSV |
| `user_data.csv` | Stores player names, balances, and jackpot counts |
| `gameplay_log.csv` | *(Planned)* Will be used for logging gameplay data for analysis (e.g., spin outcomes, win rates) |
| `settings.py` | Game-wide constants like screen size, symbol paths, and font settings |
| `wins.py` | Contains helper functions for checking wins (e.g., longest matching sequences) |

---

##  Current Features

-  Weighted reels with cherry, watermelon, bell, olive, and sevenn
-  Markov Chain-driven dynamic difficulty
-  Balance and wager system with persistent user data
-  Jackpot tracking and win feedback
-  ESC-based confirmation dialog
-  Built-in bot and statistics tracker (for future auto-analysis)
-  Structure ready for gameplay logging and analytics

---

##  Version

**v0.5** — 50% progress milestone  
 Core game logic + UI complete  
 TODO:
- Gameplay logging to `gameplay_log.csv`
- Animated transitions and sound effects
- Settings
- Leaderboard

---

##  How to Run

```bash
python app.py
