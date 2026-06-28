<template>
  <div 
    class="game-2048" 
    ref="gameContainer"
    tabindex="0"
    @click="handleClick"
  >
    <!-- 随机装饰GIF -->
    <div class="anime-decorations">
      <div 
        v-for="decor in animeDecorations" 
        :key="decor.id" 
        class="anime-decoration"
        :style="{
          left: decor.x + '%',
          top: decor.y + '%',
          '--delay': decor.delay + 's',
          '--duration': decor.duration + 's'
        }"
      >
        <img :src="decor.gif" alt="anime decoration" class="decor-gif" />
      </div>
    </div>
    
    <!-- 动漫角色表情 -->
    <div class="anime-character">
      <div class="character-face">{{ currentEmoji }}</div>
      <div class="character-bubble" v-if="showBubble">{{ bubbleText }}</div>
    </div>
    
    <!-- 特效文字 -->
    <div class="effect-texts">
      <div 
        v-for="text in effectTexts" 
        :key="text.id" 
        class="effect-text"
        :style="{
          left: text.x + '%',
          top: text.y + '%',
          '--color': text.color
        }"
      >{{ text.text }}</div>
    </div>
    
    <canvas 
      ref="canvasRef" 
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      class="game-canvas"
    ></canvas>
    
    <div v-if="gameWon" class="game-overlay win">
      <div class="overlay-content">
        <div class="overlay-emoji">🎉</div>
        <h2>恭喜!</h2>
        <p>你合成了2048!</p>
        <p class="current-score">当前分数: <strong>{{ score }}</strong></p>
        <button @click="continueGame">继续挑战更高分数!</button>
      </div>
    </div>
    
    <div v-if="gameOver" class="game-overlay lose">
      <div class="overlay-content">
        <div class="overlay-emoji">💔</div>
        <h2>游戏结束</h2>
        <p>最终分数: <strong>{{ score }}</strong></p>
        <p>最高记录: <strong>{{ bestScore }}</strong></p>
        <button @click="restart">再玩一次</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'

const emit = defineEmits(['score-update', 'game-over', 'game-win', 'show-reward'])

const canvasRef = ref(null)
const gameContainer = ref(null)
const gridSize = 4
const cellSize = 80
const gap = 10
const padding = 20

const gameOver = ref(false)
const gameWon = ref(false)
const score = ref(0)
const bestScore = ref(0)
const grid = ref([])
const history = ref([])
const lastRewardScore = ref(0)
const isGameActive = ref(true)

// 动漫装饰GIF
const decorGifUrls = [
  'https://s1.aigei.com/src/img/gif/cf/cfc0f24c2a4648918c766b4cfccf79ba.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:Rt8wq3hdSb6ekn8sBJJwheIFVlk=',
  'https://s1.aigei.com/src/img/gif/2c/2c1d291638d24ba5869a2da266457d2b.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:iCowZcNL2MaLShjuzKd39k5I4zA=',
  'https://s1.aigei.com/src/img/gif/ed/ed67aa22ff054fda9d3a456778086158.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:ZJklG1KOe5SmYAgkL-zdIGBHdkw=',
  'https://s1.aigei.com/src/img/gif/04/04ce71e66f5d47dabaaba2b09d8150e9.gif?imageMogr2/auto-orient/thumbnail/!282x282r/gravity/Center/crop/282x282/quality/85/%7CimageView2/2/w/282&e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:AdHiuK9AHm2O1bin5ygIOtUEzdg=',
  'https://s1.aigei.com/src/img/gif/6f/6f7fed9414d54d8e952dbe4e982df39b.gif?imageMogr2/auto-orient/thumbnail/!282x282r/gravity/Center/crop/282x282/quality/85/%7CimageView2/2/w/282&e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:w6BAnzNCh4t4eO5wjweuD9do95k='
]

const animeDecorations = ref([])
const effectTexts = ref([])
const currentEmoji = ref('😊')
const showBubble = ref(false)
const bubbleText = ref('')

const characterEmojis = {
  happy: ['😊', '😄', '😆', '🥰', '🤩', '😎'],
  excited: ['😍', '🤯', '🥳', '😱', '🤗'],
  sad: ['😢', '😔', '😞', '😿'],
  thinking: ['🤔', '🧐', '😌']
}

const bubbleTexts = {
  happy: ['太棒了!', '厉害!', '完美!', 'Nice!', 'Amazing!'],
  excited: ['哇!', '超酷!', '太厉害了!', '难以置信!', 'OMG!'],
  sad: ['加油!', '别放弃!', '再来一次!', '不要气馁!'],
  thinking: ['想想策略...', '下一步怎么走?', '冷静思考']
}

