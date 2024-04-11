import pandas as pd
from prétraitement import prétraitement

def football_data():
    df = prétraitement()

    attributes_input = input("Enter attributes separated by commas: ")
    attributes = attributes_input.split(',') if attributes_input else None

    percentage_input = input("Enter the percentage: ")
    percentage = float(percentage_input) if percentage_input else 100

    max_value_input = input("Enter the maximum value: ")
    max_value = float(max_value_input) if max_value_input else None

    max_age_input = input("Enter the maximum age: ")
    max_age = int(max_age_input) if max_age_input else None

    position = input("Enter the position: ") or None

    # Keep only players with correct condition
    condition_value = (df['Value (in €)'] < max_value) if max_value is not None else True
    condition_age = (df['Age'] < max_age) if max_age is not None else True
    condition_position = (df['Pos'] == position) if position is not None else True

    if (condition_value and condition_age and condition_position) is not True:
        players_with_correct_condition = df[condition_value & condition_age & condition_position]
    else:
        players_with_correct_condition = df

    best_players = pd.DataFrame()

    for attribute in attributes:
        # Select top percentage of players for each attribute
        top_percentage_players = players_with_correct_condition.nlargest(int(len(df) * percentage / 100), attribute)
        
        # Delete players that have 0 in the attribute
        top_percentage_players = top_percentage_players[top_percentage_players[attribute] > 0]

        # Add the selected players to the 'best_player' DataFrame
        best_players = pd.concat([best_players, top_percentage_players], ignore_index=True)

    # Keep only the players that are duplicated if there are more than one attribute
    if len(attributes) > 1:
        best_players = best_players[best_players.duplicated(subset='Player', keep=False)]

    # Drop duplicates
    best_players = best_players.drop_duplicates(subset='Player')

    # Sort the DataFrame by the attributes
    best_players = best_players.sort_values(by=attributes, ascending=False)

    # Keep only the columns of interest
    best_players = best_players[['Player', 'Age', 'Squad', 'Comp', 'Nation', 'Pos', 'Value (in €)'] + attributes]

    # Display the resulting DataFrame
    return best_players

if __name__ == '__main__':
    print(football_data())
