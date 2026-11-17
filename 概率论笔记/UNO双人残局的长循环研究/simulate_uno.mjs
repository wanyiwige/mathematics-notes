/**
 * UNO 多人残局 Monte Carlo、心理策略与显式非终止路径实验。
 *
 * 运行环境：Node.js 22.13+（本次核验使用 v24.14.0）
 * 运行命令：
 *   node --experimental-strip-types simulate_uno.mjs --output simulation-results.json
 *
 * 规则实现来自同目录 uno_engine.ts；该文件是用户所给
 * UNO-Source-Code.zip 中 lib/uno.ts 的逐字节快照。
 */

import assert from 'node:assert/strict';
import { writeFileSync } from 'node:fs';
import {
  canPlayCard,
  claimFirstTurn,
  createGame,
  declineWildChallenge,
  drawCardsForTurn,
  passDrawnCard,
  playCard,
} from './uno_engine.ts';

const DEFAULT_LIMIT = 20_000;

const STRATEGIES = {
  uniform: {
    name: 'uniform',
    description: '从合法牌中等概率选择；摸到可出的牌时立即打出。',
  },
  psychological: {
    name: 'psychological',
    description: '前期保留万能牌和罚牌，手牌剩 1–2 张时优先使用；受罚时用叠加牌保命；罚牌目标是手牌最少者时提高出牌权重。',
    earlyWildWeight: 0.15,
    earlyWildPenaltyWeight: 0.35,
    lateWildWeight: 8,
    earlyPenaltyWeight: 0.35,
    latePenaltyWeight: 3,
    stackDefenseWeight: 25,
    lowestHandTargetWeight: 6,
    otherTargetWeight: 0.6,
    drawnEarlyWildPlayProbability: 0.15,
    drawnEarlyPenaltyPlayProbability: 0.35,
    drawnEarlyWildPenaltyPlayProbability: 0.08,
  },
};

const PENALTY_VALUES = new Set(['draw1', 'draw3', 'wild2', 'wild5']);

function emptyDiagnostics() {
  return {
    earlyWildChoiceOpportunities: 0,
    earlyWildSelections: 0,
    lateWildChoiceOpportunities: 0,
    lateWildSelections: 0,
    drawnPlayableEarlyWilds: 0,
    drawnPlayableEarlyWildsKept: 0,
    drawnPlayableEarlyPenalties: 0,
    drawnPlayableEarlyPenaltiesKept: 0,
    penaltyPlaysWithTarget: 0,
    penaltyPlaysTargetingLeastHand: 0,
    multiplayerPenaltyPlaysWithTarget: 0,
    multiplayerPenaltyPlaysTargetingLeastHand: 0,
    stackDefensePlays: 0,
  };
}

function addDiagnostics(target, source) {
  for (const key of Object.keys(target)) target[key] += source[key];
}

function ratio(numerator, denominator) {
  return denominator === 0 ? null : +(numerator / denominator).toFixed(4);
}

function seededRandom(seed) {
  let value = seed >>> 0;
  return () => {
    value = (1664525 * value + 1013904223) >>> 0;
    return value / 0x1_0000_0000;
  };
}

function withSeed(seed, operation) {
  const originalRandom = Math.random;
  Math.random = seededRandom(seed);
  try {
    return operation();
  } finally {
    Math.random = originalRandom;
  }
}

function chooseColor(hand, excludedCardId) {
  const counts = { red: 0, yellow: 0, green: 0, blue: 0 };
  for (const card of hand) {
    if (card.id !== excludedCardId && card.color !== 'wild') counts[card.color] += 1;
  }
  return Object.entries(counts).sort((left, right) => right[1] - left[1])[0][0];
}

function activePlayerIndexes(state) {
  return state.players
    .map((player, index) => state.finishedPlayerIds.includes(player.id) ? -1 : index)
    .filter((index) => index >= 0);
}

