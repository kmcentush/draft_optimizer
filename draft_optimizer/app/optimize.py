from typing import Any, Dict, Set

import cvxpy as cp  # note: also need cvxopt installed
import numpy as np

# Prepare to specify lookup
GLOBALS: Dict[str, Any] = {
    "LOOKUP": {
        "UID_COL": "id",
        "POS_COL": "position",
        # WEEK_COLS,
        # ALL_IDX,
        # PLAYERS,
        # NUM_PLAYERS_CONST,
        # MIN_POS_CONST,
        # MAX_POS_CONST,
    }
}


def poss_opt_picks(team: int, picks_idx: Dict[int, Set[str]], picked_idx: Set[int]):
    # Get lookup
    LOOKUP = GLOBALS["LOOKUP"]
    UID_COL = LOOKUP["UID_COL"]
    POS_COL = LOOKUP["POS_COL"]
    WEEK_COLS = LOOKUP["WEEK_COLS"]
    ALL_IDX = LOOKUP["ALL_IDX"]
    PLAYERS = LOOKUP["PLAYERS"]
    NUM_PLAYERS_CONST = LOOKUP["NUM_PLAYERS_CONST"]
    MIN_POS_CONST = LOOKUP["MIN_POS_CONST"]
    MAX_POS_CONST = LOOKUP["MAX_POS_CONST"]

    # Get available players and those already picked by the team
    available_idx = ALL_IDX - picked_idx
    prev_picks_idx = picks_idx[team]
    available_idx |= prev_picks_idx
    available_idx = sorted(available_idx)

    # Get data
    uid_vals = PLAYERS.loc[available_idx, UID_COL].values
    pos_vals = PLAYERS.loc[available_idx, POS_COL].values
    points_vals = PLAYERS.loc[available_idx, WEEK_COLS].values

    # The variable we are solving for. We define our output variable as a bool
    # since we have to make a binary decision on each player (pick or don't pick)
    roster = cp.Variable(len(available_idx), boolean=True)

    # Save constraints
    constraints = list()

    # Our roster must be composed of exactly `num_players` players
    constraints.append(cp.sum(roster) == NUM_PLAYERS_CONST)

    # Define position constraints
    for pos in MIN_POS_CONST.keys():
        is_pos = pos_vals == pos
        pos_sum = cp.sum(is_pos @ roster)
        min_num = MIN_POS_CONST[pos]
        max_num = MAX_POS_CONST[pos]
        constraints.append(pos_sum >= min_num)
        constraints.append(pos_sum <= max_num)

    # Define constraints corresponding already picked players
    for idx in prev_picks_idx:
        did_pick = uid_vals == PLAYERS.loc[idx, UID_COL]
        constraints.append(cp.sum(did_pick @ roster) == 1)

    # Define the objective
    weekly_points = roster @ points_vals
    min_weekly_points = cp.min(weekly_points)
    objective = cp.Maximize(min_weekly_points)

    # Solve
    problem = cp.Problem(objective, constraints)
    problem.solve(max_iters=25)

    # Get result
    roster_idx = roster.value
    if roster_idx is not None:
        opt_roster = np.array(available_idx)[roster_idx.astype(bool)]  # re-align indices
        result = set(opt_roster)
    else:
        result = set()

    return result


def set_lookup(**kwargs):
    LOOKUP = GLOBALS["LOOKUP"]
    GLOBALS["LOOKUP"] = {**LOOKUP, **kwargs}
