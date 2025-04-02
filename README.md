# 🎮 HTML5 Game Generator

## Overview
This project is an **AI-powered HTML5 Game Generator** that takes a game description as input and generates a fully functional, single-page HTML5 game. The system consists of two AI agents: a **Game Developer Agent** that generates the game and a **QA Agent** that verifies the correctness and functionality of the game before saving it.

## Features
- Generates self-contained HTML5 games based on user descriptions.
- Ensures the game includes clear **instructions** and **alerts** when the player loses.
- Uses a **QA Agent** to validate the correctness and adherence to the given prompt.
- Saves the generated game as `unicorn.html` and opens it in a browser.
- Stores workflow sessions in an SQLite database for tracking purposes.

## Tech Stack
- **Python** - Core programming language
- **Groq (LLM)** - AI model used for game generation and QA evaluation
- **Agno** - AI agent workflow framework
- **Pydantic** - Data validation
- **SQLite** - Storage for workflow sessions
- **Rich** - CLI user interaction

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/game-generator.git
   cd game-generator
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. Set up environment variables (if required for Groq API).

## Usage
Run the script to generate a game:
```sh
python game_generator.py
```

- The script will prompt you to enter a game description.
- The **Game Developer Agent** will generate the game code.
- The **QA Agent** will verify the correctness of the game.
- If successful, the game will be saved as `unicorn.html` and opened in a browser.

## Example Game Description
```
The player must connect a power source to different lights by rotating and rearranging electrical circuit pieces on a grid. The goal is to complete the circuit before time runs out. Some tiles are locked in place, while others can be rotated or swapped. As the game progresses, new mechanics like splitters, switches, and faulty wires are introduced, making puzzles more challenging.
```

## File Structure
```
.
├── game_generator.py         # Main game generation script
├── requirements.txt          # Python dependencies
├── tmp/
│   ├── workflows.db          # SQLite database for workflow tracking
├── games/
│   ├── unicorn.html          # Generated game file
├── README.md                 # Project documentation
```

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, contact **Rithwik** at [rithwik.t2003@gmail.com](mailto:rithwik.t2003@gmail.com).
