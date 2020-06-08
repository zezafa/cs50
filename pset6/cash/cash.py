#cash.py - asks how much change is owed then spits out the minimum number of coins with which said change can be made

from cs50 import get_float

def main():
    cash = 0
    cash = get_float("Change owed: ")

    while (cash < 0):
        cash = get_float("Change owed: ")

    cash = round(cash * 100)
    leastCoinsNeeded(cash)

def leastCoinsNeeded(coins):
    # Remember that in python 3.0 double backslash means integer/floor division
    curCoins = coins
    n = curCoins // 25
    curCoins = curCoins - 25 * n
    y = curCoins // 10
    curCoins = curCoins - 10 * y
    x = curCoins // 5
    curCoins = curCoins - 5 * x
    z = curCoins

    print(f"{int(n + y + x + z)}")

if __name__ == "__main__":
    main()