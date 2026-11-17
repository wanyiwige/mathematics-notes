export type UnoColor = 'red' | 'yellow' | 'green' | 'blue';
export type CardColor = UnoColor | 'wild';
export type CardValue = `${number}` | 'skip' | 'reverse' | 'draw1' | 'draw3' | 'wild' | 'wild2' | 'wild5' | 'swapAll' | 'swapTwo' | 'reflect';

export type Card = {
  id: string;
  color: CardColor;
  value: CardValue;
};

export type Player = {
  id: string;
  name: string;
  avatarUrl?: string | null;
  hand: Card[];
};

export type WildChallenge = {
  playerId: string;
  chosenColor: UnoColor;
  hadMatchingColor: boolean;
};

export type GameRules = {
  stackDraw: boolean;
  drawToPlay: boolean;
};

export type GameState = {
  players: Player[];
  phase: 'claiming' | 'playing';
  currentPlayer: number;
  direction: 1 | -1;
  drawPile: Card[];
  discardPile: Card[];
  currentColor: UnoColor;
  pendingDraw: number;
  pendingKind: 'colorDraw' | 'wildDraw' | null;
  drawnCardId: string | null;
  unoArmed: boolean;
  unoDeclaredPlayerIds: string[];
  reportablePlayerId: string | null;
  wildChallenge: WildChallenge | null;
  finishedPlayerIds: string[];
  winnerId: string | null;
  lastPlayerId: string | null;
  turn: number;
  message: string;
  rules: GameRules;
};

export const COLORS: UnoColor[] = ['red', 'yellow', 'green', 'blue'];

export const COLOR_LABELS: Record<UnoColor, string> = {
  red: '红色',
  yellow: '黄色',
  green: '绿色',
  blue: '蓝色',
};

export const VALUE_LABELS: Record<string, string> = {
  skip: '⊘',
  reverse: '↻',
  draw1: '+1',
  draw3: '+3',
  wild: 'W',
  wild2: '+2',
  wild5: '+5',
  swapAll: '⇥',
  swapTwo: '⇄',
  reflect: '⤺',
};

function makeCard(color: CardColor, value: CardValue, index: number): Card {
  return { id: `${color}-${value}-${index}`, color, value };
}

export function createDeck(): Card[] {
  const cards: Card[] = [];
  COLORS.forEach((color) => {
    cards.push(makeCard(color, '0', 0));
    for (let value = 1; value <= 9; value += 1) {
      cards.push(makeCard(color, `${value}`, 0), makeCard(color, `${value}`, 1));
    }
    (['skip', 'reverse'] as const).forEach((value) => {
      cards.push(makeCard(color, value, 0), makeCard(color, value, 1));
    });
    for (let index = 0; index < 2; index += 1) {
      cards.push(makeCard(color, 'draw1', index), makeCard(color, 'draw3', index));
    }
  });
  for (let index = 0; index < 4; index += 1) {
    cards.push(makeCard('wild', 'wild', index));
  }
  for (let index = 0; index < 2; index += 1) {
    cards.push(makeCard('wild', 'wild2', index), makeCard('wild', 'wild5', index));
  }
  cards.push(makeCard('wild', 'swapAll', 0), makeCard('wild', 'swapTwo', 0));
  for (let index = 0; index < 4; index += 1) {
    cards.push(makeCard('wild', 'reflect', index));
  }
  return cards;
}

export function shuffle<T>(items: T[]): T[] {
  const result = [...items];
  for (let index = result.length - 1; index > 0; index -= 1) {
    const other = Math.floor(Math.random() * (index + 1));
    [result[index], result[other]] = [result[other], result[index]];
  }
  return result;
}

function nextPlayerIndex(state: Pick<GameState, 'players' | 'currentPlayer' | 'direction'> & Partial<Pick<GameState, 'finishedPlayerIds'>>, steps = 1) {
  const total = state.players.length;
  const finished = new Set(state.finishedPlayerIds ?? []);
  if (state.players.every((player) => finished.has(player.id))) return state.currentPlayer;

  let index = state.currentPlayer;
  let remaining = steps;
  while (remaining > 0) {
    index = (index + state.direction + total) % total;
    if (!finished.has(state.players[index].id)) remaining -= 1;
  }
  return index;
}

