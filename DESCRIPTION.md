# Lucky Chain Slot Machine

## Project Overview
**Lucky Chain Slot Machine** is a state-of-the-art interactive slot machine game that integrates **Markov Chain** principles to simulate state-dependent probabilities. The game offers a fun and engaging experience while also providing a robust backend for tracking player behavior, statistics, and real-time data visualizations.

### Key Features:
- **Markov Chain-Based Slot Machine Mechanics**: The outcome of each spin is determined by a Markov Chain, which introduces a dynamic, state-dependent probability system.
- **Player Profiles and Management**: Players can log in, top up their balance, place bets, and spin the slot machine, with their balance and stats saved across sessions.
- **Jackpot System**: A rare jackpot can be triggered by landing on a specific combination of symbols, providing excitement and increasing engagement.
- **Data Tracking and Visualization**: Player stats such as wins, losses, jackpots, and balance are tracked and visualized in graphs for better insights.
- **Responsive and Clean UI**: A user-friendly interface that makes the game accessible to players of all experience levels.

---

## Project Concept

### Game Mechanics:
1. **Game Flow**:
   - Players log in with their username and start with a balance (initially zero).
   - Players can top up their balance, place a bet, and spin the machine.
   - The slot machine has a dynamic outcome based on a **Markov Chain** model, where each spin's result is influenced by previous states.
   - Players win or lose based on the symbols displayed on the slot machine reels. If a player hits a specific combination (like three sevens), they win coins or even a jackpot.
   
2. **Markov Chain**:
   - The **Markov Chain** governs the state transitions of the game. It ensures that each spin’s outcome is dependent on the previous spin, providing more control over the probabilities of winning or losing.
   - The Markov Chain contains multiple states, each with specific probabilities for symbol combinations. The game dynamically adjusts these probabilities based on the state, simulating realistic slot machine behavior.
   
3. **UI and User Interaction**:
   - The **UI** class manages the graphical elements, ensuring the game is visually appealing and responsive.
   - Players can interact with the game using basic controls: pressing **Space** to spin and **ESC** to exit.
   - Player stats, such as balance and winnings, are displayed on the screen, with visual feedback for each win, loss, or jackpot hit.

### User Interaction:
- **Login**: Players log in by entering their name. If they are a returning player, their balance is automatically retrieved.
- **Gameplay**: Players place their bets and spin the machine. The game tracks wins, losses, and statistics in real-time.
- **Data Visualization**: After playing, players can view a detailed report of their performance, including graphs showing win/loss distributions and jackpot frequencies.

### Markov Chain:
The **Markov Chain** is central to the game mechanics:
- It models the state transitions between different stages of the game. 
- Each state represents a different probability distribution for the symbols on the slot machine.
- The Markov Chain ensures that outcomes are not entirely random, providing players with a sense of progression or change in difficulty.

---

## UML Class Diagram
The following UML class diagram illustrates the architecture of the **Lucky Chain Slot Machine** project. It provides a visual representation of the system, showing the main components of the game and how they interact with each other.

![UML Class Diagram](https://github.com/yourusername/yourproject/blob/main/images/uml_diagram.png)

*Note: The UML diagram is hosted in your GitHub repository. You can reference it in TPM using the HTML `<img>` tag.*

---

## Design Patterns and OOP Concepts
This project uses several Object-Oriented Programming (OOP) design patterns to ensure scalability and maintainability:

- **Singleton Pattern**: Used for the **Statistics** class to ensure that only one instance of statistics is tracked across the game.
- **Factory Pattern**: Used in the creation of the **Reel** objects, where each reel is dynamically generated based on the game state.
- **Strategy Pattern**: Applied to the **MarkovChain** class, allowing different strategies for determining spin outcomes depending on the game’s state.
  
### Object-Oriented Design:
- The game is organized into multiple classes, each representing a different aspect of the game (e.g., **Player**, **Machine**, **Statistics**).
- Each class has clear responsibilities and interactions with other classes, ensuring the system is modular and easy to maintain.
- The use of **inheritance** and **composition** helps to reduce code duplication and increase flexibility.
