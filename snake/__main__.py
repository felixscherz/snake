from snake import play
from curses import wrapper
import argparse

def main(options: argparse.Namespace):

    wrapper(play, width=options.width, height=options.height, tick_rate=options.tick_rate)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=40)
    parser.add_argument("--height", type=int, default=20)
    parser.add_argument("--tick-rate", type=float, default=0.3)
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    main(options)
