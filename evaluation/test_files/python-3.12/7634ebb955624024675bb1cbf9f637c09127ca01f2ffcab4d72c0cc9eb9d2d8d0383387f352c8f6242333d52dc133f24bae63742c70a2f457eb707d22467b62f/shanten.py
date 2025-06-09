from collections import defaultdict
from itertools import chain
from typing import List, Dict, Literal, Optional, Sequence, Tuple, Iterable, Callable, TypeVar
from pydantic import BaseModel
from mahjong_utils.internal.hand_utils import calc_regular_advance, regular_pattern_after_discard, regular_pattern_after_advance
from mahjong_utils.internal.legal_tiles_checker import ensure_legal_tiles
from mahjong_utils.internal.regular_hand_pattern_searcher import regular_hand_pattern_search
from mahjong_utils.models.furo import Furo
from mahjong_utils.models.hand import Hand
from mahjong_utils.models.hand_pattern import ChitoiHandPattern, KokushiHandPattern, RegularHandPattern, HandPattern
from mahjong_utils.models.shanten import ShantenWithGot, ShantenWithoutGot, Shanten, ShantenInfoMixin
from mahjong_utils.models.tile import Tile, is_yaochu, all_yaochu

class ShantenResult(BaseModel, ShantenInfoMixin):
    type: Literal['regular', 'chitoi', 'kokushi', 'union']
    hand: Hand
    shanten_info: Shanten

class UnionShantenResult(ShantenResult):
    regular: ShantenResult
    chitoi: Optional[ShantenResult]
    kokushi: Optional[ShantenResult]

def calc_regular_shanten(pattern: RegularHandPattern):
    shanten = 2 * (pattern.k - len(pattern.menzen_mentsu) - len(pattern.furo)) - len(pattern.tatsu)
    if pattern.jyantou is not None:
        shanten -= 1
    return shanten

def calc_chitoi_shanten(pattern: ChitoiHandPattern):
    return 6 - len(pattern.pairs)

def calc_kokushi_shanten(pattern: KokushiHandPattern):
    if pattern.repeated is not None:
        shanten_num = 12 - len(pattern.yaochu)
    else:
        shanten_num = 13 - len(pattern.yaochu)
    return shanten_num

def _fill_advance_num_by_remaining(shanten_info: ShantenWithoutGot, remaining: dict):
    advance_num = 0
    for t in shanten_info.advance:
        advance_num += remaining[t]
    shanten_info.advance_num = advance_num
    if shanten_info.well_shape_advance is not None:
        well_shape_advance_num = 0
        for t in shanten_info.well_shape_advance:
            well_shape_advance_num += remaining[t]
        shanten_info.well_shape_advance_num = well_shape_advance_num

def _fill_advance_num(shanten_info: Shanten, *tiles: Tile):
    remaining = defaultdict(lambda: 4)
    for t in tiles:
        remaining[t] -= 1
    if isinstance(shanten_info, ShantenWithoutGot):
        _fill_advance_num_by_remaining(shanten_info, remaining)
    elif isinstance(shanten_info, ShantenWithGot):
        for shanten_info_after_discard in shanten_info.discard_to_advance.values():
            _fill_advance_num_by_remaining(shanten_info_after_discard, remaining)
T_HP = TypeVar('T_HP', bound=HandPattern)

def _select_best_patterns(patterns: Iterable[T_HP], calc_shanten: Callable[[T_HP], int]) -> Tuple[int, Sequence[T_HP]]:
    best_shanten = 100
    best_patterns = []
    for pat in patterns:
        pat_shanten = calc_shanten(pat)
        if pat_shanten < best_shanten:
            best_shanten = pat_shanten
            best_patterns = []
        if pat_shanten == best_shanten:
            best_patterns.append(pat)
    return (best_shanten, best_patterns)

