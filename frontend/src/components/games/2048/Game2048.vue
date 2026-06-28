<template>
  <div 
    class="game-2048" 
    ref="gameContainer"
    tabindex="0"
    @click="handleClick"
  >
    <canvas 
      ref="canvasRef" 
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      class="game-canvas"
    ></canvas>
    
    <div v-if="gameWon" class="game-overlay win">
      <div class="overlay-content">
        <h2>🎉 恭喜!</h2>
        <p>你合成了2048!</p>
        <p class="current-score">当前分数: <strong>{{ score }}</strong></p>
        <button @click="continueGame">继续挑战更高分数!</button>
      </div>
    </div>
    
    <div v-if="gameOver" class="game-overlay lose">
      <div class="overlay-content">
        <h2>💔 游戏结束</h2>
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
    grid.value[randomCell.row][randomCell.col] = Math.random() < 0.9 ? 2 : 4
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
  }
}

const move = (direction) => {
  if (!isGameActive.value || gameOver.value) return
  
  saveState()
  
  let moved = false
  const newGrid = grid.value.map(row => [...row])
  
  if (direction === 'up') {
    for (let col = 0; col < gridSize; col++) {
      const column = []
      for (let row = 0; row < gridSize; row++) {
        if (newGrid[row][col] !== 0) {
          column.push(newGrid[row][col])
        }
      }
      const merged = merge(column)
      for (let row = 0; row < gridSize; row++) {
        newGrid[row][col] = merged[row] || 0
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
      const merged = merge(column)
      for (let row = gridSize - 1; row >= 0; row--) {
        newGrid[row][col] = merged[gridSize - 1 - row] || 0
      }
    }
  } else if (direction === 'left') {
    for (let row = 0; row < gridSize; row++) {
      const line = newGrid[row].filter(cell => cell !== 0)
      const merged = merge(line)
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = merged[col] || 0
      }
    }
  } else if (direction === 'right') {
    for (let row = 0; row < gridSize; row++) {
      const line = newGrid[row].filter(cell => cell !== 0).reverse()
      const merged = merge(line).reverse()
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = merged[col] || 0
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
    checkGameState()
    emit('score-update', score.value)
    draw()
  } else {
    history.value.pop()
    if (!canMove()) {
      gameOver.value = true
      isGameActive.value = false
      emit('game-over')
    }
  }
}

const merge = (line) => {
  const merged = []
  let i = 0
  
  while (i < line.length) {
    if (i + 1 < line.length && line[i] === line[i + 1]) {
      const newValue = line[i] * 2
      merged.push(newValue)
      score.value += newValue
      if (newValue === 2048 && !gameWon.value) {
        gameWon.value = true
        emit('game-win')
      }
      i += 2
    } else {
      merged.push(line[i])
      i++
    }
  }
  
  return merged
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
}

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
  z-index: 10;
}

.game-overlay.win {
  background: rgba(237, 194, 46, 0.8);
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

.overlay-content h2 {
  font-size: 2.5rem;
  margin-bottom: 15px;
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