import pandas as pd

pd.set_option('display.max_rows', None)

def football_data(df):
    attributes_input = input("Enter attributes separated by commas: ")
    if not attributes_input:
        raise ValueError("You must enter at least one attribute.")
    attributes = attributes_input.split(',')

    percentage_input = input("Enter the percentage (press Enter to use 100%): ")
    percentage = float(percentage_input) if percentage_input else 100

    max_value_input = input("Enter the maximum value (press Enter for no limit): ")
    max_value = float(max_value_input) if max_value_input else None

    max_age_input = input("Enter the maximum age (press Enter for no limit): ")
    max_age = int(max_age_input) if max_age_input else None

    position = input("Enter the position (press Enter for no specific position): ") or None

    # Initialize condition as a boolean Series that represents no condition
    condition = pd.Series(True, index=df.index)

    # Apply conditions if necessary
    if max_value is not None:
        condition &= (df['Value (in €)'] < max_value)

    if max_age is not None:
        condition &= (df['Age'] < max_age)

    if position is not None:
        condition &= (df['Pos'] == position)

    # Keep only players with correct condition
    players_with_correct_condition = df.loc[condition]

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

    # Return the DataFrame
    return best_players
