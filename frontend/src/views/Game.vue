<template>
  <div class="game-container">
    <AnimeBackground />
    
    <!-- 浮动装饰粒子 -->
    <div class="game-particles">
      <div class="particle" v-for="i in 30" :key="i" :style="{ '--i': i }"></div>
    </div>
    
    <!-- 顶部装饰 -->
    <div class="top-decoration">
      <div class="deco-star" v-for="i in 8" :key="i" :style="{ '--i': i }">⭐</div>
    </div>

    <header class="game-header">
      <button class="back-btn" @click="goBack">
        <span class="back-icon">←</span>
        <span class="back-text">返回</span>
      </button>
      <div class="header-title-wrap">
        <h1 class="game-title">{{ gameName }}</h1>
        <div class="title-glow"></div>
      </div>
      <div class="header-badge">Lv.{{ level }}</div>
    </header>

    <main class="game-content">
      <!-- 分数面板 -->
      <div class="score-section">
        <div class="score-main">
          <div class="score-card current">
            <div class="card-glow"></div>
            <div class="score-label-wrap">
              <span class="score-label">当前得分</span>
              <span class="score-trend" :class="scoreTrend">{{ scoreTrend === 'up' ? '📈' : scoreTrend === 'down' ? '📉' : '➡' }}</span>
            </div>
            <div class="score-display">
              <span class="score-number">{{ score }}</span>
              <span class="score-unit">分</span>
            </div>
            <div class="score-bar">
              <div class="bar-fill" :style="{ width: rewardProgress + '%' }"></div>
            </div>
            <div class="score-tip">距离下一个奖励 {{ 500 - score % 500 }} 分</div>
          </div>
          
          <div class="score-card best">
            <div class="card-glow"></div>
            <span class="score-label">最高记录</span>
            <div class="score-display">
              <span class="score-number">{{ bestScore }}</span>
              <span class="score-unit">分</span>
            </div>
            <div class="best-badge">🏆</div>
          </div>
        </div>
        
        <!-- 连击提示 -->
        <div class="combo-display" v-if="comboCount > 1">
          <span class="combo-text">🔥 {{ comboCount }} 连击!</span>
          <span class="combo-multi">x{{ comboMultiplier }}</span>
        </div>
      </div>

      <!-- 控制按钮 -->
      <div class="controls-section">
        <button class="control-btn restart" @click="restartGame">
          <span class="btn-icon">🔄</span>
          <span class="btn-text">重新开始</span>
          <div class="btn-glow"></div>
        </button>
        <button class="control-btn undo" @click="undoMove" :disabled="!canUndo">
          <span class="btn-icon">↩️</span>
          <span class="btn-text">撤销</span>
          <div class="btn-glow"></div>
        </button>
        <button class="control-btn hint" @click="showHint">
          <span class="btn-icon">💡</span>
          <span class="btn-text">提示</span>
          <div class="btn-glow"></div>
        </button>
      </div>

      <!-- 游戏区域 -->
      <div class="game-area-wrapper">
        <!-- 装饰边框 -->
        <div class="game-frame">
          <div class="frame-corner tl"></div>
          <div class="frame-corner tr"></div>
          <div class="frame-corner bl"></div>
          <div class="frame-corner br"></div>
          <div class="frame-border-top"></div>
          <div class="frame-border-bottom"></div>
          <div class="frame-border-left"></div>
          <div class="frame-border-right"></div>
        </div>
        
        <div class="game-area">
          <!-- 动漫角色 -->
          <div class="anime-sidekick">
            <div class="sidekick-face" :class="sidekickState">{{ sidekickEmoji }}</div>
            <div class="sidekick-bubble" v-if="showSidekickBubble">{{ sidekickMessage }}</div>
          </div>
          
          <Game2048 
            ref="gameRef"
            @score-update="handleScoreUpdate"
            @game-over="handleGameOver"
            @game-win="handleGameWin"
            @show-reward="handleShowReward"
            @combo="handleCombo"
          />
          
          <!-- 游戏状态提示 -->
          <div class="game-status">
            <span class="status-badge" :class="gameStatus">{{ gameStatusText }}</span>
          </div>
        </div>
      </div>

      <!-- 操作提示 -->
      <div class="action-hints">
        <div class="hint-item">
          <span class="hint-key">⬆️⬇️⬅️➡️</span>
          <span class="hint-desc">方向键移动</span>
        </div>
        <div class="hint-item">
          <span class="hint-key">R</span>
          <span class="hint-desc">重新开始</span>
        </div>
        <div class="hint-item">
          <span class="hint-key">Z</span>
          <span class="hint-desc">撤销</span>
        </div>
      </div>

      <!-- 游戏规则 -->
      <div class="rules-section">
        <div class="rules-header">
          <span class="rules-icon">📜</span>
          <span class="rules-title">游戏规则</span>
        </div>
        <div class="rules-content">
          <div class="rule-item">
            <span class="rule-icon">🎮</span>
            <span class="rule-text">使用方向键或点击滑动来移动方块</span>
          </div>
          <div class="rule-item">
            <span class="rule-icon">🔢</span>
            <span class="rule-text">相同数字的方块相遇时会合并</span>
          </div>
          <div class="rule-item">
            <span class="rule-icon">🎯</span>
            <span class="rule-text">目标：合成出2048方块！</span>
          </div>
          <div class="rule-item">
            <span class="rule-icon">🎁</span>
            <span class="rule-text">每获得500分有惊喜奖励哦~</span>
          </div>
        </div>
      </div>

      <!-- 提交分数弹窗 -->
      <div v-if="showSubmit" class="submit-modal">
        <div class="modal-backdrop" @click="closeModal"></div>
        <div class="modal-content">
          <div class="modal-header">
            <div class="modal-icon">{{ gameWon ? '🏆' : '💔' }}</div>
            <h3>{{ gameWon ? '恭喜通关!' : '游戏结束!' }}</h3>
          </div>
          <div class="modal-body">
            <div class="final-score">
              <span class="score-label">最终得分</span>
              <span class="score-value">{{ score }}</span>
            </div>
            <div class="score-comparison" v-if="score >= bestScore && score > 0">
              <span class="new-record">🎉 新纪录!</span>
            </div>
            <input 
              v-model="playerName" 
              type="text" 
              placeholder="输入您的昵称" 
              maxlength="10"
              class="name-input"
              @keyup.enter="submitScore"
            />
          </div>
          <div class="modal-footer">
            <button class="submit-btn" @click="submitScore">
              <span class="btn-icon">📤</span>
              <span class="btn-text">提交分数</span>
            </button>
            <button class="cancel-btn" @click="closeModal">
              <span class="btn-icon">✕</span>
              <span class="btn-text">关闭</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- 提示弹窗 -->
      <div v-if="showHintModal" class="hint-modal">
        <div class="modal-backdrop" @click="closeHint"></div>
        <div class="modal-content hint-content">
          <div class="modal-header">
            <span class="modal-icon">💡</span>
            <h3>游戏提示</h3>
          </div>
          <div class="modal-body">
            <ul class="hint-list">
              <li>尽量保持最大数字在角落</li>
              <li>保持数字按大小顺序排列</li>
              <li>不要频繁上下移动</li>
              <li>小数字合并可以获得更高分数</li>
            </ul>
          </div>
          <div class="modal-footer">
            <button class="submit-btn" @click="closeHint">
              <span class="btn-text">知道了</span>
            </button>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 奖励效果 -->
    <RewardEffect 
      :show="showReward" 
      :points="rewardPoints"
      :current-score="score"
      @complete="hideReward"
    />
    
    <!-- 底部装饰 -->
    <div class="bottom-decoration">
      <span v-for="i in 15" :key="i" class="bottom-star" :style="{ '--i': i }">✨</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/api.js'