export function normalizeGameState(state: GameState): GameState {
  const phase = state.phase ?? 'playing';
  const finishedPlayerIds = state.finishedPlayerIds ?? state.players.filter((player) => player.hand.length === 0).map((player) => player.id);
  const unoDeclaredPlayerIds = (state.unoDeclaredPlayerIds ?? []).filter((playerId) => state.players.some((player) => player.id === playerId && player.hand.length === 1));
  const activePlayers = state.players.filter((player) => !finishedPlayerIds.includes(player.id));
  const winnerId = state.winnerId ?? finishedPlayerIds[0] ?? null;
  const lastPlayerId = state.lastPlayerId ?? (finishedPlayerIds.length > 0 && activePlayers.length <= 1 ? activePlayers[0]?.id ?? null : null);
  const currentIsFinished = finishedPlayerIds.includes(state.players[state.currentPlayer]?.id);
  const normalized = { ...state, phase, unoDeclaredPlayerIds, wildChallenge: state.wildChallenge ?? null, finishedPlayerIds, winnerId, lastPlayerId };
  return currentIsFinished && !lastPlayerId
    ? { ...normalized, currentPlayer: nextPlayerIndex(normalized) }
    : normalized;
}

function drawFromPile(state: GameState, count: number): { cards: Card[]; drawPile: Card[]; discardPile: Card[] } {
  let drawPile = [...state.drawPile];
  let discardPile = [...state.discardPile];
  const cards: Card[] = [];

  while (cards.length < count) {
    if (drawPile.length === 0) {
      const top = discardPile[discardPile.length - 1];
      const recyclable = discardPile.slice(0, -1);
      if (!top || recyclable.length === 0) break;
      drawPile = shuffle(recyclable);
      discardPile = [top];
    }
    const card = drawPile.pop();
    if (card) cards.push(card);
  }
  return { cards, drawPile, discardPile };
}

export function createGame(names: string[], rules: GameRules, avatars: Array<string | null> = []): GameState {
  const deck = shuffle(createDeck());
  const players: Player[] = names.map((name, index) => ({
    id: `player-${Date.now()}-${index}`,
    name: name.trim() || `玩家 ${index + 1}`,
    avatarUrl: avatars[index] ?? null,
    hand: [],
  }));

  for (let round = 0; round < 7; round += 1) {
    players.forEach((player) => {
      const card = deck.pop();
      if (card) player.hand.push(card);
    });
  }

  let firstCardIndex = deck.findIndex((card) => card.color !== 'wild' && !['draw1', 'draw3', 'skip', 'reverse'].includes(card.value));
  if (firstCardIndex < 0) firstCardIndex = deck.length - 1;
  const [firstCard] = deck.splice(firstCardIndex, 1);

  return {
    players,
    phase: 'claiming',
    currentPlayer: 0,
    direction: 1,
    drawPile: deck,
    discardPile: [firstCard],
    currentColor: firstCard.color as UnoColor,
    pendingDraw: 0,
    pendingKind: null,
    drawnCardId: null,
    unoArmed: false,
    unoDeclaredPlayerIds: [],
    reportablePlayerId: null,
    wildChallenge: null,
    finishedPlayerIds: [],
    winnerId: null,
    lastPlayerId: null,
    turn: 0,
    message: '等待所有玩家抢先手',
    rules,
  };
}

export function claimFirstTurn(state: GameState, playerId: string): GameState {
  state = normalizeGameState(state);
  if (state.phase !== 'claiming') return state;
  const playerIndex = state.players.findIndex((player) => player.id === playerId && !state.finishedPlayerIds.includes(player.id));
  if (playerIndex < 0) return state;
  return {
    ...state,
    phase: 'playing',
    currentPlayer: playerIndex,
    turn: 1,
    message: `${state.players[playerIndex].name} 抢到了先手！`,
  };
}

