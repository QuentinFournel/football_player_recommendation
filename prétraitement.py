import pandas as pd # type: ignore

def prétraitement():
    players = pd.read_csv('dataset/players.csv', encoding='latin1', delimiter=',')

    valuations = pd.read_csv('dataset/player_valuations.csv', encoding='latin1', delimiter=',')

    value_df = pd.merge(players, valuations, on='player_id')

    value_df = value_df.drop_duplicates(subset=['player_id'])

    value_df = value_df[['name', 'market_value_in_eur_x']]

    value_df = value_df.rename(columns={'name': 'Player', 'market_value_in_eur_x': 'Value (in €)'})

    player_df = pd.read_csv('dataset/player_stats_22_23.csv', encoding='latin1', delimiter=';')

    df = pd.merge(player_df, value_df, on='Player')

    # Delete double players and keep the player with the highest value
    df = df.sort_values('Value (in €)', ascending=False).drop_duplicates('Player').sort_index()

    # Delete players with less than 10 games
    df = df[df['MP'] >= 10]

    return df