import Game2048 from '../components/games/2048/Game2048.vue'
import RewardEffect from '../components/RewardEffect.vue'
import AnimeBackground from '../components/AnimeBackground.vue'

const route = useRoute()
const router = useRouter()
const gameRef = ref(null)
const gameName = ref('2048')
const score = ref(0)
const bestScore = ref(0)
const showSubmit = ref(false)
const showHintModal = ref(false)
const playerName = ref('')
const showReward = ref(false)
const rewardPoints = ref(500)
const gameWon = ref(false)
const comboCount = ref(0)
const comboMultiplier = ref(1)
const canUndo = ref(false)
const gameStatus = ref('playing')

const level = computed(() => Math.floor(score.value / 1000) + 1)

const rewardProgress = computed(() => ((score.value % 500) / 500) * 100)

const scoreTrend = ref('up')
const prevScore = ref(0)

const sidekickEmoji = ref('😊')
const showSidekickBubble = ref(false)
const sidekickMessage = ref('')
const sidekickState = ref('happy')

const sidekickStates = {
  happy: ['😊', '😄', '😆', '🥰', '🤩', '😎'],
  excited: ['😍', '🤯', '🥳', '😱', '🤗', '🎉'],
  sad: ['😢', '😔', '😞', '😿'],
  thinking: ['🤔', '🧐', '😌'],
  surprised: ['😮', '😲', '🙀']
}

