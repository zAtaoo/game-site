<template>
  <div v-if="show" class="reward-overlay">
    <!-- 背景闪烁 -->
    <div class="bg-flash"></div>
    
    <!-- 放射光线 -->
    <div class="rays-container">
      <div class="ray" v-for="i in 24" :key="i" :style="{ '--i': i }"></div>
    </div>
    
    <!-- 魔法阵 -->
    <div class="magic-circle">
      <div class="magic-ring ring-outer"></div>
      <div class="magic-ring ring-inner"></div>
      <div class="magic-star"></div>
    </div>
    
    <!-- 星星粒子 -->
    <div class="stars-container">
      <div 
        v-for="star in rewardStars" 
        :key="star.id" 
        class="reward-star"
        :style="{
          left: star.x + '%',
          top: star.y + '%',
          animationDelay: star.delay + 's',
          '--size': star.size + 'px',
          '--color': star.color
        }"
      >{{ star.emoji }}</div>
    </div>
    
    <!-- 火花粒子 -->
    <div class="sparks-container">
      <div 
        v-for="spark in sparks" 
        :key="spark.id" 
        class="spark"
        :style="{
          '--angle': spark.angle + 'deg',
          '--distance': spark.distance + 'px',
          '--delay': spark.delay + 's',
          '--color': spark.color
        }"
      ></div>
    </div>
    
    <!-- 分数弹出 -->
    <div class="score-popup">
      <div class="popup-icon">🎁</div>
      <div class="popup-text">+{{ points }} 分!</div>
      <div class="popup-subtext">超级奖励达成!</div>
      <div class="popup-extra">✨ 继续加油! ✨</div>
    </div>
    
    <!-- 彩带 -->
    <div class="confetti-container">
      <div 
        v-for="confetti in confettiItems" 
        :key="confetti.id" 
        class="confetti"
        :style="{
          left: confetti.x + '%',
          '--color': confetti.color,
          '--delay': confetti.delay + 's',
          '--duration': confetti.duration + 's'
        }"
      ></div>
    </div>
    
    <!-- 冲击波 -->
    <div class="shockwave"></div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  points: { type: Number, default: 500 }
})

const emit = defineEmits(['complete'])

const rewardStars = ref([])
const sparks = ref([])
const confettiItems = ref([])

const starEmojis = ['⭐', '✨', '🌟', '💫', '🌟', '✨', '⭐', '💫', '✨', '⭐']
const starColors = ['#FFD700', '#FF69B4', '#00FFFF', '#FF6347', '#9370DB', '#00FF7F']
const sparkColors = ['#FFD700', '#FF6B9D', '#4ECDC4', '#A855F7', '#FFE66D', '#FF6347']
const confettiColors = ['#FF6B9D', '#C44BE9', '#4ECDC4', '#FFD700', '#FF6347', '#00FFFF']

const generateRewardStars = () => {
  const count = 30
  rewardStars.value = []
  for (let i = 0; i < count; i++) {
    rewardStars.value.push({
      id: i,
      x: 50 + (Math.random() - 0.5) * 80,
      y: 50 + (Math.random() - 0.5) * 80,
      delay: Math.random() * 0.6,
      size: Math.random() * 40 + 25,
      emoji: starEmojis[Math.floor(Math.random() * starEmojis.length)],
      color: starColors[Math.floor(Math.random() * starColors.length)]
    })
  }
}

const generateSparks = () => {
  const count = 40
  sparks.value = []
  for (let i = 0; i < count; i++) {
    sparks.value.push({
      id: i,
      angle: (i / count) * 360,
      distance: Math.random() * 200 + 100,
      delay: Math.random() * 0.3,
      color: sparkColors[Math.floor(Math.random() * sparkColors.length)]
    })
  }
}

const generateConfetti = () => {
  const count = 25
  confettiItems.value = []
  for (let i = 0; i < count; i++) {
    confettiItems.value.push({
      id: i,
      x: Math.random() * 100,
      color: confettiColors[Math.floor(Math.random() * confettiColors.length)],
      delay: Math.random() * 0.5,
      duration: Math.random() * 2 + 2
    })
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    generateRewardStars()
    generateSparks()
    generateConfetti()
    playRewardSound()
    setTimeout(() => {
      emit('complete')
    }, 2500)
  }
})

