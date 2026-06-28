<template>
  <div 
    class="game-2048" 
    ref="gameContainer"
    tabindex="0"
    @click="handleClick"
  >
    <!-- 方块合并特效 -->
    <div class="merge-effects">
      <div 
        v-for="effect in mergeEffects" 
        :key="effect.id" 
        class="merge-effect"
        :style="{
          left: effect.x + '%',
          top: effect.y + '%',
          '--value': effect.value,
          '--color': effect.color
        }"
      >+{{ effect.value }}</div>
    </div>
    
    <!-- 方块出现特效 -->
    <div class="appear-effects">
      <div 
        v-for="effect in appearEffects" 
        :key="effect.id" 
        class="appear-effect"
        :style="{
          left: effect.x + '%',
          top: effect.y + '%',
          '--size': effect.size + 'px'
        }"
      ></div>
    </div>
    
    <!-- 游戏状态提示 -->
    <div class="game-toast" v-if="showToast">{{ toastMessage }}</div>

    <canvas 
      ref="canvasRef" 
      @touchstart="handleTouchStart"
      @touchend="handleTouchEnd"
      @touchmove="handleTouchMove"
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

const emit = defineEmits(['score-update', 'game-over', 'game-win', 'show-reward', 'combo'])

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
const comboCount = ref(0)
const comboTimer = ref(null)
const mergeEffects = ref([])
const appearEffects = ref([])
const showToast = ref(false)
const toastMessage = ref('')

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
  comboCount.value = 0
  mergeEffects.value = []
  appearEffects.value = []
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
    addAppearEffect(randomCell.col, randomCell.row)
    playSound('appear', newValue === 4 ? 0.8 : 0.5)
  }
}

const addAppearEffect = (col, row) => {
  const effect = {
    id: Date.now() + Math.random(),
    x: (col + 0.5) * 25,
    y: (row + 0.5) * 25,
    size: cellSize
  }
  appearEffects.value.push(effect)
  setTimeout(() => {
    appearEffects.value = appearEffects.value.filter(e => e.id !== effect.id)
  }, 500)
}

const addMergeEffect = (col, row, value) => {
  const effect = {
    id: Date.now() + Math.random(),
    x: (col + 0.5) * 25,
    y: (row + 0.5) * 25,
    value,
    color: colors[value] || '#3c3a32'
  }
  mergeEffects.value.push(effect)
  setTimeout(() => {
    mergeEffects.value = mergeEffects.value.filter(e => e.id !== effect.id)
  }, 800)
}

const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 1500)
}

const playSound = (type, volume = 0.1) => {
  if (!window.audioContext) {
    window.audioContext = new (window.AudioContext || window.webkitAudioContext)()
  }
  const ctx = window.audioContext
  const now = ctx.currentTime
  const osc = ctx.createOscillator()
  const gain = ctx.createGain()
  
  gain.gain.setValueAtTime(volume, now)
  
  if (type === 'move') {
    osc.type = 'sine'
    osc.frequency.setValueAtTime(200 + Math.random() * 100, now)
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1)
    osc.start(now)
    osc.stop(now + 0.1)
  } else if (type === 'merge') {
    osc.type = 'triangle'
    osc.frequency.setValueAtTime(400, now)
    osc.frequency.exponentialRampToValueAtTime(800, now + 0.15)
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2)
    osc.start(now)
    osc.stop(now + 0.2)
  } else if (type === 'appear') {
    osc.type = 'sine'
    osc.frequency.setValueAtTime(600, now)
    osc.frequency.exponentialRampToValueAtTime(400, now + 0.1)
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.15)
    osc.start(now)
    osc.stop(now + 0.15)
  } else if (type === 'win') {
    osc.type = 'sine'
    const notes = [523.25, 659.25, 783.99, 1046.50]
    notes.forEach((freq, i) => {
      const o = ctx.createOscillator()
      const g = ctx.createGain()
      o.type = 'sine'
      o.frequency.value = freq
      g.gain.setValueAtTime(0.1, now + i * 0.15)
      g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.15 + 0.3)
      o.connect(g)
      g.connect(ctx.destination)
      o.start(now + i * 0.15)
      o.stop(now + i * 0.15 + 0.3)
    })
  } else if (type === 'lose') {
    osc.type = 'sawtooth'
    osc.frequency.setValueAtTime(300, now)
    osc.frequency.exponentialRampToValueAtTime(150, now + 0.5)
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5)
    osc.start(now)
    osc.stop(now + 0.5)
  } else if (type === 'combo') {
    osc.type = 'square'
    osc.frequency.setValueAtTime(800 + comboCount.value * 100, now)
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.1)
    osc.start(now)
    osc.stop(now + 0.1)
  }
  
  osc.connect(gain)
  gain.connect(ctx.destination)
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