const sidekickMessages = {
  happy: ['太棒了!', '厉害!', '完美!', 'Nice!', 'Amazing!', '漂亮!'],
  excited: ['哇!', '超酷!', '太厉害了!', '难以置信!', 'OMG!', '无敌!'],
  sad: ['加油!', '别放弃!', '再来一次!', '不要气馁!', '我相信你!'],
  thinking: ['想想策略...', '下一步怎么走?', '冷静思考', '仔细观察'],
  surprised: ['哇哦!', '太意外了!', '不可思议!', '天呐!']
}

const gameStatusText = computed(() => {
  const status = {
    playing: '游戏中',
    won: '已达成2048!',
    over: '游戏结束'
  }
  return status[gameStatus.value] || '游戏中'
})

const updateSidekick = (state) => {
  sidekickState.value = state
  const emojis = sidekickStates[state] || sidekickStates.happy
  const messages = sidekickMessages[state] || sidekickMessages.happy
  sidekickEmoji.value = emojis[Math.floor(Math.random() * emojis.length)]
  sidekickMessage.value = messages[Math.floor(Math.random() * messages.length)]
  showSidekickBubble.value = true
  setTimeout(() => {
    showSidekickBubble.value = false
  }, 2500)
}

onMounted(async () => {
  const savedBest = localStorage.getItem('2048_best_score')
  if (savedBest) {
    bestScore.value = parseInt(savedBest)
  }
  
  try {
    const res = await api.get(`/api/games/${route.params.id}`)
    gameName.value = res.data.name
  } catch (error) {
    console.error('Failed to load game info:', error)
  }
})

const goBack = () => {
  router.push('/')
}

const handleScoreUpdate = (newScore) => {
  const oldScore = score.value
  scoreTrend.value = newScore > prevScore.value ? 'up' : newScore < prevScore.value ? 'down' : 'same'
  prevScore.value = oldScore
  score.value = newScore
  if (newScore > bestScore.value) {
    bestScore.value = newScore
    localStorage.setItem('2048_best_score', newScore.toString())
    updateSidekick('excited')
  }
  
  canUndo.value = true
  
  if (newScore >= 2048 && gameStatus.value === 'playing') {
    gameStatus.value = 'won'
  }
}

const handleGameOver = () => {
  gameStatus.value = 'over'
  updateSidekick('sad')
  showSubmit.value = true
}

const handleGameWin = () => {
  gameStatus.value = 'won'
  gameWon.value = true
  updateSidekick('excited')
}

const handleShowReward = (data) => {
  rewardPoints.value = data.points
  showReward.value = true
  updateSidekick('excited')
}

const handleCombo = (count) => {
  comboCount.value = count
  comboMultiplier.value = Math.min(count, 5)
  
  if (count >= 3) {
    updateSidekick('excited')
  } else if (count === 2) {
    updateSidekick('happy')
  }
  
  setTimeout(() => {
    comboCount.value = 0
    comboMultiplier.value = 1
  }, 2000)
}