export function canPlayCard(state: GameState, card: Card): boolean {
  if (state.phase === 'claiming') return false;
  if (state.lastPlayerId) return false;
  if (state.drawnCardId && state.drawnCardId !== card.id) return false;
  if (state.pendingDraw > 0) {
    if (card.value === 'reflect') return true;
    if (!state.rules.stackDraw) return false;
    if (state.pendingKind === 'wildDraw') return card.value === 'wild2' || card.value === 'wild5';
    return ['draw1', 'draw3', 'wild2', 'wild5'].includes(card.value);
  }
  const top = state.discardPile[state.discardPile.length - 1];
  return card.color === 'wild' || card.color === state.currentColor || card.value === top?.value;
}

export function playCard(state: GameState, cardId: string, chosenColor?: UnoColor, swapPair?: [string, string]): GameState {
  state = normalizeGameState(state);
  const player = state.players[state.currentPlayer];
  const card = player.hand.find((item) => item.id === cardId);
  if (!card || !canPlayCard(state, card)) return state;
  const needsColor = ['wild', 'wild2', 'wild5', 'reflect'].includes(card.value);
  if (needsColor && !chosenColor) return state;
  if (card.value === 'swapTwo' && (!swapPair || swapPair[0] === swapPair[1])) return state;

  let players = state.players.map((item, index) => index === state.currentPlayer
    ? { ...item, hand: item.hand.filter((held) => held.id !== cardId) }
    : item);
  let direction = state.direction;
  let steps = 1;
  let pendingDraw = state.pendingDraw;
  let pendingKind = state.pendingKind;
  let actionMessage = `${player.name} 打出了 ${VALUE_LABELS[card.value] ?? card.value}`;
  const canBeChallenged = ['wild', 'wild2', 'wild5'].includes(card.value) && !!chosenColor;
  const wildChallenge: WildChallenge | null = canBeChallenged ? {
    playerId: player.id,
    chosenColor: chosenColor!,
    hadMatchingColor: player.hand.some((held) => held.id !== cardId && held.color === chosenColor),
  } : null;

  if (card.value === 'reverse') {
    direction = state.direction === 1 ? -1 : 1;
    if (players.length - state.finishedPlayerIds.length === 2) steps = 2;
  } else if (card.value === 'skip') {
    steps = 2;
  } else if (card.value === 'draw1' || card.value === 'draw3') {
    pendingDraw += card.value === 'draw1' ? 1 : 3;
    pendingKind = 'colorDraw';
  } else if (card.value === 'wild2' || card.value === 'wild5') {
    pendingDraw += card.value === 'wild2' ? 2 : 5;
    pendingKind = 'wildDraw';
  } else if (card.value === 'reflect') {
    const reflectedCount = state.pendingDraw;
    direction = state.direction === 1 ? -1 : 1;
    steps = reflectedCount > 0 ? 1 : players.length - state.finishedPlayerIds.length === 2 ? 2 : 1;
    actionMessage = reflectedCount > 0
      ? `${player.name} 弹返了 ${reflectedCount} 张罚牌！`
      : `${player.name} 用弹返牌改变了方向`;
  } else if (card.value === 'swapAll') {
    const activeIndexes = players.map((item, index) => state.finishedPlayerIds.includes(item.id) ? -1 : index).filter((index) => index >= 0);
    const activeHands = activeIndexes.map((index) => players[index].hand);
    players = players.map((item, index) => {
      const activePosition = activeIndexes.indexOf(index);
      return activePosition < 0 ? item : { ...item, hand: activeHands[(activePosition - 1 + activeHands.length) % activeHands.length] };
    });
    actionMessage = `${player.name} 发起了全员顺时针换牌`;
  } else if (card.value === 'swapTwo' && swapPair) {
    const firstIndex = players.findIndex((item) => item.id === swapPair[0]);
    const secondIndex = players.findIndex((item) => item.id === swapPair[1]);
    if (firstIndex < 0 || secondIndex < 0 || state.finishedPlayerIds.includes(players[firstIndex].id) || state.finishedPlayerIds.includes(players[secondIndex].id)) return state;
    const firstHand = players[firstIndex].hand;
    const secondHand = players[secondIndex].hand;
    players = players.map((item, index) => index === firstIndex
      ? { ...item, hand: secondHand }
      : index === secondIndex
        ? { ...item, hand: firstHand }
        : item);
    actionMessage = `${players[firstIndex].name} 与 ${players[secondIndex].name} 交换了手牌`;
  }

  const newlyFinished = players.filter((item) => item.hand.length === 0 && !state.finishedPlayerIds.includes(item.id));
  const finishedPlayerIds = [...state.finishedPlayerIds, ...newlyFinished.map((item) => item.id)];
  const activePlayers = players.filter((item) => !finishedPlayerIds.includes(item.id));
  const winnerId = state.winnerId ?? finishedPlayerIds[0] ?? null;
  const lastPlayerId = activePlayers.length <= 1 && finishedPlayerIds.length > 0 ? activePlayers[0]?.id ?? null : null;
  const remaining = players[state.currentPlayer].hand.length;
  const reportablePlayerId = remaining === 1 && !state.unoArmed ? player.id : null;
  const unoDeclaredPlayerIds = state.unoDeclaredPlayerIds
    .filter((playerId) => players.some((item) => item.id === playerId && item.hand.length === 1));
  if (remaining === 1 && state.unoArmed && !unoDeclaredPlayerIds.includes(player.id)) unoDeclaredPlayerIds.push(player.id);
  const partial = { ...state, players, direction, finishedPlayerIds };
  const nextIndex = nextPlayerIndex(partial, steps);
  const finishedNames = newlyFinished.map((item) => item.name).join('、');
  const lastPlayer = activePlayers[0];
  const message = wildChallenge
    ? `${player.name} 将颜色改为${COLOR_LABELS[wildChallenge.chosenColor]}，其他玩家可以质疑`
    : lastPlayerId
    ? `牌局结束，${lastPlayer.name} 是最后一名`
    : newlyFinished.length > 0
      ? `${finishedNames} 已出完手牌，牌局继续`
      : actionMessage;

  return {
    ...state,
    players,
    direction,
    currentPlayer: lastPlayerId ? players.findIndex((item) => item.id === lastPlayerId) : nextIndex,
    discardPile: [...state.discardPile, card],
    currentColor: needsColor ? chosenColor! : card.color === 'wild' ? state.currentColor : card.color,
    pendingDraw,
    pendingKind,
    drawnCardId: null,
    unoArmed: false,
    unoDeclaredPlayerIds,
    reportablePlayerId,
    wildChallenge,
    finishedPlayerIds,
    winnerId,
    lastPlayerId,
    turn: state.turn + 1,
    message,
  };
}

