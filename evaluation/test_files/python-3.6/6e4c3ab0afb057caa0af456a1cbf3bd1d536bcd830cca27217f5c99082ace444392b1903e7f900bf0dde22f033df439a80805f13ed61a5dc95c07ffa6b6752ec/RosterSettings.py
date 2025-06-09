from __future__ import annotations
from dataclasses import dataclass

@dataclass(kw_only=True)
class RosterSettings:
    fpts: int
    fpts_against: int
    fpts_against_decimal: int
    fpts_decimal: int
    losses: int
    ppts: int
    ppts_decimal: int
    ties: int
    total_moves: int
    waiver_adjusted: int
    waiver_budget_used: int
    waiver_position: int
    wins: int

    @classmethod
    def from_dict(cls, roster_settings_dict: dict) -> RosterSettings:
        return RosterSettings(wins=roster_settings_dict.get('wins'), waiver_position=roster_settings_dict.get('waiver_position'), waiver_budget_used=roster_settings_dict.get('waiver_budget_used'), total_moves=roster_settings_dict.get('total_moves'), ties=roster_settings_dict.get('ties'), losses=roster_settings_dict.get('losses'), fpts_decimal=roster_settings_dict.get('fpts_decimal'), fpts_against_decimal=roster_settings_dict.get('fpts_against_decimal'), fpts_against=roster_settings_dict.get('fpts_against'), fpts=roster_settings_dict.get('fpts'), ppts_decimal=roster_settings_dict.get('ppts_decimal'), ppts=roster_settings_dict.get('ppts'), waiver_adjusted=roster_settings_dict.get('waiver_adjusted'))