const updateCombo = () => {
  comboCount.value++
  emit('combo', comboCount.value)
  if (comboTimer.value) {
    clearTimeout(comboTimer.value)
  }
  comboTimer.value = setTimeout(() => {
    comboCount.value = 0
    emit('combo', 0)
  }, 2000)
  playSound('combo')
}

const move = (direction) => {
  if (!isGameActive.value || gameOver.value) return
  
  saveState()
  
  let moved = false
  let merged = false
  let scoreGained = 0
  let mergedPositions = []
  let won = false
  let highMergeValue = 0
  
  const newGrid = grid.value.map(row => [...row])
  
  const processLine = (line) => {
    const filtered = line.filter(item => item.value !== 0)
    const result = []
    const positions = []
    let lineMerged = false
    let lineScore = 0
    
    let i = 0
    while (i < filtered.length) {
      if (i + 1 < filtered.length && filtered[i].value === filtered[i + 1].value) {
        const newValue = filtered[i].value * 2
        result.push({ value: newValue, merged: true })
        lineScore += newValue
        lineMerged = true
        positions.push(result.length - 1)
        
        if (newValue > highMergeValue) {
          highMergeValue = newValue
        }
        
        if (newValue === 2048 && !gameWon.value) {
          won = true
        }
        
        i += 2 // Skip next element as it's merged
      } else {
        result.push({ value: filtered[i].value, merged: false })
        i++
      }
    }
    
    while (result.length < gridSize) {
      result.push({ value: 0, merged: false })
    }
    
    return { line: result, merged: lineMerged, score: lineScore, positions }
  }
  
  if (direction === 'up') {
    for (let col = 0; col < gridSize; col++) {
      const column = []
      for (let row = 0; row < gridSize; row++) {
        column.push({ value: newGrid[row][col], row, col })
      }
      const result = processLine(column)
      merged = merged || result.merged
      scoreGained += result.score
      result.positions.forEach(pos => {
        mergedPositions.push({ col, row: pos })
      })
      for (let row = 0; row < gridSize; row++) {
        newGrid[row][col] = result.line[row].value
      }
    }
  } else if (direction === 'down') {
    for (let col = 0; col < gridSize; col++) {
      const column = []
      for (let row = gridSize - 1; row >= 0; row--) {
        column.push({ value: newGrid[row][col], row, col })
      }
      const result = processLine(column)
      merged = merged || result.merged
      scoreGained += result.score
      result.positions.forEach(pos => {
        mergedPositions.push({ col, row: gridSize - 1 - pos })
      })
      for (let row = gridSize - 1; row >= 0; row--) {
        newGrid[row][col] = result.line[gridSize - 1 - row].value
      }
    }
  } else if (direction === 'left') {
    for (let row = 0; row < gridSize; row++) {
      const line = []
      for (let col = 0; col < gridSize; col++) {
        line.push({ value: newGrid[row][col], row, col })
      }
      const result = processLine(line)
      merged = merged || result.merged
      scoreGained += result.score
      result.positions.forEach(pos => {
        mergedPositions.push({ col: pos, row })
      })
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = result.line[col].value
      }
    }
  } else if (direction === 'right') {
    for (let row = 0; row < gridSize; row++) {
      const line = []
      for (let col = gridSize - 1; col >= 0; col--) {
        line.push({ value: newGrid[row][col], row, col })
      }
      const result = processLine(line)
      merged = merged || result.merged
      scoreGained += result.score
      result.positions.forEach(pos => {
        mergedPositions.push({ col: gridSize - 1 - pos, row })
      })
      const mergedLine = result.line.reverse()
      for (let col = 0; col < gridSize; col++) {
        newGrid[row][col] = mergedLine[col].value
      }
    }
  }
  
  // Check if anything moved
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
    score.value += scoreGained
    
    if (won) {
      gameWon.value = true
      playSound('win')
      showToastMessage('🎉 恭喜合成2048!')
      emit('game-win')
    }
    else if (highMergeValue >= 128) {
      showToastMessage(`🔥 +${highMergeValue}!`)
    }
    
    addRandomTile()
    
    if (merged) {
      updateCombo()
      mergedPositions.forEach(pos => {
        const value = grid.value[pos.row][pos.col]
        addMergeEffect(pos.col, pos.row, value)
      })
      playSound('merge')
    } else {
      playSound('move')
    }
    
    emit('score-update', score.value)
    checkGameState()
    draw()
  } else {
    // Restore state if no movement occurred
    if (history.value.length > 0) {
      const prevState = history.value.pop()
      grid.value = prevState.grid
      score.value = prevState.score
      gameWon.value = prevState.gameWon
    }
    playSound('move', 0.05)
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
  if (!isGameActive.value || gameOver.value) {
    if (e.key === 'r' || e.key === 'R') {
      restart()
    }
    return
  }
  
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
    case 'r':
    case 'R':
      e.preventDefault()
      restart()
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
  
  // Initialize audio context on first interaction
  const initAudio = () => {
    if (!window.audioContext) {
      window.audioContext = new (window.AudioContext || window.webkitAudioContext)()
    }
    document.removeEventListener('click', initAudio)
    document.removeEventListener('touchstart', initAudio)
  }
  document.addEventListener('click', initAudio)
  document.addEventListener('touchstart', initAudio)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (comboTimer.value) {
    clearTimeout(comboTimer.value)
  }
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
  undo,
  score
})
</script>

