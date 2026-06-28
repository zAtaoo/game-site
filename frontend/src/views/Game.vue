<template>
  <div class="game-container">
    <AnimeBackground />
    
    <header class="game-header">
      <button class="back-btn" @click="goBack">← 返回</button>
      <h1 class="game-title">{{ gameName }}</h1>
    </header>

    <main class="game-content">
      <div class="game-info">
        <div class="score-board">
          <div class="score-item">
            <span class="score-label">得分</span>
            <span class="score-value">{{ score }}</span>
          </div>
          <div class="score-item best">
            <span class="score-label">最高</span>
            <span class="score-value">{{ bestScore }}</span>
          </div>
        </div>
        
        <div class="game-controls">
          <button class="control-btn" @click="restartGame">🔄 重新开始</button>
          <button class="control-btn" @click="undoMove">↩️ 撤销</button>
        </div>
      </div>

      <div class="game-area">
        <Game2048 
          ref="gameRef"
          @score-update="handleScoreUpdate"
          @game-over="handleGameOver"
          @game-win="handleGameWin"
          @show-reward="handleShowReward"
        />
      </div>

      <div class="game-rules">
        <h3>游戏规则</h3>
        <ul>
          <li>使用方向键或点击滑动来移动方块</li>
          <li>相同数字的方块相遇时会合并</li>
          <li>目标：合成出2048方块！</li>
          <li>每获得500分有惊喜奖励哦~ 🎁</li>
        </ul>
      </div>

      <div v-if="showSubmit" class="submit-modal">
        <div class="modal-content">
          <h3>🎉 游戏结束!</h3>
          <p>最终得分: <strong>{{ score }}</strong></p>
          <input 
            v-model="playerName" 
            type="text" 
            placeholder="输入您的昵称" 
            maxlength="10"
            class="name-input"
          />
          <div class="modal-buttons">
            <button class="submit-btn" @click="submitScore">提交分数</button>
            <button class="cancel-btn" @click="closeModal">关闭</button>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 奖励效果 -->
    <RewardEffect 
      :show="showReward" 
      :points="rewardPoints"
      @complete="hideReward"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
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
const playerName = ref('')
const showReward = ref(false)
const rewardPoints = ref(500)

onMounted(async () => {
  const savedBest = localStorage.getItem('2048_best_score')
  if (savedBest) {
    bestScore.value = parseInt(savedBest)
  }
  
  try {
    const res = await axios.get(`/api/games/${route.params.id}`)
    gameName.value = res.data.name
  } catch (error) {
    console.error('Failed to load game info:', error)
  }
})

const goBack = () => {
  router.push('/')
}

const handleScoreUpdate = (newScore) => {
  score.value = newScore
  if (newScore > bestScore.value) {
    bestScore.value = newScore
    localStorage.setItem('2048_best_score', newScore.toString())
  }
}

const handleGameOver = () => {
  showSubmit.value = true
}

const handleGameWin = () => {
  showSubmit.value = true
}

const handleShowReward = (data) => {
  rewardPoints.value = data.points
  showReward.value = true
}

const hideReward = () => {
  showReward.value = false
}

const restartGame = () => {
  gameRef.value?.restart()
  score.value = 0
  showSubmit.value = false
}

const undoMove = () => {
  gameRef.value?.undo()
}

const closeModal = () => {
  showSubmit.value = false
}

const submitScore = async () => {
  const name = playerName.value.trim() || '匿名玩家'
  try {
    await axios.post('/api/score', {
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
</script>

<style scoped>
.game-container {
  min-height: 100vh;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.game-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  width: 100%;
  max-width: 500px;
}

.back-btn {
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.back-btn:hover {
  transform: scale(1.05);
}

.game-title {
  font-size: 2rem;
  color: #fff;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.game-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  position: relative;
  z-index: 1;
}

.game-info {
  width: 100%;
  max-width: 400px;
}

.score-board {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 20px;
}

.score-item {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 15px 30px;
  text-align: center;
  min-width: 120px;
}

.score-item.best {
  background: linear-gradient(135deg, #ffd700, #ffaa00);
}

.score-label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 5px;
}

.score-item.best .score-label {
  color: rgba(0, 0, 0, 0.6);
}

.score-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
}

.game-controls {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.control-btn {
  background: rgba(255, 255, 255, 0.95);
  border: none;
  border-radius: 10px;
  padding: 12px 25px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.control-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.game-area {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.game-rules {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 20px;
  max-width: 400px;
}

.game-rules h3 {
  color: #333;
  margin-bottom: 15px;
}

.game-rules ul {
  list-style: none;
  color: #666;
}

.game-rules li {
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.game-rules li:last-child {
  border-bottom: none;
}

.submit-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  max-width: 400px;
  width: 90%;
}

.modal-content h3 {
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.modal-content p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.name-input {
  width: 100%;
  padding: 15px;
  border: 2px solid #ddd;
  border-radius: 10px;
  font-size: 1rem;
  margin-bottom: 20px;
  outline: none;
}

.name-input:focus {
  border-color: #667eea;
}

.modal-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 12px 30px;
  font-size: 1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.submit-btn:hover {
  transform: scale(1.05);
}

.cancel-btn {
  background: #eee;
  border: none;
  border-radius: 10px;
  padding: 12px 30px;
  font-size: 1rem;
  cursor: pointer;
}

.cancel-btn:hover {
  background: #ddd;
}
</style>