function nextActivePlayer(state, direction = state.direction) {
  const activeIndexes = activePlayerIndexes(state);
  if (activeIndexes.length <= 1) return null;
  let index = state.currentPlayer;
  do {
    index = (index + direction + state.players.length) % state.players.length;
  } while (state.finishedPlayerIds.includes(state.players[index].id));
  return state.players[index];
}

function penaltyTarget(state, card) {
  if (PENALTY_VALUES.has(card.value)) return nextActivePlayer(state);
  if (card.value === 'reflect' && state.pendingDraw > 0) {
    return nextActivePlayer(state, state.direction === 1 ? -1 : 1);
  }
  return null;
}

function targetHasLeastHand(state, target) {
  if (!target) return false;
  const opponents = state.players.filter(
    (player) => player.id !== state.players[state.currentPlayer].id
      && !state.finishedPlayerIds.includes(player.id),
  );
  if (opponents.length === 0) return false;
  const least = Math.min(...opponents.map((player) => player.hand.length));
  return target.hand.length === least;
}

function cardWeight(state, card, strategy) {
  if (strategy.name === 'uniform') return 1;

  const handSize = state.players[state.currentPlayer].hand.length;
  const lateGame = handSize <= 2;
  const wild = card.color === 'wild';
  const penalty = PENALTY_VALUES.has(card.value);
  const stackDefense = state.pendingDraw > 0 && (penalty || card.value === 'reflect');
  let weight = 1;

  if (wild) {
    weight *= lateGame ? strategy.lateWildWeight : strategy.earlyWildWeight;
  }
  if (stackDefense) {
    weight *= strategy.stackDefenseWeight;
  } else if (penalty) {
    weight *= lateGame ? strategy.latePenaltyWeight : strategy.earlyPenaltyWeight;
    if (wild && !lateGame) weight *= strategy.earlyWildPenaltyWeight;
  }

  const target = penaltyTarget(state, card);
  if (target) {
    weight *= targetHasLeastHand(state, target)
      ? strategy.lowestHandTargetWeight
      : strategy.otherTargetWeight;
  }
  return weight;
}

function weightedChoice(items, weightOf) {
  const weights = items.map((item) => Math.max(0, weightOf(item)));
  const total = weights.reduce((sum, weight) => sum + weight, 0);
  assert.ok(Number.isFinite(total) && total > 0, '出牌权重之和必须为正有限数');
  let cursor = Math.random() * total;
  for (let index = 0; index < items.length; index += 1) {
    cursor -= weights[index];
    if (cursor < 0) return items[index];
  }
  return items.at(-1);
}

function verifyStrategyWeights() {
  const ordinary = { id: 'red-7-test', color: 'red', value: '7' };
  const wild = { id: 'wild-wild-test', color: 'wild', value: 'wild' };
  const wildPenalty = { id: 'wild-wild5-test', color: 'wild', value: 'wild5' };
  const colorPenalty = { id: 'red-draw3-test', color: 'red', value: 'draw3' };
  const filler = Array.from({ length: 3 }, (_, index) => ({
    id: `blue-${index}-test`, color: 'blue', value: `${index}`,
  }));
  const makeState = (hand, direction = 1, pendingDraw = 0) => ({
    players: [
      { id: 'A', hand },
      { id: 'B', hand: [ordinary] },
      { id: 'C', hand: [ordinary, wild, wildPenalty, colorPenalty, ...filler] },
    ],
    currentPlayer: 0,
    direction,
    finishedPlayerIds: [],
    pendingDraw,
  });
  const strategy = STRATEGIES.psychological;
  const early = makeState([ordinary, wild, wildPenalty, colorPenalty, ...filler]);
  const late = makeState([ordinary, wild]);
  const stack = makeState([ordinary, wild, wildPenalty, colorPenalty, ...filler], 1, 5);
  const earlyOrdinary = cardWeight(early, ordinary, strategy);
  const earlyWild = cardWeight(early, wild, strategy);
  const lateOrdinary = cardWeight(late, ordinary, strategy);
  const lateWild = cardWeight(late, wild, strategy);
  const earlyPenaltyToLeast = cardWeight(early, colorPenalty, strategy);
  const earlyPenaltyToOther = cardWeight(
    makeState([ordinary, wild, wildPenalty, colorPenalty, ...filler], -1),
    colorPenalty,
    strategy,
  );
  const earlyWildPenalty = cardWeight(early, wildPenalty, strategy);
  const defensiveWildPenalty = cardWeight(stack, wildPenalty, strategy);

  assert.ok(earlyWild < earlyOrdinary, '前期万能牌权重必须低于普通牌');
  assert.ok(lateWild > lateOrdinary, '剩余 1–2 张时万能牌权重必须高于普通牌');
  assert.ok(earlyPenaltyToLeast > earlyPenaltyToOther, '罚牌必须更偏向手牌最少的目标');
  assert.ok(defensiveWildPenalty > earlyWildPenalty, '遭遇累计罚牌时，保命叠加权重必须提高');

  return {
    passed: true,
    earlyOrdinary,
    earlyWild,
    lateOrdinary,
    lateWild,
    earlyPenaltyToLeast,
    earlyPenaltyToOther,
    earlyWildPenalty,
    defensiveWildPenalty,
  };
}

