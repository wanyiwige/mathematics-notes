/**
 * UNO 双人残局 Monte Carlo 与显式非终止路径实验。
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

function playChosenCard(state, card) {
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
 * - 摸到可立即打出的牌时总是打出；draw+play 计为两个动作。
 * - 若手中原本有可出牌，仍以 voluntaryDrawProbability 主动摸牌。
 */
function simulateOneGame({
  playerCount,
  rules,
  voluntaryDrawProbability,
  actionLimit = DEFAULT_LIMIT,
}) {
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
      state = drawnCard && canPlayCard(state, drawnCard)
        ? playChosenCard(state, drawnCard)
        : passDrawnCard(state);
    } else {
      const playableCards = currentPlayer.hand.filter((card) => canPlayCard(state, card));
      const voluntarilyDraws = playableCards.length > 0
        && Math.random() < voluntaryDrawProbability;
      if (playableCards.length > 0 && !voluntarilyDraws) {
        const selected = playableCards[Math.floor(Math.random() * playableCards.length)];
        state = playChosenCard(state, selected);
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
    let unresolved = 0;

    for (let game = 0; game < configuration.games; game += 1) {
      const result = simulateOneGame(configuration);
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
      unresolved,
      allCompleted: summarize(completedActions),
      completedTwoPlayerPhase: summarize(completedTwoPlayerActions),
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
    voluntaryDrawProbability: 0,
  },
  {
    label: '双人：积极出牌，叠加关，摸牌即出关',
    seed: 0xC0FFEE02,
    games: 10_000,
    playerCount: 2,
    rules: { stackDraw: false, drawToPlay: false },
    voluntaryDrawProbability: 0,
  },
  {
    label: '双人：有牌可出时以 10% 概率主动摸牌',
    seed: 0xC0FFEE03,
    games: 10_000,
    playerCount: 2,
    rules: { stackDraw: true, drawToPlay: true },
    voluntaryDrawProbability: 0.10,
  },
  {
    label: '双人：有牌可出时以 25% 概率主动摸牌',
    seed: 0xC0FFEE04,
    games: 3_000,
    playerCount: 2,
    rules: { stackDraw: true, drawToPlay: true },
    voluntaryDrawProbability: 0.25,
  },
  {
    label: '四人开局：积极出牌',
    seed: 0xC0FFEE05,
    games: 10_000,
    playerCount: 4,
    rules: { stackDraw: true, drawToPlay: true },
    voluntaryDrawProbability: 0,
  },
  {
    label: '四人开局：有牌可出时以 10% 概率主动摸牌',
    seed: 0xC0FFEE06,
    games: 10_000,
    playerCount: 4,
    rules: { stackDraw: true, drawToPlay: true },
    voluntaryDrawProbability: 0.10,
  },
];

const output = {
  metadata: {
    generatedAt: '2026-09-14T00:00:00+08:00',
    nodeRequirement: '>=22.13.0',
    actionDefinition: '一次 playCard、drawCardsForTurn 或 passDrawnCard 调用计一个动作；draw+play 计两个动作。',
    interpretation: '统计量只属于本文明示的自动策略，不代表真人策略或标准 UNO 的精确分布。',
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