const hideReward = () => {
  showReward.value = false
}

const restartGame = () => {
  gameRef.value?.restart()
  score.value = 0
  showSubmit.value = false
  gameWon.value = false
  gameStatus.value = 'playing'
  comboCount.value = 0
  canUndo.value = false
  updateSidekick('happy')
}

const undoMove = () => {
  gameRef.value?.undo()
  canUndo.value = false
  updateSidekick('thinking')
}

const showHint = () => {
  showHintModal.value = true
}

const closeHint = () => {
  showHintModal.value = false
}

const closeModal = () => {
  showSubmit.value = false
}

const submitScore = async () => {
  const name = playerName.value.trim() || '匿名玩家'
  try {
    await api.post('/api/score', {
      game_id: parseInt(route.params.id),
      player_name: name,
      score: score.value
    })
    showSubmit.value = false
    playerName.value = ''
    alert('分数提交成功!')
  } catch (error) {
    console.error('Failed to submit score:', error)
    alert('提交失败，请重试')
  }
}

watch(comboCount, (newVal) => {
  if (newVal >= 5) {
    updateSidekick('surprised')
  }
})
</script>

<style scoped>
.game-container {
  min-height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  overflow-x: hidden;
  z-index: 1;
}

/* 浮动粒子 */
.game-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  width: 6px;
  height: 6px;
  background: radial-gradient(circle, #FFD700 0%, #FF6B9D 50%, transparent 100%);
  border-radius: 50%;
  left: calc(var(--i) * 3.3%);
  animation: game-particle-float 12s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.4s);
}

@keyframes game-particle-float {
  0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
  10% { opacity: 0.7; }
  50% { transform: translateY(-60vh) translateX(30px); opacity: 0.5; }
  90% { opacity: 0.7; }
  100% { transform: translateY(-120vh) translateX(-20px); }
}

/* 顶部装饰 */
.top-decoration {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 150px;
  pointer-events: none;
  z-index: 0;
}

.deco-star {
  position: absolute;
  font-size: 1.2rem;
  animation: star-twinkle 2s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.2s);
}

.deco-star:nth-child(1) { top: 5%; left: 5%; }
.deco-star:nth-child(2) { top: 10%; left: 20%; }
.deco-star:nth-child(3) { top: 3%; right: 15%; }
.deco-star:nth-child(4) { top: 12%; right: 5%; }
.deco-star:nth-child(5) { top: 8%; left: 50%; }
.deco-star:nth-child(6) { top: 15%; left: 30%; }
.deco-star:nth-child(7) { top: 6%; right: 35%; }
.deco-star:nth-child(8) { top: 18%; left: 70%; }

@keyframes star-twinkle {
  0%, 100% { opacity: 1; transform: scale(1) rotate(0deg); }
  50% { opacity: 0.3; transform: scale(0.7) rotate(180deg); }
}

/* 头部 */
.game-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 520px;
  margin-bottom: 30px;
  padding: 0 10px;
  position: relative;
  z-index: 10;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  border: 2px solid rgba(255, 107, 157, 0.3);
  border-radius: 20px;
  padding: 12px 22px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.back-btn:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 8px 25px rgba(255, 107, 157, 0.3);
  border-color: rgba(255, 107, 157, 0.6);
}

.back-icon {
  font-size: 1.2rem;
}

.header-title-wrap {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.game-title {
  font-size: 3rem;
  background: linear-gradient(135deg, #fff 0%, #FFE66D 30%, #FF6B9D 60%, #fff 100%);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
  animation: title-gradient 3s ease infinite;
  margin: 0;
}

@keyframes title-gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.title-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 60px;
  background: radial-gradient(ellipse, rgba(255, 230, 109, 0.4) 0%, transparent 70%);
  filter: blur(15px);
  animation: glow-pulse 2s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
  50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
}

.header-badge {
  background: linear-gradient(135deg, #A855F7, #FF6B9D);
  color: white;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: bold;
  box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4);
  animation: badge-float 3s ease-in-out infinite;
}

@keyframes badge-float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* 分数区域 */
.score-section {
  width: 100%;
  max-width: 480px;
  margin-bottom: 25px;
  position: relative;
  z-index: 10;
}

.score-main {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.score-card {
  flex: 1;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.9));
  border-radius: 25px;
  padding: 22px;
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease;
}