<style scoped>
.game-2048 {
  position: relative;
  outline: none;
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
}

.game-2048:focus {
  outline: none;
}

.game-canvas {
  border-radius: 15px;
  display: block;
  position: relative;
  z-index: 10;
  transition: transform 0.1s ease;
}

.game-canvas:active {
  transform: scale(0.98);
}

/* 合并特效 */
.merge-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 20;
}

.merge-effect {
  position: absolute;
  font-size: 32px;
  font-weight: bold;
  color: var(--color);
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.8), 0 0 40px var(--color);
  animation: merge-pop 0.8s ease-out forwards;
  white-space: nowrap;
}

@keyframes merge-pop {
  0% { opacity: 0; transform: scale(0) translateY(0); }
  30% { opacity: 1; transform: scale(1.5) translateY(-20px); }
  100% { opacity: 0; transform: scale(1) translateY(-60px); }
}

/* 出現特效 */
.appear-effects {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 15;
}

.appear-effect {
  position: absolute;
  width: var(--size);
  height: var(--size);
  background: rgba(255, 255, 255, 0.6);
  border-radius: 10px;
  animation: appear-pulse 0.5s ease-out forwards;
}

@keyframes appear-pulse {
  0% { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.3); }
}

/* Toast提示 */
.game-toast {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  padding: 15px 30px;
  border-radius: 25px;
  font-size: 1.5rem;
  font-weight: bold;
  z-index: 50;
  animation: toast-fade 1.5s ease-out forwards;
  pointer-events: none;
  text-shadow: 0 0 20px rgba(255, 230, 109, 0.8);
}

@keyframes toast-fade {
  0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
  20% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
  30% { transform: translate(-50%, -50%) scale(1); }
  80% { opacity: 1; }
  100% { opacity: 0; }
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
  border-radius: 15px;
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
  background: rgba(255, 255, 255, 0.95);
  padding: 40px;
  border-radius: 25px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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

.overlay-emoji {
  font-size: 4rem;
  margin-bottom: 10px;
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