function recordChoiceDiagnostics(state, playableCards, selected, diagnostics) {
  const handSize = state.players[state.currentPlayer].hand.length;
  const hasWild = playableCards.some((card) => card.color === 'wild');
  const hasNonWild = playableCards.some((card) => card.color !== 'wild');
  if (hasWild && hasNonWild) {
    if (handSize <= 2) {
      diagnostics.lateWildChoiceOpportunities += 1;
      if (selected.color === 'wild') diagnostics.lateWildSelections += 1;
    } else {
      diagnostics.earlyWildChoiceOpportunities += 1;
      if (selected.color === 'wild') diagnostics.earlyWildSelections += 1;
    }
  }
}

function recordPlayDiagnostics(state, card, diagnostics) {
  const target = penaltyTarget(state, card);
  if (target) {
    diagnostics.penaltyPlaysWithTarget += 1;
    const targetsLeast = targetHasLeastHand(state, target);
    if (targetsLeast) {
      diagnostics.penaltyPlaysTargetingLeastHand += 1;
    }
    if (activePlayerIndexes(state).length >= 3) {
      diagnostics.multiplayerPenaltyPlaysWithTarget += 1;
      if (targetsLeast) diagnostics.multiplayerPenaltyPlaysTargetingLeastHand += 1;
    }
  }
  if (state.pendingDraw > 0 && (PENALTY_VALUES.has(card.value) || card.value === 'reflect')) {
    diagnostics.stackDefensePlays += 1;
  }
}

function shouldPlayDrawnCard(state, card, strategy, diagnostics) {
  if (strategy.name === 'uniform') return true;
  const handSize = state.players[state.currentPlayer].hand.length;
  if (handSize <= 2) return true;

  const wild = card.color === 'wild';
  const penalty = PENALTY_VALUES.has(card.value);
  if (wild) {
    diagnostics.drawnPlayableEarlyWilds += 1;
    if (penalty) diagnostics.drawnPlayableEarlyPenalties += 1;
    const probability = penalty
      ? strategy.drawnEarlyWildPenaltyPlayProbability
      : strategy.drawnEarlyWildPlayProbability;
    const play = Math.random() < probability;
    if (!play) {
      diagnostics.drawnPlayableEarlyWildsKept += 1;
      if (penalty) diagnostics.drawnPlayableEarlyPenaltiesKept += 1;
    }
    return play;
  }
  if (penalty) {
    diagnostics.drawnPlayableEarlyPenalties += 1;
    const play = Math.random() < strategy.drawnEarlyPenaltyPlayProbability;
    if (!play) diagnostics.drawnPlayableEarlyPenaltiesKept += 1;
    return play;
  }
  return true;
}