.score-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.18);
}

.score-card.current {
  border-color: rgba(255, 107, 157, 0.4);
}

.score-card.best {
  background: linear-gradient(145deg, rgba(255, 215, 0, 0.9), rgba(255, 170, 0, 0.85));
  border-color: rgba(255, 215, 0, 0.6);
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 107, 157, 0.1) 0%, transparent 70%);
  pointer-events: none;
}

.score-label-wrap {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.score-label {
  font-size: 0.85rem;
  color: #666;
  font-weight: 600;
}

.score-card.best .score-label {
  color: rgba(0, 0, 0, 0.7);
}

.score-trend {
  font-size: 1rem;
}

.score-display {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.score-number {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.score-card.best .score-number {
  background: linear-gradient(135deg, #fff, rgba(255, 255, 255, 0.8));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.score-unit {
  font-size: 0.9rem;
  color: #888;
}

.score-card.best .score-unit {
  color: rgba(0, 0, 0, 0.6);
}

.score-bar {
  height: 6px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
  margin-top: 12px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #FF6B9D, #A855F7, #4ECDC4);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.score-tip {
  font-size: 0.75rem;
  color: #999;
  margin-top: 8px;
  text-align: center;
}

.best-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 1.5rem;
  animation: badge-bounce 2s ease-in-out infinite;
}

@keyframes badge-bounce {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* 连击显示 */
.combo-display {
  text-align: center;
  margin-top: 15px;
  animation: combo-pop 0.3s ease-out;
}

@keyframes combo-pop {
  0% { opacity: 0; transform: scale(0.5); }
  50% { transform: scale(1.2); }
  100% { opacity: 1; transform: scale(1); }
}

.combo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: #FF6B9D;
  text-shadow: 0 0 20px rgba(255, 107, 157, 0.8), 0 0 40px rgba(255, 230, 109, 0.6);
}

.combo-multi {
  font-size: 1.8rem;
  font-weight: bold;
  color: #FFE66D;
  margin-left: 10px;
  text-shadow: 0 0 15px rgba(255, 230, 109, 0.8);
}

/* 控制按钮 */
.controls-section {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  position: relative;
  z-index: 10;
}

.control-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
  min-width: 100px;
}

.control-btn:hover:not(:disabled) {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.18);
}

.control-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.control-btn.restart:hover {
  border-color: #FF6B9D;
  box-shadow: 0 15px 35px rgba(255, 107, 157, 0.3);
}

.control-btn.undo:hover {
  border-color: #A855F7;
  box-shadow: 0 15px 35px rgba(168, 85, 247, 0.3);
}

.control-btn.hint:hover {
  border-color: #FFE66D;
  box-shadow: 0 15px 35px rgba(255, 230, 109, 0.3);
}

.btn-icon {
  font-size: 1.8rem;
}

.btn-text {
  font-size: 0.85rem;
  font-weight: 600;
  color: #333;
}

.btn-glow {
  position: absolute;
  top: 50%;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  transition: left 0.6s ease;
}

.control-btn:hover .btn-glow {
  left: 100%;
}

/* 游戏区域 */
.game-area-wrapper {
  position: relative;
  margin-bottom: 25px;
  z-index: 10;
}

.game-frame {
  position: absolute;
  top: -15px;
  left: -15px;
  right: -15px;
  bottom: -15px;
  pointer-events: none;
  z-index: 5;
}

.frame-corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 4px solid #FFD700;
}

.frame-corner.tl {
  top: 0;
  left: 0;
  border-right: none;
  border-bottom: none;
  border-radius: 15px 0 0 0;
}

.frame-corner.tr {
  top: 0;
  right: 0;
  border-left: none;
  border-bottom: none;
  border-radius: 0 15px 0 0;
}

.frame-corner.bl {
  bottom: 0;
  left: 0;
  border-right: none;
  border-top: none;
  border-radius: 0 0 0 15px;
}