def _handle_regular_shanten_without_got(patterns: Iterable[RegularHandPattern], calc_well_shape_advance: bool=True) -> Tuple[ShantenWithoutGot, Sequence[RegularHandPattern]]:
    best_shanten, best_patterns = _select_best_patterns(patterns, calc_regular_shanten)
    advance = set()
    for pat in best_patterns:
        advance |= calc_regular_advance(pat)
    shanten_info = ShantenWithoutGot(shanten=best_shanten, advance=advance)
    if calc_well_shape_advance and shanten_info.shanten == 1:
        well_shape = set()
        for adv in shanten_info.advance:
            patterns_after_adv = set()
            for pat in best_patterns:
                for pat_after_discard in regular_pattern_after_advance(pat, adv):
                    patterns_after_adv.add(pat_after_discard)
            shanten_after_adv, _ = _handle_regular_shanten_with_got(patterns_after_adv, calc_well_shape_advance=False, best_shanten_only=True)
            _fill_advance_num(shanten_after_adv, adv, *best_patterns[0].tiles, *chain(*map(lambda fr: fr.tiles, best_patterns[0].furo)))
            max_adv_after_adv = max(map(lambda x: x.advance_num, shanten_after_adv.discard_to_advance.values()))
            if max_adv_after_adv > 4:
                well_shape.add(adv)
        shanten_info.well_shape_advance = well_shape
    return (shanten_info, best_patterns)

def _handle_regular_shanten_with_got(patterns: Iterable[RegularHandPattern], calc_well_shape_advance: bool=True, best_shanten_only: bool=False) -> Tuple[ShantenWithGot, Sequence[RegularHandPattern]]:
    best_shanten, best_patterns = _select_best_patterns(patterns, calc_regular_shanten)
    discard_to_advance = dict()
    for discard in set(best_patterns[0].tiles):
        patterns_after_discard = set()
        for pat in best_patterns:
            for pat_after_discard in regular_pattern_after_discard(pat, discard):
                patterns_after_discard.add(pat_after_discard)
        shanten_after_discard, _ = _handle_regular_shanten_without_got(patterns_after_discard, calc_well_shape_advance)
        discard_to_advance[discard] = shanten_after_discard
    if best_shanten_only:
        for t in list(discard_to_advance.keys()):
            if discard_to_advance[t].shanten != best_shanten:
                del discard_to_advance[t]
    shanten_info = ShantenWithGot(shanten=best_shanten, discard_to_advance=discard_to_advance)
    return (shanten_info, best_patterns)

def regular_shanten(tiles: Sequence[Tile], furo: Optional[Sequence[Furo]]=None, calc_advance_num: bool=True) -> ShantenResult:
    tiles = ensure_legal_tiles(tiles)
    if furo is None:
        furo = []
    patterns = regular_hand_pattern_search(tiles, furo)
    with_got = len(tiles) % 3 == 2
    if with_got:
        shanten_info, best_patterns = _handle_regular_shanten_with_got(patterns)
    else:
        shanten_info, best_patterns = _handle_regular_shanten_without_got(patterns)
    if calc_advance_num:
        _fill_advance_num(shanten_info, *best_patterns[0].tiles, *chain(*map(lambda fr: fr.tiles, best_patterns[0].furo)))
    hand = Hand(tiles=tiles, furo=furo, patterns=best_patterns)
    result = ShantenResult(type='regular', hand=hand, shanten_info=shanten_info)
    return result

def _build_chitoi_pattern(tiles: Iterable[Tile]):
    cnt: Dict[Tile, int] = {}
    for t in tiles:
        cnt[t] = cnt.get(t, 0) + 1
    pairs = []
    remaining = []
    for t in cnt:
        if cnt[t] >= 2:
            pairs.append(t)
            for i in range(cnt[t] - 2):
                remaining.append(t)
        elif cnt[t] == 1:
            remaining.append(t)
    pattern = ChitoiHandPattern(pairs=frozenset(pairs), remaining=tuple(remaining))
    return pattern

def _handle_chitoi_shanten_without_got(tiles: Iterable[Tile]) -> Tuple[ShantenWithoutGot, ChitoiHandPattern]:
    pattern = _build_chitoi_pattern(tiles)
    advance = set()
    for t in pattern.remaining:
        if t not in pattern.pairs:
            advance.add(t)
    shanten_num = calc_chitoi_shanten(pattern)
    shanten_info = ShantenWithoutGot(shanten=shanten_num, advance=advance)
    if shanten_num == 1:
        shanten_info.well_shape_advance = set()
    return (shanten_info, pattern)

