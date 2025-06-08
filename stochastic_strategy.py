import argparse
from pathlib import Path

import pandas as pd


def compute_stochastic(df: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> pd.DataFrame:
    """Calculate %K and %D lines for the Stochastic Oscillator."""
    low_min = df['Low'].rolling(k_window).min()
    high_max = df['High'].rolling(k_window).max()
    df['%K'] = 100 * (df['Close'] - low_min) / (high_max - low_min)
    df['%D'] = df['%K'].rolling(d_window).mean()
    return df


def generate_signals(df: pd.DataFrame, overbought: float = 80, oversold: float = 20) -> pd.DataFrame:
    """Generate buy/sell signals based on %K and %D crossovers."""
    signals = []
    prev_k = df['%K'].shift(1)
    prev_d = df['%D'].shift(1)

    for k, d, pk, pd in zip(df['%K'], df['%D'], prev_k, prev_d):
        if pd is None or pk is None:
            signals.append(None)
            continue
        if pk < pd and k > d and k < oversold:
            signals.append('BUY')
        elif pk > pd and k < d and k > overbought:
            signals.append('SELL')
        else:
            signals.append(None)
    df['Signal'] = signals
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple Stochastic Oscillator strategy")
    parser.add_argument('csv', type=Path, help='Path to CSV with OHLC data')
    parser.add_argument('--k-window', type=int, default=14, help='Lookback window for %K')
    parser.add_argument('--d-window', type=int, default=3, help='Moving average window for %D')
    parser.add_argument('--overbought', type=float, default=80, help='Overbought threshold')
    parser.add_argument('--oversold', type=float, default=20, help='Oversold threshold')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_csv(args.csv, parse_dates=['Date'])
    df.sort_values('Date', inplace=True)

    df = compute_stochastic(df, k_window=args.k_window, d_window=args.d_window)
    df = generate_signals(df, overbought=args.overbought, oversold=args.oversold)

    last_signal = df.dropna(subset=['Signal']).tail(1)
    if not last_signal.empty:
        row = last_signal.iloc[0]
        print(f"{row['Date'].date()} -> {row['Signal']}")
    else:
        print("No recent signals")


if __name__ == '__main__':
    main()