.frame-corner.br {
  bottom: 0;
  right: 0;
  border-left: none;
  border-top: none;
  border-radius: 0 0 15px 0;
}

.frame-border-top, .frame-border-bottom {
  position: absolute;
  left: 40px;
  right: 40px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #FFD700, transparent);
}

.frame-border-top { top: 0; }
.frame-border-bottom { bottom: 0; }

.frame-border-left, .frame-border-right {
  position: absolute;
  top: 40px;
  bottom: 40px;
  width: 3px;
  background: linear-gradient(180deg, transparent, #FFD700, transparent);
}

.frame-border-left { left: 0; }
.frame-border-right { right: 0; }

.game-area {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.92));
  border-radius: 25px;
  padding: 25px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2), 0 0 40px rgba(255, 107, 157, 0.1);
  position: relative;
}

/* 动漫角色 */
.anime-sidekick {
  position: absolute;
  top: -15px;
  right: -70px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 20;
}

.sidekick-face {
  font-size: 56px;
  animation: face-bounce 2s ease-in-out infinite;
  filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.2));
}

.sidekick-face.happy { animation: face-happy 2s ease-in-out infinite; }
.sidekick-face.excited { animation: face-excited 0.5s ease-in-out infinite; }
.sidekick-face.sad { animation: face-sad 2s ease-in-out infinite; }

@keyframes face-bounce {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-8px) scale(1.05); }
}

@keyframes face-happy {
  0%, 100% { transform: translateY(0) rotate(-5deg); }
  50% { transform: translateY(-8px) rotate(5deg); }
}

@keyframes face-excited {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.2) rotate(-10deg); }
  75% { transform: scale(1.2) rotate(10deg); }
}

@keyframes face-sad {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(5px) rotate(-3deg); }
}

.sidekick-bubble {
  background: white;
  padding: 10px 18px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: bold;
  color: #333;
  margin-top: 5px;
  position: relative;
  animation: bubble-appear 0.3s ease-out;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  border: 2px solid rgba(255, 107, 157, 0.3);
}

.sidekick-bubble::before {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 10px 10px 0;
  border-style: solid;
  border-color: white transparent transparent;
}

@keyframes bubble-appear {
  from { opacity: 0; transform: translateY(15px) scale(0.7); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* 游戏状态 */
.game-status {
  position: absolute;
  top: 10px;
  left: 15px;
}

.status-badge {
  background: linear-gradient(135deg, #4ECDC4, #44A08D);
  color: white;
  padding: 6px 16px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 600;
  box-shadow: 0 3px 10px rgba(78, 205, 196, 0.4);
}

.status-badge.won {
  background: linear-gradient(135deg, #FFD700, #FF6B6B);
  box-shadow: 0 3px 10px rgba(255, 215, 0, 0.5);
  animation: won-pulse 1s ease-in-out infinite;
}

.status-badge.over {
  background: linear-gradient(135deg, #95A5A6, #7F8C8D);
}

@keyframes won-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* 操作提示 */
.action-hints {
  display: flex;
  gap: 25px;
  margin-bottom: 25px;
  position: relative;
  z-index: 10;
}

.hint-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  background: rgba(255, 255, 255, 0.85);
  padding: 10px 20px;
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

.hint-key {
  font-size: 1.1rem;
  font-weight: bold;
  color: #667eea;
}

.hint-desc {
  font-size: 0.75rem;
  color: #666;
}

/* 游戏规则 */
.rules-section {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.85));
  border-radius: 25px;
  padding: 25px;
  max-width: 450px;
  margin-bottom: 30px;
  border: 2px solid rgba(255, 255, 255, 0.6);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 10;
}

.rules-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.rules-icon {
  font-size: 1.8rem;
}

.rules-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: #333;
}

.rules-content {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.rule-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.rule-icon {
  font-size: 1.3rem;
}

.rule-text {
  font-size: 0.9rem;
  color: #666;
}

/* 弹窗 */
.submit-modal, .hint-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: modal-fade 0.3s ease;
}

@keyframes modal-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(5px);
}

.modal-content {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.98), rgba(255, 255, 255, 0.95));
  border-radius: 30px;
  padding: 0;
  max-width: 450px;
  width: 90%;
  overflow: hidden;
  animation: modal-scale 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