const playRewardSound = () => {
  if (!window.audioContext) {
    window.audioContext = new (window.AudioContext || window.webkitAudioContext)()
  }
  
  const ctx = window.audioContext
  
  const playNote = (freq, startTime, duration, type = 'sine', volume = 0.1) => {
    const osc = ctx.createOscillator()
    const gain = ctx.createGain()
    
    osc.type = type
    osc.frequency.value = freq
    
    gain.gain.setValueAtTime(volume, startTime)
    gain.gain.exponentialRampToValueAtTime(0.001, startTime + duration)
    
    osc.connect(gain)
    gain.connect(ctx.destination)
    
    osc.start(startTime)
    osc.stop(startTime + duration)
  }
  
  const now = ctx.currentTime
  
  // 开场冲击音
  playNote(150, now, 0.1, 'sawtooth', 0.2)
  
  // 上升音阶 (C5-E5-G5-C6-E6)
  playNote(523.25, now + 0.1, 0.3)
  playNote(659.25, now + 0.2, 0.3)
  playNote(783.99, now + 0.3, 0.4)
  playNote(1046.50, now + 0.45, 0.5)
  playNote(1318.51, now + 0.6, 0.6)
  
  // 和弦共鸣
  setTimeout(() => {
    const t = ctx.currentTime
    playNote(1046.50, t, 0.8, 'sine', 0.08)
    playNote(1318.51, t, 0.8, 'sine', 0.06)
    playNote(1567.98, t, 0.8, 'sine', 0.08)
  }, 500)
  
  // 叮铃声效果
  setTimeout(() => {
    const t = ctx.currentTime
    playNote(2093.00, t, 0.3, 'sine', 0.1)
    playNote(2637.02, t + 0.05, 0.3, 'sine', 0.08)
    playNote(3135.96, t + 0.1, 0.4, 'sine', 0.06)
  }, 800)
  
  // 额外装饰音
  setTimeout(() => {
    const t = ctx.currentTime
    playNote(4186.01, t, 0.5, 'triangle', 0.05)
  }, 1000)
}

onMounted(() => {
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
</script>

<style scoped>
.reward-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 背景闪烁 */
.bg-flash {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.6);
  animation: bg-flash 0.6s ease-out forwards;
}

@keyframes bg-flash {
  0% { opacity: 0; }
  30% { opacity: 1; }
  100% { opacity: 0; }
}

/* 放射光线 */
.rays-container {
  position: absolute;
  width: 500px;
  height: 500px;
}

.ray {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 6px;
  height: 200px;
  background: linear-gradient(to top, var(--color, #FFD700), rgba(255, 255, 255, 0.8), transparent);
  transform-origin: bottom center;
  transform: translate(-50%, -100%) rotate(calc(var(--i) * 15deg));
  animation: ray-expand 1.2s ease-out forwards;
  animation-delay: calc(var(--i) * 0.03s);
  opacity: 0;
  filter: drop-shadow(0 0 10px #FFD700);
}

.ray:nth-child(odd) {
  --color: #FF6B9D;
}

.ray:nth-child(even) {
  --color: #A855F7;
}

@keyframes ray-expand {
  0% { 
    height: 0;
    opacity: 1;
  }
  40% {
    opacity: 1;
  }
  100% { 
    height: 250px;
    opacity: 0;
  }
}

/* 魔法阵 */
.magic-circle {
  position: absolute;
  width: 300px;
  height: 300px;
  animation: magic-pulse 1.5s ease-out forwards;
}

@keyframes magic-pulse {
  0% { transform: scale(0); opacity: 0; }
  30% { transform: scale(1.2); opacity: 1; }
  50% { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(1.5); opacity: 0; }
}

.magic-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  border: 3px solid transparent;
  border-radius: 50%;
}

.ring-outer {
  width: 300px;
  height: 300px;
  transform: translate(-50%, -50%);
  border-top-color: #FF6B9D;
  border-right-color: #A855F7;
  border-bottom-color: #4ECDC4;
  border-left-color: #FFD700;
  animation: ring-rotate 1s linear forwards;
}

.ring-inner {
  width: 200px;
  height: 200px;
  transform: translate(-50%, -50%);
  border-top-color: #4ECDC4;
  border-right-color: #FFD700;
  border-bottom-color: #FF6B9D;
  border-left-color: #A855F7;
  animation: ring-rotate 1s linear reverse forwards;
}

@keyframes ring-rotate {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.magic-star {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80px;
  height: 80px;
  background: radial-gradient(circle, #FFD700 0%, #FF6B9D 50%, transparent 70%);
  clip-path: polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%);
  animation: star-glow 1.2s ease-out forwards;
}

@keyframes star-glow {
  0% { transform: translate(-50%, -50%) scale(0); opacity: 0; filter: blur(0); }
  40% { transform: translate(-50%, -50%) scale(1.5); opacity: 1; filter: blur(5px); }
  100% { transform: translate(-50%, -50%) scale(2); opacity: 0; filter: blur(10px); }
}

/* 星星粒子 */
.stars-container {
  position: absolute;
  width: 100%;
  height: 100%;
}

.reward-star {
  position: absolute;
  font-size: var(--size);
  animation: star-burst 2s ease-out forwards;
  opacity: 0;
  text-shadow: 0 0 10px var(--color), 0 0 20px var(--color);
}

@keyframes star-burst {
  0% {
    opacity: 0;
    transform: scale(0) rotate(0deg) translate(0, 0);
  }
  20% {
    opacity: 1;
    transform: scale(1.8) rotate(180deg) translate(0, -20px);
  }
  50% {
    opacity: 1;
    transform: scale(1) rotate(360deg) translate(0, -40px);
  }
  100% {
    opacity: 0;
    transform: scale(0.3) rotate(720deg) translate(0, -80px);
  }
}

/* 火花粒子 */
.sparks-container {
  position: absolute;
  width: 100%;
  height: 100%;
}

.spark {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 8px;
  height: 8px;
  background: var(--color);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--color), 0 0 20px var(--color);
  animation: spark-fly 1.5s ease-out forwards;
  animation-delay: var(--delay);
}

@keyframes spark-fly {
  0% {
    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(0) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--distance)) scale(0);
    opacity: 0;
  }
}

/* 分数弹出 */
.score-popup {
  position: relative;
  text-align: center;
  animation: popup-appear 2s ease-out forwards;
  z-index: 100;
}

@keyframes popup-appear {
  0% {
    opacity: 0;
    transform: scale(0) translateY(100px);
  }
  25% {
    opacity: 1;
    transform: scale(1.5) translateY(-30px);
  }
  40% {
    transform: scale(1) translateY(0);
  }
  80% {
    opacity: 1;
    transform: scale(1) translateY(-20px);
  }
  100% {
    opacity: 0;
    transform: scale(1.2) translateY(-50px);
  }
}

.popup-icon {
  font-size: 6rem;
  animation: icon-bounce 0.8s ease-out;
  display: block;
}

@keyframes icon-bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}

