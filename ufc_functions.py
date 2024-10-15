import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import StandardScaler

ufc_fighters = pd.read_csv('Data_Collection/ufc_fighters.csv')
ufc_fights = pd.read_csv('Data_Collection/ufc_fights.csv')
ufc_fighters = ufc_fighters.drop(['Nickname'], axis=1)

ufc_fighters['DOB'] = pd.to_datetime(ufc_fighters['DOB'], errors='coerce')
ufc_fighters['age_d'] = (pd.Timestamp('today') - ufc_fighters['DOB']).dt.days

categorical_columns = ['Stance']
ufc_fighters = pd.get_dummies(ufc_fighters, columns=categorical_columns)

stats_columns = ['Streak', 'Height', 'Weight', 'Reach', 'Sig_Str_M', 'Sig_Str_Acc',
                 'Sig_Str_Abs_M', 'Str_Def', 'TD_Avg', 'TD_Acc', 'TD_Def', 'Sub_Avg', 'Wins', 'Losses',
                 'age_d', 'Stance_Open Stance', 'Stance_Orthodox', 'Stance_Sideways', 'Stance_Southpaw',
                 'Stance_Switch']

ufc_fighters = ufc_fighters.dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(ufc_fighters[stats_columns])

distance_matrix = pairwise_distances(X_scaled, metric='euclidean')

# Convert the distance matrix to a DataFrame for better readability
distance_df = pd.DataFrame(distance_matrix, index=ufc_fighters['Name'], columns=ufc_fighters['Name'])
np.fill_diagonal(distance_matrix, np.inf)


def fighter_compare_stats(f1, f2):
    f1_stats = ufc_fighters.loc[ufc_fighters['Name'].str.contains(f1)]
    f2_stats = ufc_fighters.loc[ufc_fighters['Name'].str.contains(f2)]
    stats = pd.concat([f1_stats, f2_stats], axis=0)
    return stats


def fights_profile(name):
    # Filter for rows where the fighter appears in either f1 or f2
    fights = ufc_fights[
        ufc_fights['f1'].str.contains(name, case=False) | ufc_fights['f2'].str.contains(name, case=False)].copy()

    # Define the columns that need to be swapped
    columns_to_swap = [
        ('f1Outcome', 'f2Outcome'), ('F1KD', 'F2KD'),
        ('f1_Sig_STR_pct', 'f2_Sig_STR_pct'), ('f1_TD_pct', 'f2_TD_pct'),
        ('f1_Sub_ATT', 'f2_Sub_ATT'), ('f1_Rev', 'f2_Rev'),
        ('f1_CTRL', 'f2_CTRL'), ('f1_Landed_Sig_STR', 'f2_Landed_Sig_STR'),
        ('f1_Thrown_sig_STR', 'f2_Thrown_sig_STR'), ('f1_Landed_total_STR', 'f2_Landed_total_STR'),
        ('f1_Landed_TD', 'f2_Landed_TD'), ('f1_Attempt_TD', 'f2_Attempt_TD')
    ]

    for index, row in fights.iterrows():
        # If fighter is in f2, swap f1 and f2 values
        if row['f2'].lower() == name.lower():
            # Swap f1 and f2 columns
            fights.at[index, 'f1'], fights.at[index, 'f2'] = row['f2'], row['f1']

            # Swap all the other necessary columns
            for f1_col, f2_col in columns_to_swap:
                fights.at[index, f1_col], fights.at[index, f2_col] = row[f2_col], row[f1_col]

            # After swapping, ensure 'f1' is assigned the fighter's name
            fights.at[index, 'f1'] = name

    return fights


def find_like(name):
    print(distance_df)