export function drawCardsForTurn(state: GameState): GameState {
  state = normalizeGameState(state);
  if (state.phase === 'claiming' || state.lastPlayerId) return state;
  const count = state.pendingDraw || 1;
  const player = state.players[state.currentPlayer];
  const result = drawFromPile(state, count);
  const players = state.players.map((item, index) => index === state.currentPlayer
    ? { ...item, hand: [...item.hand, ...result.cards] }
    : item);
  const drawnCard = result.cards[result.cards.length - 1];
  const unoDeclaredPlayerIds = state.unoDeclaredPlayerIds.filter((playerId) => players.some((item) => item.id === playerId && item.hand.length === 1));
  const base: GameState = {
    ...state,
    players,
    drawPile: result.drawPile,
    discardPile: result.discardPile,
    pendingDraw: 0,
    pendingKind: null,
    unoArmed: false,
    unoDeclaredPlayerIds,
    reportablePlayerId: null,
    wildChallenge: null,
    message: `${player.name} 摸了 ${count} 张牌`,
  };

  if (count === 1 && state.rules.drawToPlay && drawnCard) {
    const candidate = { ...base, drawnCardId: null };
    if (canPlayCard(candidate, drawnCard)) {
      return { ...base, drawnCardId: drawnCard.id, message: `${player.name} 可以打出刚摸到的牌` };
    }
  }

  return {
    ...base,
    currentPlayer: nextPlayerIndex(base),
    drawnCardId: null,
    turn: state.turn + 1,
  };
}