def _handle_chitoi_shanten_with_got(tiles: Sequence[Tile]) -> Tuple[ShantenWithGot, ChitoiHandPattern]:
    pattern = _build_chitoi_pattern(tiles)
    shanten_num = calc_chitoi_shanten(pattern)
    discard_to_advance = dict()
    if shanten_num != -1:
        tiles = tuple(tiles)
        for t in set(tiles):
            t_idx = tiles.index(t)
            shanten_after_discard, _ = _handle_chitoi_shanten_without_got(tiles[:t_idx] + tiles[t_idx + 1:])
            discard_to_advance[t] = shanten_after_discard
    shanten_info = ShantenWithGot(shanten=shanten_num, discard_to_advance=discard_to_advance)
    return (shanten_info, pattern)

def chitoi_shanten(tiles: Sequence[Tile], calc_advance_num: bool=True) -> ShantenResult:
    tiles = ensure_legal_tiles(tiles, False)
    if len(tiles) == 13:
        shanten_info, pattern = _handle_chitoi_shanten_without_got(tiles)
    else:
        shanten_info, pattern = _handle_chitoi_shanten_with_got(tiles)
    if calc_advance_num:
        _fill_advance_num(shanten_info, *tiles)
    hand = Hand(tiles=tiles, patterns=[pattern])
    result = ShantenResult(type='chitoi', hand=hand, shanten_info=shanten_info)
    return result

def _build_kokushi_pattern(tiles: Iterable[Tile]) -> Sequence[KokushiHandPattern]:
    yaochu = set()
    repeated = set()
    remaining = []
    for t in tiles:
        if is_yaochu(t):
            if t in yaochu:
                if t in repeated:
                    remaining.append(t)
                else:
                    repeated.add(t)
            else:
                yaochu.add(t)
        else:
            remaining.append(t)
    yaochu = frozenset(yaochu)
    remaining = tuple(remaining)
    patterns = []
    if len(repeated) > 0:
        for t in repeated:
            pat = KokushiHandPattern(yaochu=yaochu, repeated=t, remaining=(*remaining, *repeated.difference([t])))
            patterns.append(pat)
    else:
        pat = KokushiHandPattern(yaochu=yaochu, repeated=None, remaining=remaining)
        patterns.append(pat)
    return patterns

def _handle_kokushi_shanten_without_got(tiles: Sequence[Tile]) -> Tuple[ShantenWithoutGot, Sequence[KokushiHandPattern]]:
    patterns = _build_kokushi_pattern(tiles)
    shanten_num, patterns = _select_best_patterns(patterns, calc_kokushi_shanten)
    pat = patterns[0]
    if pat.repeated is not None:
        advance = all_yaochu - pat.yaochu
        if shanten_num == 1:
            well_shape_advance = set()
        else:
            well_shape_advance = None
    else:
        advance = all_yaochu.copy()
        if shanten_num == 1:
            well_shape_advance = all_yaochu - pat.yaochu
        else:
            well_shape_advance = None
    shanten_info = ShantenWithoutGot(shanten=shanten_num, advance=advance, well_shape_advance=well_shape_advance)
    return (shanten_info, patterns)

def _handle_kokushi_shanten_with_got(tiles: Sequence[Tile]) -> Tuple[ShantenWithGot, Sequence[KokushiHandPattern]]:
    patterns = _build_kokushi_pattern(tiles)
    shanten_num, patterns = _select_best_patterns(patterns, calc_kokushi_shanten)
    discard_to_advance = dict()
    if shanten_num != -1:
        tiles = tuple(tiles)
        for t in set(tiles):
            t_idx = tiles.index(t)
            shanten_after_discard, _ = _handle_kokushi_shanten_without_got(tiles[:t_idx] + tiles[t_idx + 1:])
            shanten_num = min(shanten_num, shanten_after_discard.shanten)
            discard_to_advance[t] = shanten_after_discard
    shanten_info = ShantenWithGot(shanten=shanten_num, discard_to_advance=discard_to_advance)
    return (shanten_info, _build_kokushi_pattern(tiles))

def kokushi_shanten(tiles: Sequence[Tile], calc_advance_num: bool=True) -> ShantenResult:
    tiles = ensure_legal_tiles(tiles, False)
    if len(tiles) == 13:
        shanten_info, patterns = _handle_kokushi_shanten_without_got(tiles)
    else:
        shanten_info, patterns = _handle_kokushi_shanten_with_got(tiles)
    if calc_advance_num:
        _fill_advance_num(shanten_info, *tiles)
    hand = Hand(tiles=tiles, patterns=patterns)
    result = ShantenResult(type='kokushi', hand=hand, shanten_info=shanten_info)
    return result