.popup-text {
  font-size: 5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #FFD700, #FF6B9D, #A855F7, #4ECDC4);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 30px rgba(255, 215, 0, 0.5), 0 0 60px rgba(255, 107, 157, 0.3);
  animation: text-gradient 1.5s ease infinite;
  margin-bottom: 10px;
  display: block;
}

@keyframes text-gradient {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.popup-subtext {
  font-size: 2rem;
  color: #fff;
  text-shadow: 0 0 20px rgba(255, 107, 157, 0.8), 0 0 40px rgba(168, 85, 247, 0.6);
  animation: subtext-glow 1s ease-out;
  display: block;
}

@keyframes subtext-glow {
  0% { opacity: 0; text-shadow: 0 0 0 transparent; }
  50% { opacity: 1; text-shadow: 0 0 30px rgba(255, 107, 157, 1); }
  100% { opacity: 1; text-shadow: 0 0 20px rgba(255, 107, 157, 0.8); }
}

.popup-extra {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin-top: 10px;
  animation: extra-fade 0.5s ease-out 0.5s forwards;
  opacity: 0;
  display: block;
}

@keyframes extra-fade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 彩带 */
.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.confetti {
  position: absolute;
  top: -20px;
  width: 12px;
  height: 12px;
  background: var(--color);
  animation: confetti-fall var(--duration) ease-in-out infinite;
  animation-delay: var(--delay);
}

@keyframes confetti-fall {
  0% {
    transform: translateY(0) rotate(0deg) scale(1);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(720deg) scale(0.5);
    opacity: 0;
  }
}

/* 冲击波 */
.shockwave {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 215, 0, 0.8);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: shockwave-expand 1.5s ease-out forwards;
}

@keyframes shockwave-expand {
  0% {
    width: 20px;
    height: 20px;
    opacity: 1;
    border-width: 3px;
  }
  100% {
    width: 800px;
    height: 800px;
    opacity: 0;
    border-width: 1px;
  }
}
</style>