function playChosenCard(state, card, diagnostics) {
  recordPlayDiagnostics(state, card, diagnostics);
  const player = state.players[state.currentPlayer];
  const activePlayers = state.players.filter(
    (candidate) => !state.finishedPlayerIds.includes(candidate.id),
  );
  const chosenColor = ['wild', 'wild2', 'wild5', 'reflect'].includes(card.value)
    ? chooseColor(player.hand, card.id)
    : undefined;
  const otherPlayer = activePlayers.find((candidate) => candidate.id !== player.id);
  const swapPair = card.value === 'swapTwo' && otherPlayer
    ? [player.id, otherPlayer.id]
    : undefined;
  return playCard(state, card.id, chosenColor, swapPair);
}

/**
 * 自动策略：
 * - 万能牌选择剩余手牌中数量最多的颜色；平局按红、黄、绿、蓝排序。
 * - 指定交换牌选择当前玩家与第一名其他活跃玩家。
 * - 不发起质疑，也不举报 UNO（它们在本策略中不改变出牌合法性）。
 * - uniform 摸到可出的牌时总是打出；psychological 会在前期保留刚摸到的万能牌/罚牌。
 * - 若手中原本有可出牌，仍以 voluntaryDrawProbability 主动摸牌。
 */
function simulateOneGame({
  playerCount,
  rules,
  strategyName,
  voluntaryDrawProbability,
  actionLimit = DEFAULT_LIMIT,
}) {
  const strategy = STRATEGIES[strategyName];
  if (!strategy) throw new Error(`未知策略：${strategyName}`);
  const diagnostics = emptyDiagnostics();
  let state = createGame(
    Array.from({ length: playerCount }, (_, index) => `P${index + 1}`),
    rules,
  );
  state = claimFirstTurn(state, state.players[0].id);

  let actions = 0;
  let twoPlayerPhaseStartedAt = playerCount === 2 ? 0 : null;

  while (!state.lastPlayerId && actions < actionLimit) {
    if (state.wildChallenge) {
      const responder = state.players.find(
        (player) => player.id !== state.wildChallenge.playerId
          && !state.finishedPlayerIds.includes(player.id),
      );
      if (responder) state = declineWildChallenge(state, responder.id);
    }

    const currentPlayer = state.players[state.currentPlayer];
    if (state.drawnCardId) {
      const drawnCard = currentPlayer.hand.find((card) => card.id === state.drawnCardId);
      const playsDrawnCard = drawnCard
        && canPlayCard(state, drawnCard)
        && shouldPlayDrawnCard(state, drawnCard, strategy, diagnostics);
      state = playsDrawnCard
        ? playChosenCard(state, drawnCard, diagnostics)
        : passDrawnCard(state);
    } else {
      const playableCards = currentPlayer.hand.filter((card) => canPlayCard(state, card));
      const voluntarilyDraws = playableCards.length > 0
        && Math.random() < voluntaryDrawProbability;
      if (playableCards.length > 0 && !voluntarilyDraws) {
        const selected = strategy.name === 'uniform'
          ? playableCards[Math.floor(Math.random() * playableCards.length)]
          : weightedChoice(playableCards, (card) => cardWeight(state, card, strategy));
        recordChoiceDiagnostics(state, playableCards, selected, diagnostics);
        state = playChosenCard(state, selected, diagnostics);
      } else {
        state = drawCardsForTurn(state);
      }
    }

    actions += 1;
    const activePlayerCount = state.players.length - state.finishedPlayerIds.length;
    if (activePlayerCount === 2 && twoPlayerPhaseStartedAt === null) {
      twoPlayerPhaseStartedAt = actions;
    }
  }

  return {
    ended: Boolean(state.lastPlayerId),
    actions,
    twoPlayerPhaseActions: twoPlayerPhaseStartedAt === null
      ? null
      : actions - twoPlayerPhaseStartedAt,
    diagnostics,
  };
}

function percentile(sortedValues, probability) {
  if (sortedValues.length === 0) return null;
  const index = Math.min(
    sortedValues.length - 1,
    Math.floor(probability * sortedValues.length),
  );
  return sortedValues[index];
}

