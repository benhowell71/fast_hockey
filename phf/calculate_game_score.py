import pandas as pd
import numpy as np

from phf.phf_player_box import phf_player_box

game_df = phf_player_box(game_id=585655)
skaters_df = game_df[0]
skaters_df = skaters_df[skaters_df.team == 'Minnesota Whitecaps']

def calculate_game_score(skaters_df: pd.DataFrame) -> pd.DataFrame:

    weights = pd.read_csv('phf/weights.csv')

    skaters_df['offense_game_score'] = np.round((
        (skaters_df.goals * weights.goals_weight.item()) + 
        (skaters_df.assists * weights.assists_weight.item()) + 
        (skaters_df.shots_on_goal * weights.shots_on_goal_weight.item()) -
        (skaters_df.shots_blocked * weights.shots_blocked_weight.item())
    ), 2)

    skaters_df['defense_game_score'] = np.round((
        (skaters_df.blocks * weights.blocks_weight.item()) + 
        (skaters_df.takeaways * weights.takeaways_weight.item()) -
        (skaters_df.giveaways * weights.giveaways_weight.item())
    ), 2)

    skaters_df['faceoff_game_score'] = np.round((
        (skaters_df.faceoff_won * weights.faceoffs_won_weight.item()) -
        (skaters_df.faceoff_lost * weights.faceoffs_lost_weight.item())
    ), 2)

    skaters_df['penalty_game_score'] = np.round((
        -1 * (skaters_df.penalty_minutes * weights.penalty_minutes_weight.item())
    ), 2)

    skaters_df['game_score'] = np.round(skaters_df.offense_game_score + skaters_df.defense_game_score + skaters_df.faceoff_game_score + skaters_df.penalty_game_score, 2)

    return skaters_df