export function passDrawnCard(state: GameState): GameState {
  state = normalizeGameState(state);
  if (state.phase === 'claiming' || !state.drawnCardId) return state;
  return {
    ...state,
    currentPlayer: nextPlayerIndex(state),
    drawnCardId: null,
    unoArmed: false,
    wildChallenge: null,
    turn: state.turn + 1,
    message: `${state.players[state.currentPlayer].name} 保留了摸到的牌`,
  };
}

export function reportUno(state: GameState, reporterPlayerId: string): GameState {
  state = normalizeGameState(state);
  if (!state.reportablePlayerId) return state;
  const offenderIndex = state.players.findIndex((player) => player.id === state.reportablePlayerId);
  if (offenderIndex < 0) return { ...state, reportablePlayerId: null };
  const reporter = state.players.find((player) => player.id === reporterPlayerId);
  if (!reporter || reporter.id === state.reportablePlayerId) return state;
  const result = drawFromPile(state, 2);
  const offender = state.players[offenderIndex];
  const players = state.players.map((player, index) => index === offenderIndex
    ? { ...player, hand: [...player.hand, ...result.cards] }
    : player);
  const unoDeclaredPlayerIds = state.unoDeclaredPlayerIds.filter((playerId) => players.some((player) => player.id === playerId && player.hand.length === 1));
  return {
    ...state,
    players,
    drawPile: result.drawPile,
    discardPile: result.discardPile,
    unoDeclaredPlayerIds,
    reportablePlayerId: null,
    message: `${reporter.name} 举报 ${offender.name} 没喊 UNO，${offender.name} 被罚摸 2 张！`,
  };
}

export function challengeWild(state: GameState, challengerPlayerId: string): GameState {
  state = normalizeGameState(state);
  const challenge = state.wildChallenge;
  if (!challenge || challengerPlayerId === challenge.playerId) return state;
  const challengerIndex = state.players.findIndex((player) => player.id === challengerPlayerId);
  const challengedIndex = state.players.findIndex((player) => player.id === challenge.playerId);
  if (challengerIndex < 0 || challengedIndex < 0 || state.finishedPlayerIds.includes(challengerPlayerId)) return state;

  const punishedIndex = challenge.hadMatchingColor ? challengedIndex : challengerIndex;
  const result = drawFromPile(state, 2);
  const players = state.players.map((player, index) => index === punishedIndex
    ? { ...player, hand: [...player.hand, ...result.cards] }
    : player);
  const challenger = players[challengerIndex];
  const challenged = players[challengedIndex];
  const punished = players[punishedIndex];
  const unoDeclaredPlayerIds = state.unoDeclaredPlayerIds.filter((playerId) => players.some((player) => player.id === playerId && player.hand.length === 1));

  return {
    ...state,
    players,
    drawPile: result.drawPile,
    discardPile: result.discardPile,
    unoDeclaredPlayerIds,
    wildChallenge: null,
    message: challenge.hadMatchingColor
      ? `${challenger.name} 质疑成功！${challenged.name} 当时有${COLOR_LABELS[challenge.chosenColor]}牌，被罚摸 2 张`
      : `${challenger.name} 质疑失败！${challenged.name} 当时没有${COLOR_LABELS[challenge.chosenColor]}牌，${punished.name} 被罚摸 2 张`,
  };
}

export function declineWildChallenge(state: GameState, playerId: string): GameState {
  state = normalizeGameState(state);
  const challenge = state.wildChallenge;
  if (!challenge || challenge.playerId === playerId || !state.players.some((player) => player.id === playerId)) return state;
  const challenged = state.players.find((player) => player.id === challenge.playerId)!;
  return {
    ...state,
    wildChallenge: null,
    message: `无人质疑 ${challenged.name} 的改色，牌局继续`,
  };
}

export function clearReport(state: GameState): GameState {
  return { ...state, reportablePlayerId: null };
}
