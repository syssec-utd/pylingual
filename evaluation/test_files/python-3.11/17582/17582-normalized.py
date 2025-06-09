def get_dense_lineups(df):
    """Returns a new DataFrame based on the one it is passed. Specifically, it
    adds five columns for each team (ten total), where each column has the ID
    of a player on the court during the play.

    This information is figured out sequentially from the game's substitution
    data in the passed DataFrame, so the DataFrame passed as an argument must
    be from a specific BoxScore (rather than a DataFrame of non-consecutive
    plays). That is, the DataFrame must be of the form returned by
    :func:`nba.BoxScore.pbp <nba.BoxScore.pbp>`.

    .. note:: Note that the lineups reflect the teams in the game when the play
        happened, not after the play. For example, if a play is a substitution,
        the lineups for that play will be the lineups before the substituion
        occurs.

    :param df: A DataFrame of a game's play-by-play data.
    :returns: A DataFrame with additional lineup columns.

    """
    assert df['boxscore_id'].nunique() == 1

    def lineup_dict(aw_lineup, hm_lineup):
        """Returns a dictionary of lineups to be converted to columns.
        Specifically, the columns are 'aw_player1' through 'aw_player5' and
        'hm_player1' through 'hm_player5'.

        :param aw_lineup: The away team's current lineup.
        :param hm_lineup: The home team's current lineup.
        :returns: A dictionary of lineups.
        """
        return {'{}_player{}'.format(tm, i + 1): player for tm, lineup in zip(['aw', 'hm'], [aw_lineup, hm_lineup]) for i, player in enumerate(lineup)}

    def handle_sub(row, aw_lineup, hm_lineup):
        """Modifies the aw_lineup and hm_lineup lists based on the substitution
        that takes place in the given row."""
        assert row['is_sub']
        sub_lineup = hm_lineup if row['sub_team'] == row['home'] else aw_lineup
        try:
            idx = sub_lineup.index(row['sub_out'])
            sub_lineup[idx] = row['sub_in']
        except ValueError:
            if row['sub_in'] in sub_lineup and row['sub_out'] not in sub_lineup:
                return (aw_lineup, hm_lineup)
            print('ERROR IN SUB IN {}, Q{}, {}: {}'.format(row['boxscore_id'], row['quarter'], row['clock_time'], row['detail']))
            raise
        return (aw_lineup, hm_lineup)
    per_starters = get_period_starters(df)
    cur_qtr = 0
    aw_lineup, hm_lineup = ([], [])
    df = df.reset_index(drop=True)
    lineups = [{} for _ in range(df.shape[0])]
    sub_or_per_start = df.is_sub | df.quarter.diff().astype(bool)
    for i, row in df.loc[sub_or_per_start].iterrows():
        if row['quarter'] > cur_qtr:
            assert row['quarter'] == cur_qtr + 1
            if cur_qtr > 0 and (not df.loc[i - 1, 'is_sub']):
                lineups[i - 1] = lineup_dict(aw_lineup, hm_lineup)
            cur_qtr += 1
            aw_lineup, hm_lineup = map(list, per_starters[cur_qtr - 1])
            lineups[i] = lineup_dict(aw_lineup, hm_lineup)
            if row['is_sub']:
                aw_lineup, hm_lineup = handle_sub(row, aw_lineup, hm_lineup)
        else:
            lineups[i] = lineup_dict(aw_lineup, hm_lineup)
            if row['is_sub']:
                aw_lineup, hm_lineup = handle_sub(row, aw_lineup, hm_lineup)
    lineup_df = pd.DataFrame(lineups)
    if lineup_df.iloc[-1].isnull().all():
        lineup_df.iloc[-1] = lineup_dict(aw_lineup, hm_lineup)
    lineup_df = lineup_df.groupby(df.quarter).fillna(method='bfill')
    bool_mat = lineup_df.isnull()
    mask = bool_mat.any(axis=1)
    if mask.any():
        bs = sportsref.nba.BoxScore(df.boxscore_id[0])
        stats = sportsref.nba.BoxScore(df.boxscore_id.iloc[0]).basic_stats()
        true_mp = pd.Series(stats.query('mp > 0')[['player_id', 'mp']].set_index('player_id').to_dict()['mp']) * 60
        calc_mp = pd.Series({p: (df.secs_elapsed.diff() * [p in row for row in lineup_df.values]).sum() for p in stats.query('mp > 0').player_id.values})
        diff = true_mp - calc_mp
        players_missing = diff.loc[diff.abs() >= 150]
        hm_roster = bs.basic_stats().query('is_home == True').player_id.values
        missing_df = pd.DataFrame({'secs': players_missing.values, 'is_home': players_missing.index.isin(hm_roster)}, index=players_missing.index)
        if missing_df.empty:
            print('There are NaNs in the lineup data, but no players were found to be missing significant minutes')
        else:
            for is_home, group in missing_df.groupby('is_home'):
                player_id = group.index.item()
                tm_cols = sportsref.nba.pbp.HM_LINEUP_COLS if is_home else sportsref.nba.pbp.AW_LINEUP_COLS
                row_mask = lineup_df[tm_cols].isnull().any(axis=1)
                lineup_df.loc[row_mask, tm_cols] = lineup_df.loc[row_mask, tm_cols].fillna(player_id).values
    return lineup_df