function summarize(values) {
  if (values.length === 0) return null;
  const sorted = [...values].sort((left, right) => left - right);
  return {
    mean: +(sorted.reduce((sum, value) => sum + value, 0) / sorted.length).toFixed(2),
    median: percentile(sorted, 0.50),
    p95: percentile(sorted, 0.95),
    p99: percentile(sorted, 0.99),
    max: sorted.at(-1),
  };
}

function runExperiment(configuration) {
  return withSeed(configuration.seed, () => {
    const completedActions = [];
    const completedTwoPlayerActions = [];
    const diagnostics = emptyDiagnostics();
    let unresolved = 0;

    for (let game = 0; game < configuration.games; game += 1) {
      const result = simulateOneGame(configuration);
      addDiagnostics(diagnostics, result.diagnostics);
      if (!result.ended) {
        unresolved += 1;
        continue;
      }
      completedActions.push(result.actions);
      if (result.twoPlayerPhaseActions !== null) {
        completedTwoPlayerActions.push(result.twoPlayerPhaseActions);
      }
    }

    return {
      label: configuration.label,
      seed: `0x${configuration.seed.toString(16).toUpperCase()}`,
      games: configuration.games,
      actionLimit: configuration.actionLimit ?? DEFAULT_LIMIT,
      strategy: configuration.strategyName,
      unresolved,
      allCompleted: summarize(completedActions),
      completedTwoPlayerPhase: summarize(completedTwoPlayerActions),
      behavioralDiagnostics: {
        ...diagnostics,
        earlyWildSelectionRateWhenAlternativeExists: ratio(
          diagnostics.earlyWildSelections,
          diagnostics.earlyWildChoiceOpportunities,
        ),
        lateWildSelectionRateWhenAlternativeExists: ratio(
          diagnostics.lateWildSelections,
          diagnostics.lateWildChoiceOpportunities,
        ),
        drawnPlayableEarlyWildKeepRate: ratio(
          diagnostics.drawnPlayableEarlyWildsKept,
          diagnostics.drawnPlayableEarlyWilds,
        ),
        drawnPlayableEarlyPenaltyKeepRate: ratio(
          diagnostics.drawnPlayableEarlyPenaltiesKept,
          diagnostics.drawnPlayableEarlyPenalties,
        ),
        penaltyTargetLeastHandRate: ratio(
          diagnostics.penaltyPlaysTargetingLeastHand,
          diagnostics.penaltyPlaysWithTarget,
        ),
        multiplayerPenaltyTargetLeastHandRate: ratio(
          diagnostics.multiplayerPenaltyPlaysTargetingLeastHand,
          diagnostics.multiplayerPenaltyPlaysWithTarget,
        ),
      },
    };
  });
}

function strategicSignature(state) {
  return JSON.stringify({
    players: state.players.map((player) => ({
      id: player.id,
      hand: player.hand.map((card) => card.id),
    })),
    currentPlayer: state.currentPlayer,
    direction: state.direction,
    drawPile: state.drawPile.map((card) => card.id),
    discardPile: state.discardPile.map((card) => card.id),
    currentColor: state.currentColor,
    pendingDraw: state.pendingDraw,
    pendingKind: state.pendingKind,
    drawnCardId: state.drawnCardId,
    finishedPlayerIds: state.finishedPlayerIds,
    lastPlayerId: state.lastPlayerId,
  });
}

