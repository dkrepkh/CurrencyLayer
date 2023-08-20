from currency_client import Client
from currency_gui import CurrencySelector
import api_tools


def main():
    api_key = api_tools.get_valid_api_key()
    if api_key:
        main_window = CurrencySelector(api_key)
        main_window.root.mainloop()


if __name__ == '__main__':
    main()