const effectColors = ['#FFD700', '#FF6B9D', '#00FFFF', '#A855F7', '#4ECDC4', '#FF6347']

const generateDecorations = () => {
  const count = Math.floor(Math.random() * 3) + 1
  animeDecorations.value = []
  for (let i = 0; i < count; i++) {
    animeDecorations.value.push({
      id: Date.now() + i,
      x: Math.random() * 90 + 5,
      y: Math.random() * 90 + 5,
      gif: decorGifUrls[Math.floor(Math.random() * decorGifUrls.length)],
      delay: Math.random() * 2,
      duration: Math.random() * 3 + 4
    })
  }
}

const addEffectText = (text, x, y) => {
  const newText = {
    id: Date.now(),
    text,
    x: x || Math.random() * 80 + 10,
    y: y || Math.random() * 80 + 10,
    color: effectColors[Math.floor(Math.random() * effectColors.length)]
  }
  effectTexts.value.push(newText)
  setTimeout(() => {
    effectTexts.value = effectTexts.value.filter(t => t.id !== newText.id)
  }, 2000)
}

const updateCharacter = (type) => {
  const emojis = characterEmojis[type] || characterEmojis.happy
  const texts = bubbleTexts[type] || bubbleTexts.happy
  currentEmoji.value = emojis[Math.floor(Math.random() * emojis.length)]
  bubbleText.value = texts[Math.floor(Math.random() * texts.length)]
  showBubble.value = true
  setTimeout(() => {
    showBubble.value = false
  }, 2000)
}

const colors = {
  0: '#cdc1b4',
  2: '#eee4da',
  4: '#ede0c8',
  8: '#f2b179',
  16: '#f59563',
  32: '#f67c5f',
  64: '#f65e3b',
  128: '#edcf72',
  256: '#edcc61',
  512: '#edc850',
  1024: '#edc53f',
  2048: '#edc22e'
}

const textColors = {
  0: '#cdc1b4',
  2: '#776e65',
  4: '#776e65',
  8: '#f9f6f2',
  16: '#f9f6f2',
  32: '#f9f6f2',
  64: '#f9f6f2',
  128: '#f9f6f2',
  256: '#f9f6f2',
  512: '#f9f6f2',
  1024: '#f9f6f2',
  2048: '#f9f6f2'
}

const initGrid = () => {
  grid.value = Array(gridSize).fill(null).map(() => Array(gridSize).fill(0))
  score.value = 0
  gameOver.value = false
  gameWon.value = false
  history.value = []
  lastRewardScore.value = 0
  isGameActive.value = true
  currentEmoji.value = '😊'
  effectTexts.value = []
  generateDecorations()
  addRandomTile()
  addRandomTile()
  emit('score-update', score.value)
  draw()
  
  nextTick(() => {
    gameContainer.value?.focus()
  })
}

const addRandomTile = () => {
  const emptyCells = []
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid.value[i][j] === 0) {
        emptyCells.push({ row: i, col: j })
      }
    }
  }
  
  if (emptyCells.length > 0) {
    const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)]
    const newValue = Math.random() < 0.9 ? 2 : 4
    grid.value[randomCell.row][randomCell.col] = newValue
    
    if (Math.random() < 0.3) {
      addEffectText(newValue === 4 ? '✨' : '🌟', (randomCell.col + 0.5) * 25, (randomCell.row + 0.5) * 25)
    }
  }
}

const saveState = () => {
  history.value.push({
    grid: grid.value.map(row => [...row]),
    score: score.value,
    gameWon: gameWon.value
  })
  if (history.value.length > 5) {
    history.value.shift()
  }
}

const undo = () => {
  if (history.value.length > 0) {
    const prevState = history.value.pop()
    grid.value = prevState.grid
    score.value = prevState.score
    gameWon.value = prevState.gameWon
    gameOver.value = false
    isGameActive.value = true
    emit('score-update', score.value)
    draw()
    updateCharacter('thinking')
  }
}

