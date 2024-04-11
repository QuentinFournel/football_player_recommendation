from prétraitement import prétraitement
from football_data import football_data

if __name__ == '__main__':
    df = prétraitement()
    df = football_data(df)
    df.to_csv('best_players.csv', index=False)
    print("DataFrame has been downloaded as 'best_players.csv'.")