function constructAlwaysDrawCycle() {
  return withSeed(0xDEADBEEF, () => {
    let state = createGame(['A', 'B'], { stackDraw: true, drawToPlay: true });
    state = claimFirstTurn(state, state.players[0].id);

    let constructionActions = 0;
    while ((state.drawPile.length > 0 || state.drawnCardId) && constructionActions < 500) {
      state = state.drawnCardId ? passDrawnCard(state) : drawCardsForTurn(state);
      constructionActions += 1;
    }

    assert.equal(state.drawPile.length, 0);
    assert.equal(state.discardPile.length, 1);
    assert.equal(state.players.reduce((sum, player) => sum + player.hand.length, 0), 121);
    assert.equal(state.lastPlayerId, null);

    const before = strategicSignature(state);
    const afterOneEmptyDraw = drawCardsForTurn(state);
    const afterTwoEmptyDraws = drawCardsForTurn(afterOneEmptyDraw);
    const after = strategicSignature(afterTwoEmptyDraws);
    assert.equal(after, before);

    return {
      constructionActions,
      handSizes: state.players.map((player) => player.hand.length),
      drawPileSize: state.drawPile.length,
      discardPileSize: state.discardPile.length,
      completeGameStateRepeats: false,
      strategicProjectionHasPeriodTwo: true,
      explanation: 'turn 与 message 会变化；剔除展示字段后的战略状态每两个空摸动作重复。',
    };
  });
}

const configurations = [
  {
    label: '双人：积极出牌，叠加开，摸牌即出开',
    seed: 0xC0FFEE01,
    games: 10_000,
    playerCount: 2,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0,
  },
  {
    label: '双人：积极出牌，叠加关，摸牌即出关',
    seed: 0xC0FFEE02,
    games: 10_000,
    playerCount: 2,
    rules: { stackDraw: false, drawToPlay: false },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0,
  },
  {
    label: '双人：有牌可出时以 10% 概率主动摸牌',
    seed: 0xC0FFEE03,
    games: 10_000,
    playerCount: 2,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0.10,
  },
  {
    label: '双人：有牌可出时以 25% 概率主动摸牌',
    seed: 0xC0FFEE04,
    games: 3_000,
    playerCount: 2,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0.25,
  },
  {
    label: '四人开局：积极出牌',
    seed: 0xC0FFEE05,
    games: 10_000,
    playerCount: 4,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0,
  },
  {
    label: '四人开局：有牌可出时以 10% 概率主动摸牌',
    seed: 0xC0FFEE06,
    games: 10_000,
    playerCount: 4,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0.10,
  },
  {
    label: '三人开局：等概率积极出牌（基线）',
    seed: 0xC0FFEE07,
    games: 10_000,
    playerCount: 3,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'uniform',
    voluntaryDrawProbability: 0,
  },
  {
    label: '三人开局：保牌、叠加保命与攻击领先者',
    seed: 0xC0FFEE08,
    games: 10_000,
    playerCount: 3,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'psychological',
    voluntaryDrawProbability: 0,
  },
  {
    label: '四人开局：保牌、叠加保命与攻击领先者',
    seed: 0xC0FFEE09,
    games: 10_000,
    playerCount: 4,
    rules: { stackDraw: true, drawToPlay: true },
    strategyName: 'psychological',
    voluntaryDrawProbability: 0,
  },
];

const output = {
  metadata: {
    generatedAt: '2026-09-19T00:00:00+08:00',
    nodeRequirement: '>=22.13.0',
    actionDefinition: '一次 playCard、drawCardsForTurn 或 passDrawnCard 调用计一个动作；draw+play 计两个动作。',
    interpretation: '统计量只属于本文明示的自动策略，不代表真人策略或标准 UNO 的精确分布。心理策略使用相对权重；罚牌目标受行动顺序约束，不能任意指定。',
    strategyDefinitions: STRATEGIES,
    strategyWeightAssertions: verifyStrategyWeights(),
  },
  experiments: configurations.map(runExperiment),
  explicitNonTerminationConstruction: constructAlwaysDrawCycle(),
};

const serialized = `${JSON.stringify(output, null, 2)}\n`;
const outputFlag = process.argv.indexOf('--output');
if (outputFlag >= 0) {
  const outputPath = process.argv[outputFlag + 1];
  if (!outputPath) throw new Error('--output 后必须提供文件路径');
  writeFileSync(outputPath, serialized, 'utf8');
}
process.stdout.write(serialized);