const move = (direction) => {
  if (!isGameActive.value || gameOver.value) return
  
  saveState()
  
  let moved = false
  let merged = false
  const newGrid = grid.value.map(row => [...row])
  
  if (direction === 'up') {
    for (let col = 0; col < gridSize; col++) {
      const column = []
      for (let row = 0; row < gridSize; row++) {
        if (newGrid[row][col] !== 0) {
          column.push(newGrid[row][col])
        }
      }
      const result = merge(column)
      merged = merged || result.merged
      for (let row = 0; row < gridSize; row++) {
        newGrid[row][col] = result.line[row] || 0
      }
    }
  } else if (direction === 'down') {
    for (let col = 0; col < gridSize; col++) {
      const column = []
      for (let row = gridSize - 1; row >= 0; row--) {
        if (newGrid[row][col] !== 0) {
          column.push(newGrid[row][col])
        }
      }
      const result = merge(column)
      merged = merged || result.merged
      for (let row = gridSize - 1; row >= 0; row--) {
        newGrid[row][col] = result.line[gridSize - 1 - row] || 0
      }
    }
  } else if (direction === 'left') {
    for (let row = 0; row < gridSize; row++) {
      const line = newGrid[row].filter(cell => cell !== 0)
      const result = merge(line)
      merged = merged || result.merged
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = result.line[col] || 0
      }
    }
  } else if (direction === 'right') {
    for (let row = 0; row < gridSize; row++) {
      const line = newGrid[row].filter(cell => cell !== 0).reverse()
      const result = merge(line)
      merged = merged || result.merged
      const mergedLine = result.line.reverse()
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = mergedLine[col] || 0
      }
    }
  }
  
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid.value[i][j] !== newGrid[i][j]) {
        moved = true
        break
      }
    }
    if (moved) break
  }
  
  if (moved) {
    grid.value = newGrid
    addRandomTile()
    
    if (merged && Math.random() < 0.5) {
      updateCharacter('happy')
    }
    
    checkGameState()
    emit('score-update', score.value)
    draw()
  } else {
    history.value.pop()
    if (!canMove()) {
      gameOver.value = true
      isGameActive.value = false
      updateCharacter('sad')
      emit('game-over')
    }
  }
}

const merge = (line) => {
  const mergedLine = []
  let merged = false
  let i = 0
  
  while (i < line.length) {
    if (i + 1 < line.length && line[i] === line[i + 1]) {
      const newValue = line[i] * 2
      mergedLine.push(newValue)
      score.value += newValue
      merged = true
      
      if (newValue === 2048 && !gameWon.value) {
        gameWon.value = true
        updateCharacter('excited')
        addEffectText('🏆', 50, 50)
        emit('game-win')
      } else if (newValue >= 128) {
        addEffectText(`+${newValue}`, Math.random() * 80 + 10, Math.random() * 80 + 10)
      }
      
      i += 2
    } else {
      mergedLine.push(line[i])
      i++
    }
  }
  
  return { line: mergedLine, merged }
}

const canMove = () => {
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (grid.value[i][j] === 0) return true
    }
  }
  
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      if (i < gridSize - 1 && grid.value[i][j] === grid.value[i + 1][j]) return true
      if (j < gridSize - 1 && grid.value[i][j] === grid.value[i][j + 1]) return true
    }
  }
  
  return false
}

const checkGameState = () => {
  if (!canMove()) {
    gameOver.value = true
    isGameActive.value = false
    updateCharacter('sad')
    emit('game-over')
  }
}

const draw = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  const totalSize = cellSize * gridSize + gap * (gridSize - 1) + padding * 2
  
  ctx.fillStyle = '#bbada0'
  ctx.fillRect(0, 0, totalSize, totalSize)
  
  for (let i = 0; i < gridSize; i++) {
    for (let j = 0; j < gridSize; j++) {
      const x = padding + j * (cellSize + gap)
      const y = padding + i * (cellSize + gap)
      const value = grid.value[i][j]
      
      ctx.fillStyle = colors[value] || '#3c3a32'
      ctx.fillRect(x, y, cellSize, cellSize)
      
      if (value !== 0) {
        ctx.fillStyle = textColors[value] || '#f9f6f2'
        ctx.font = value >= 1000 ? '36px Arial' : '48px Arial'
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(value.toString(), x + cellSize / 2, y + cellSize / 2)
      }
    }
  }
}

const handleKeydown = (e) => {
  if (!isGameActive.value || gameOver.value) return
  
  switch (e.key) {
    case 'ArrowUp':
    case 'w':
    case 'W':
      e.preventDefault()
      move('up')
      break
    case 'ArrowDown':
    case 's':
    case 'S':
      e.preventDefault()
      move('down')
      break
    case 'ArrowLeft':
    case 'a':
    case 'A':
      e.preventDefault()
      move('left')
      break
    case 'ArrowRight':
    case 'd':
    case 'D':
      e.preventDefault()
      move('right')
      break
  }
}

const handleClick = () => {
  gameContainer.value?.focus()
}

let touchStartX = 0
let touchStartY = 0

const handleTouchStart = (e) => {
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
}