def shanten(tiles: List[Tile], furo: Optional[List[Furo]]=None, calc_advance_num: bool=True) -> UnionShantenResult:
    tiles = ensure_legal_tiles(tiles)
    if furo is None:
        furo = []
    with_got = len(tiles) % 3 == 2
    k = len(tiles) // 3
    if k != 4:
        regular = regular_shanten(tiles, furo, calc_advance_num)
        return UnionShantenResult(type='union', hand=regular.hand, shanten_info=regular.shanten_info, regular=regular, chitoi=None, kokushi=None)
    regular = regular_shanten(tiles, furo, calc_advance_num=False)
    chitoi = chitoi_shanten(tiles, calc_advance_num=False)
    kokushi = kokushi_shanten(tiles, calc_advance_num=False)
    shanten_num = min(regular.shanten, chitoi.shanten, kokushi.shanten)
    patterns = []
    if not with_got:
        advance_aggregated = set()
        well_shape_advance_aggregated = set() if shanten_num == 1 else None
        if regular.shanten == shanten_num:
            advance_aggregated |= regular.advance
            patterns += regular.hand.patterns
            if shanten_num == 1:
                well_shape_advance_aggregated |= regular.well_shape_advance
        if chitoi.shanten == shanten_num:
            advance_aggregated |= chitoi.advance
            patterns += chitoi.hand.patterns
            if shanten_num == 1:
                well_shape_advance_aggregated |= chitoi.well_shape_advance
        if kokushi.shanten == shanten_num:
            advance_aggregated |= kokushi.advance
            patterns += kokushi.hand.patterns
            if shanten_num == 1:
                well_shape_advance_aggregated |= kokushi.well_shape_advance
        shanten_info = ShantenWithoutGot(shanten=shanten_num, advance=advance_aggregated, well_shape_advance=well_shape_advance_aggregated)
    else:
        discard_to_advance_aggregated = dict()
        for discard, advance in regular.discard_to_advance.items():
            if discard not in discard_to_advance_aggregated or discard_to_advance_aggregated[discard].shanten > advance.shanten:
                discard_to_advance_aggregated[discard] = advance
            elif discard_to_advance_aggregated[discard].shanten == advance.shanten:
                discard_to_advance_aggregated[discard].advance |= advance.advance
                if discard_to_advance_aggregated[discard].shanten == 1:
                    discard_to_advance_aggregated[discard].well_shape_advance |= advance.well_shape_advance
        patterns += regular.hand.patterns
        for discard, advance in chitoi.discard_to_advance.items():
            if discard not in discard_to_advance_aggregated or discard_to_advance_aggregated[discard].shanten > advance.shanten:
                discard_to_advance_aggregated[discard] = advance
            elif discard_to_advance_aggregated[discard].shanten == advance.shanten:
                discard_to_advance_aggregated[discard].advance |= advance.advance
                if discard_to_advance_aggregated[discard].shanten == 1:
                    discard_to_advance_aggregated[discard].well_shape_advance |= advance.well_shape_advance
        patterns += chitoi.hand.patterns
        for discard, advance in kokushi.discard_to_advance.items():
            if discard not in discard_to_advance_aggregated or discard_to_advance_aggregated[discard].shanten > advance.shanten:
                discard_to_advance_aggregated[discard] = advance
            elif discard_to_advance_aggregated[discard].shanten == advance.shanten:
                discard_to_advance_aggregated[discard].advance |= advance.advance
                if discard_to_advance_aggregated[discard].shanten == 1:
                    discard_to_advance_aggregated[discard].well_shape_advance |= advance.well_shape_advance
        patterns += kokushi.hand.patterns
        shanten_info = ShantenWithGot(shanten=shanten_num, discard_to_advance=discard_to_advance_aggregated)
    if calc_advance_num:
        _fill_advance_num(shanten_info, *tiles, *chain(*map(lambda fr: fr.tiles, furo)))
    hand = Hand(tiles=tiles, furo=furo, patterns=patterns)
    return UnionShantenResult(type='union', hand=hand, shanten_info=shanten_info, regular=regular, chitoi=chitoi, kokushi=kokushi)
__all__ = ('regular_shanten', 'chitoi_shanten', 'kokushi_shanten', 'shanten', 'ShantenResult', 'UnionShantenResult')