@keyframes modal-scale {
  from { opacity: 0; transform: scale(0.7); }
  to { opacity: 1; transform: scale(1); }
}

.modal-header {
  text-align: center;
  padding: 30px 30px 20px;
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.1), rgba(255, 107, 157, 0.1));
}

.modal-icon {
  font-size: 4rem;
  display: block;
  animation: emoji-bounce 0.5s ease-out;
}

@keyframes emoji-bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}

.modal-header h3 {
  font-size: 1.8rem;
  margin-top: 15px;
  color: #333;
}

.modal-body {
  padding: 25px 30px;
}

.final-score {
  text-align: center;
  margin-bottom: 20px;
}

.final-score .score-label {
  display: block;
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
}

.final-score .score-value {
  font-size: 3.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea, #FF6B9D);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.score-comparison {
  text-align: center;
  margin-bottom: 20px;
}

.new-record {
  font-size: 1.4rem;
  font-weight: bold;
  color: #FFD700;
  text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}

.name-input {
  width: 100%;
  padding: 18px;
  border: 3px solid #eee;
  border-radius: 15px;
  font-size: 1.1rem;
  margin-bottom: 20px;
  outline: none;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.name-input:focus {
  border-color: #A855F7;
  box-shadow: 0 0 20px rgba(168, 85, 247, 0.2);
}

.modal-footer {
  display: flex;
  gap: 15px;
  padding: 20px 30px 30px;
}

.submit-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 15px;
  padding: 18px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

.cancel-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: #f0f0f0;
  color: #666;
  border: none;
  border-radius: 15px;
  padding: 18px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background: #e0e0e0;
  transform: translateY(-3px);
}

/* 提示弹窗特殊样式 */
.hint-content {
  max-width: 400px;
}

.hint-list {
  list-style: none;
  padding: 0;
}

.hint-list li {
  padding: 12px 0;
  border-bottom: 1px dashed #eee;
  color: #666;
  font-size: 1rem;
}

.hint-list li:last-child {
  border-bottom: none;
}

/* 底部装饰 */
.bottom-decoration {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100px;
  pointer-events: none;
  z-index: 0;
}

.bottom-star {
  position: absolute;
  font-size: 1rem;
  animation: bottom-star-twinkle 3s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.15s);
  opacity: 0.4;
}

.bottom-star:nth-child(odd) { bottom: calc(var(--i) * 5%); left: calc(var(--i) * 4%); }
.bottom-star:nth-child(even) { bottom: calc(var(--i) * 4%); right: calc(var(--i) * 4%); }

@keyframes bottom-star-twinkle {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 0.7; transform: scale(1.3); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .game-title {
    font-size: 2.2rem;
  }
  
  .header-badge {
    font-size: 0.85rem;
    padding: 6px 14px;
  }
  
  .score-main {
    flex-direction: column;
    gap: 15px;
  }
  
  .controls-section {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .control-btn {
    min-width: 80px;
    padding: 12px 15px;
  }
  
  .anime-sidekick {
    right: -50px;
  }
  
  .sidekick-face {
    font-size: 40px;
  }
  
  .rules-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .game-container {
    padding: 15px;
  }
  
  .game-header {
    flex-wrap: wrap;
    justify-content: center;
    gap: 15px;
  }
  
  .back-btn {
    order: 1;
    width: 100%;
    justify-content: center;
  }
  
  .header-title-wrap {
    order: 0;
    width: 100%;
  }
  
  .header-badge {
    order: 2;
  }
  
  .anime-sidekick {
    right: -40px;
    top: -10px;
  }
  
  .sidekick-face {
    font-size: 32px;
  }
  
  .sidekick-bubble {
    font-size: 0.8rem;
    padding: 8px 12px;
  }
  
  .action-hints {
    gap: 10px;
  }
  
  .hint-item {
    padding: 8px 12px;
  }
}
</style>