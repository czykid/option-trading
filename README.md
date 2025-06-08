# Option Trading Strategies

This repository provides a basic daily option trading strategy using the Stochastic Oscillator. The strategy calculates %K and %D lines from daily OHLC data and generates buy or sell signals when predefined thresholds are crossed.

## Usage

1. Prepare a CSV file with columns: `Date`, `Open`, `High`, `Low`, `Close`.
2. Run `python stochastic_strategy.py path/to/your_data.csv`.
3. The script prints the most recent signal based on the %K and %D crossover logic.

Signals:
- **BUY**: %K crosses above %D while below the oversold threshold (default 20).
- **SELL**: %K crosses below %D while above the overbought threshold (default 80).

The thresholds and lookback periods can be changed with command line arguments. See `python stochastic_strategy.py --help` for details.
