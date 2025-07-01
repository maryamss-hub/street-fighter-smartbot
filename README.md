
# Street Fighter II Turbo Game Bot using ML

An AI bot that uses a trained MLP model to play Street Fighter II Turbo based on real-time game state input. Built with the BizHawk emulator and Python.

## Features

- Game state extraction from emulator
- Custom dataset generation through gameplay
- Feature engineering for spatial and status data
- MLP model trained to predict button actions
- Works for both Player 1 and Player 2

## Technologies Used

- Python
- scikit-learn
- BizHawk Emulator
- pandas, NumPy

## How to Run

1. Install BizHawk and configure for Python socket control
2. Generate gameplay data (`controller.py`)
3. Train MLP model using `manual_game_data.csv`
4. Replace rule-based logic in `bot.py` with ML predictions

## Future Improvements

- Use larger and more diverse training data
- Add combo detection and opponent prediction