const handleTouchEnd = (e) => {
  if (!isGameActive.value || gameOver.value) return
  
  const touchEndX = e.changedTouches[0].clientX
  const touchEndY = e.changedTouches[0].clientY
  
  const deltaX = touchEndX - touchStartX
  const deltaY = touchEndY - touchStartY
  const minSwipe = 30
  
  if (Math.abs(deltaX) > Math.abs(deltaY)) {
    if (Math.abs(deltaX) > minSwipe) {
      move(deltaX > 0 ? 'right' : 'left')
    }
  } else {
    if (Math.abs(deltaY) > minSwipe) {
      move(deltaY > 0 ? 'down' : 'up')
    }
  }
}

const restart = () => {
  initGrid()
}

const continueGame = () => {
  gameWon.value = false
  checkGameState()
  draw()
  gameContainer.value?.focus()
}

onMounted(() => {
  const canvas = canvasRef.value
  const totalSize = cellSize * gridSize + gap * (gridSize - 1) + padding * 2
  canvas.width = totalSize
  canvas.height = totalSize
  
  const savedBest = localStorage.getItem('2048_best_score')
  if (savedBest) {
    bestScore.value = parseInt(savedBest)
  }
  
  initGrid()
  
  window.addEventListener('keydown', handleKeydown)
  
  // 定时刷新装饰
  setInterval(() => {
    if (isGameActive.value && !gameOver.value) {
      generateDecorations()
    }
  }, 15000)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

watch(score, (newScore) => {
  if (newScore > bestScore.value) {
    bestScore.value = newScore
    localStorage.setItem('2048_best_score', newScore.toString())
  }
  
  const rewardThreshold = Math.floor(newScore / 500) * 500
  if (rewardThreshold > lastRewardScore.value && rewardThreshold >= 500) {
    lastRewardScore.value = rewardThreshold
    emit('show-reward', { points: 500, currentScore: newScore })
  }
})

defineExpose({
  restart,
  undo
})
</script>

<style scoped>
.game-2048 {
  position: relative;
  outline: none;
  cursor: pointer;
}

.game-2048:focus {
  outline: none;
}

.game-canvas {
  border-radius: 10px;
  display: block;
  position: relative;
  z-index: 10;
}

/* 随机装饰GIF */
.anime-decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
}

.anime-decoration {
  position: absolute;
  animation: decor-float var(--duration) ease-in-out infinite;
  animation-delay: var(--delay);
}

.decor-gif {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

@keyframes decor-float {
  0%, 100% { transform: translateY(0) rotate(0deg) scale(1); opacity: 0.6; }
  25% { transform: translateY(-10px) rotate(5deg) scale(1.1); opacity: 0.8; }
  50% { transform: translateY(-5px) rotate(-5deg) scale(0.9); opacity: 0.7; }
  75% { transform: translateY(-15px) rotate(10deg) scale(1.05); opacity: 0.8; }
}

/* 动漫角色表情 */
.anime-character {
  position: absolute;
  top: -20px;
  right: -80px;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.character-face {
  font-size: 48px;
  animation: face-bounce 2s ease-in-out infinite;
}

@keyframes face-bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.character-bubble {
  background: white;
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-top: 5px;
  position: relative;
  animation: bubble-appear 0.3s ease-out;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.character-bubble::before {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  border-width: 8px 8px 0;
  border-style: solid;
  border-color: white transparent transparent;
}

@keyframes bubble-appear {
  from { opacity: 0; transform: translateY(10px) scale(0.8); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

/* 特效文字 */
.effect-texts {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 15;
}

.effect-text {
  position: absolute;
  font-size: 28px;
  font-weight: bold;
  color: var(--color);
  text-shadow: 0 0 10px var(--color), 0 0 20px var(--color);
  animation: text-float 2s ease-out forwards;
}

@keyframes text-float {
  0% { opacity: 0; transform: scale(0) translateY(0); }
  20% { opacity: 1; transform: scale(1.5) translateY(-10px); }
  100% { opacity: 0; transform: scale(1) translateY(-50px); }
}

/* 游戏覆盖层 */
.game-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  z-index: 100;
}

.game-overlay.win {
  background: rgba(237, 194, 46, 0.85);
  animation: fadeIn 0.3s ease;
}

.game-overlay.lose {
  background: rgba(238, 228, 218, 0.95);
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.overlay-content {
  text-align: center;
  color: #776e65;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.overlay-emoji {
  font-size: 4rem;
  animation: emoji-bounce 0.5s ease-out;
}

@keyframes emoji-bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}

.overlay-content h2 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  margin-top: 10px;
}

.overlay-content p {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

.current-score {
  font-size: 1.2rem;
  color: #776e65;
}

.overlay-content button {
  background: #8f7a66;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 12px 30px;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.2s;
}

.overlay-content button:hover {
  background: #9f8b77;
  transform: scale(1.05);
}
</style>