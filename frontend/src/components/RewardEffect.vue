<template>
  <div v-if="show" class="reward-overlay" :class="rewardTheme">
    <!-- 奖励特效GIF背景 -->
    <div class="reward-gif-bg">
      <img :src="currentRewardGif" alt="reward effect" class="gif-bg" />
    </div>
    
    <!-- 背景闪烁 -->
    <div class="bg-flash"></div>
    
    <!-- 放射光线 -->
    <div class="rays-container">
      <div class="ray" v-for="i in rayCount" :key="i" :style="{ '--i': i, '--color': rayColors[i % rayColors.length] }"></div>
    </div>
    
    <!-- 魔法阵 -->
    <div class="magic-circle">
      <div class="magic-ring ring-outer"></div>
      <div class="magic-ring ring-inner"></div>
      <div class="magic-star" :style="{ '--star-color': themeColors.primary }"></div>
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
      <div class="popup-icon">{{ rewardIcon }}</div>
      <div class="popup-text" :style="{ background: textGradient }">+{{ points }} 分!</div>
      <div class="popup-subtext">{{ rewardTitle }}</div>
      <div class="popup-extra">{{ rewardExtra }}</div>
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
    <div class="shockwave" :style="{ '--wave-color': themeColors.secondary }"></div>
    
    <!-- 进阶特效：分数 >= 1500 -->
    <div v-if="scoreLevel >= 2" class="advanced-effects">
      <!-- 流星 -->
      <div class="meteor" v-for="i in meteorCount" :key="'m'+i" :style="{ '--i': i }"></div>
      <!-- 光圈扩散 -->
      <div class="ring-expand" v-for="i in 3" :key="'r'+i" :style="{ '--i': i }"></div>
    </div>
    
    <!-- 高级特效：分数 >= 2500 -->
    <div v-if="scoreLevel >= 3" class="elite-effects">
      <!-- 能量球 -->
      <div class="energy-orbs">
        <div class="energy-orb" v-for="i in 8" :key="'e'+i" :style="{ '--i': i }"></div>
      </div>
      <!-- 彩虹桥 -->
      <div class="rainbow-bridge"></div>
    </div>
    
    <!-- 终极特效：分数 >= 5000 -->
    <div v-if="scoreLevel >= 4" class="ultimate-effects">
      <!-- 黑洞 -->
      <div class="blackhole"></div>
      <!-- 量子粒子 -->
      <div class="quantum-particles">
        <div class="quantum-particle" v-for="i in 50" :key="'q'+i" :style="{ '--i': i }"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

const props = defineProps({
  show: { type: Boolean, default: false },
  points: { type: Number, default: 500 },
  currentScore: { type: Number, default: 0 }
})

const emit = defineEmits(['complete'])

const rewardStars = ref([])
const sparks = ref([])
const confettiItems = ref([])
const currentRewardGif = ref('')

const rewardGifUrls = [
  'https://s1.aigei.com/src/img/gif/f3/f3dacc343d6742f5b9eb2d7496b8907b.gif?e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:mOkCSWIgt0A6g5BlUzsq82ANp-A=',
  'https://s1.aigei.com/src/img/gif/83/83ea016dc8f54ee7b8c97d10f20aa5e8.gif?imageMogr2/auto-orient/thumbnail/!282x282r/gravity/Center/crop/282x282/quality/85/%7CimageView2/2/w/282&e=2051020800&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:lrf3WZxviyO1Cz8cx66CXL229JE='
]

const rewardThemes = [
  {
    name: 'basic',
    icon: '�',
    title: '奖励达成!',
    extra: '继续加油!',
    rayColors: ['#FFD700', '#FF6B9D'],
    themeColors: { primary: '#FFD700', secondary: '#FF6B9D' },
    rayCount: 12,
    meteorCount: 0
  },
  {
    name: 'advanced',
    icon: '✨',
    title: '超级奖励!',
    extra: '太厉害了!',
    rayColors: ['#00FFFF', '#FF6B9D', '#A855F7'],
    themeColors: { primary: '#00FFFF', secondary: '#A855F7' },
    rayCount: 18,
    meteorCount: 5
  },
  {
    name: 'elite',
    icon: '🌟',
    title: '精英奖励!',
    extra: '你是游戏大师!',
    rayColors: ['#FFD700', '#FF6B9D', '#00FFFF', '#A855F7', '#4ECDC4'],
    themeColors: { primary: '#FFD700', secondary: '#C44BE9' },
    rayCount: 24,
    meteorCount: 8
  },
  {
    name: 'ultimate',
    icon: '👑',
    title: '传说奖励!',
    extra: '你是传奇!',
    rayColors: ['#FFD700', '#FF6B9D', '#00FFFF', '#A855F7', '#4ECDC4', '#FF6347'],
    themeColors: { primary: '#FFD700', secondary: '#FF6347' },
    rayCount: 36,
    meteorCount: 12
  }
]

const scoreLevel = computed(() => {
  const score = props.currentScore
  if (score >= 5000) return 3
  if (score >= 2500) return 2
  if (score >= 1500) return 1
  return 0
})

const rewardTheme = computed(() => rewardThemes[scoreLevel.value].name)
const rewardIcon = computed(() => rewardThemes[scoreLevel.value].icon)
const rewardTitle = computed(() => rewardThemes[scoreLevel.value].title)
const rewardExtra = computed(() => rewardThemes[scoreLevel.value].extra)
const rayColors = computed(() => rewardThemes[scoreLevel.value].rayColors)
const rayCount = computed(() => rewardThemes[scoreLevel.value].rayCount)
const meteorCount = computed(() => rewardThemes[scoreLevel.value].meteorCount)
const themeColors = computed(() => rewardThemes[scoreLevel.value].themeColors)

const textGradient = computed(() => {
  const colors = rayColors.value.join(', ')
  return `linear-gradient(135deg, ${colors})`
})

const starEmojis = ['⭐', '✨', '🌟', '💫', '🌟', '✨', '⭐', '💫', '✨', '⭐']

const generateRewardStars = () => {
  const count = 20 + scoreLevel.value * 10
  rewardStars.value = []
  for (let i = 0; i < count; i++) {
    rewardStars.value.push({
      id: i,
      x: 50 + (Math.random() - 0.5) * 80,
      y: 50 + (Math.random() - 0.5) * 80,
      delay: Math.random() * 0.6,
      size: Math.random() * 40 + 25,
      emoji: starEmojis[Math.floor(Math.random() * starEmojis.length)],
      color: rayColors.value[Math.floor(Math.random() * rayColors.value.length)]
    })
  }
}

const generateSparks = () => {
  const count = 30 + scoreLevel.value * 15
  sparks.value = []
  for (let i = 0; i < count; i++) {
    sparks.value.push({
      id: i,
      angle: (i / count) * 360,
      distance: Math.random() * 200 + 100,
      delay: Math.random() * 0.3,
      color: rayColors.value[Math.floor(Math.random() * rayColors.value.length)]
    })
  }
}

const generateConfetti = () => {
  const count = 20 + scoreLevel.value * 10
  confettiItems.value = []
  for (let i = 0; i < count; i++) {
    confettiItems.value.push({
      id: i,
      x: Math.random() * 100,
      color: rayColors.value[Math.floor(Math.random() * rayColors.value.length)],
      delay: Math.random() * 0.5,
      duration: Math.random() * 2 + 2
    })
  }
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    currentRewardGif.value = rewardGifUrls[Math.floor(Math.random() * rewardGifUrls.length)]
    generateRewardStars()
    generateSparks()
    generateConfetti()
    playRewardSound()
    setTimeout(() => {
      emit('complete')
    }, 3000)
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
  const level = scoreLevel.value
  
  // 开场冲击音
  playNote(150, now, 0.1, 'sawtooth', 0.2)
  
  // 上升音阶
  if (level >= 3) {
    // 终极版：七音阶
    playNote(523.25, now + 0.1, 0.3)
    playNote(659.25, now + 0.18, 0.3)
    playNote(783.99, now + 0.26, 0.3)
    playNote(880, now + 0.34, 0.3)
    playNote(1046.50, now + 0.42, 0.4)
    playNote(1174.66, now + 0.5, 0.4)
    playNote(1318.51, now + 0.58, 0.5)
  } else if (level >= 2) {
    // 精英版：五音阶
    playNote(523.25, now + 0.1, 0.3)
    playNote(659.25, now + 0.2, 0.3)
    playNote(783.99, now + 0.3, 0.4)
    playNote(1046.50, now + 0.45, 0.5)
    playNote(1318.51, now + 0.6, 0.6)
  } else if (level >= 1) {
    // 进阶版：四音阶
    playNote(523.25, now + 0.1, 0.3)
    playNote(659.25, now + 0.2, 0.3)
    playNote(783.99, now + 0.3, 0.4)
    playNote(1046.50, now + 0.45, 0.5)
  } else {
    // 基础版：三音阶
    playNote(523.25, now + 0.1, 0.3)
    playNote(659.25, now + 0.2, 0.3)
    playNote(783.99, now + 0.3, 0.4)
  }
  
  // 和弦共鸣
  setTimeout(() => {
    const t = ctx.currentTime
    playNote(1046.50, t, 0.8, 'sine', 0.08)
    playNote(1318.51, t, 0.8, 'sine', 0.06)
    playNote(1567.98, t, 0.8, 'sine', 0.08)
  }, 500 + level * 100)
  
  // 叮铃声效果
  setTimeout(() => {
    const t = ctx.currentTime
    playNote(2093.00, t, 0.3, 'sine', 0.1)
    playNote(2637.02, t + 0.05, 0.3, 'sine', 0.08)
    playNote(3135.96, t + 0.1, 0.4, 'sine', 0.06)
  }, 800 + level * 150)
  
  // 终极版额外音效
  if (level >= 3) {
    setTimeout(() => {
      const t = ctx.currentTime
      playNote(4186.01, t, 0.5, 'triangle', 0.05)
      playNote(5232.51, t + 0.1, 0.6, 'sine', 0.04)
    }, 1200)
  }
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

/* 奖励特效GIF背景 */
.reward-gif-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.gif-bg {
  width: 100%;
  height: 100%;
  object-fit: cover;
  animation: gif-pulse 3s ease-in-out infinite;
}

@keyframes gif-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
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
  transform: translate(-50%, -100%) rotate(calc(var(--i) * (360 / var(--ray-count, 12)) * 1deg));
  animation: ray-expand 1.2s ease-out forwards;
  animation-delay: calc(var(--i) * 0.03s);
  opacity: 0;
  filter: drop-shadow(0 0 10px var(--color));
}

@keyframes ray-expand {
  0% { height: 0; opacity: 1; }
  40% { opacity: 1; }
  100% { height: 250px; opacity: 0; }
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
  background: radial-gradient(circle, var(--star-color, #FFD700) 0%, #FF6B9D 50%, transparent 70%);
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
  0% { opacity: 0; transform: scale(0) rotate(0deg) translate(0, 0); }
  20% { opacity: 1; transform: scale(1.8) rotate(180deg) translate(0, -20px); }
  50% { opacity: 1; transform: scale(1) rotate(360deg) translate(0, -40px); }
  100% { opacity: 0; transform: scale(0.3) rotate(720deg) translate(0, -80px); }
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
  0% { transform: translate(-50%, -50%) rotate(var(--angle)) translateX(0) scale(1); opacity: 1; }
  100% { transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--distance)) scale(0); opacity: 0; }
}

/* 分数弹出 */
.score-popup {
  position: relative;
  text-align: center;
  animation: popup-appear 2.5s ease-out forwards;
  z-index: 100;
}

@keyframes popup-appear {
  0% { opacity: 0; transform: scale(0) translateY(100px); }
  25% { opacity: 1; transform: scale(1.5) translateY(-30px); }
  40% { transform: scale(1) translateY(0); }
  80% { opacity: 1; transform: scale(1) translateY(-20px); }
  100% { opacity: 0; transform: scale(1.2) translateY(-50px); }
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
  0%, 100% { filter: brightness(1); }
  50% { filter: brightness(1.2); }
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
  0% { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg) scale(0.5); opacity: 0; }
}

/* 冲击波 */
.shockwave {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border: 3px solid var(--wave-color, #FFD700);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: shockwave-expand 1.5s ease-out forwards;
}

@keyframes shockwave-expand {
  0% { width: 20px; height: 20px; opacity: 1; border-width: 3px; }
  100% { width: 800px; height: 800px; opacity: 0; border-width: 1px; }
}

/* 进阶特效 */
.advanced-effects {
  position: absolute;
  width: 100%;
  height: 100%;
}

.meteor {
  position: absolute;
  top: -50px;
  left: calc(var(--i) * 15%);
  width: 4px;
  height: 60px;
  background: linear-gradient(to bottom, transparent, #FFD700, #FF6B9D);
  transform: rotate(45deg);
  animation: meteor-fly 1s ease-out forwards;
  animation-delay: calc(var(--i) * 0.15s);
  opacity: 0;
}

@keyframes meteor-fly {
  0% { opacity: 0; transform: rotate(45deg) translateX(-100px); }
  20% { opacity: 1; }
  100% { opacity: 0; transform: rotate(45deg) translateX(300px) translateY(300px); }
}

.ring-expand {
  position: absolute;
  top: 50%;
  left: 50%;
  border: 2px solid rgba(0, 255, 255, 0.6);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ring-expand-anim 1s ease-out forwards;
  animation-delay: calc(var(--i) * 0.2s);
}

@keyframes ring-expand-anim {
  0% { width: 50px; height: 50px; opacity: 1; }
  100% { width: 400px; height: 400px; opacity: 0; }
}

/* 高级特效 */
.elite-effects {
  position: absolute;
  width: 100%;
  height: 100%;
}

.energy-orbs {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 300px;
  height: 300px;
  transform: translate(-50%, -50%);
}

.energy-orb {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  background: radial-gradient(circle, #FFD700, #C44BE9);
  border-radius: 50%;
  transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg)) translateX(100px);
  animation: orb-orbit 1s ease-out forwards;
  animation-delay: calc(var(--i) * 0.05s);
}

@keyframes orb-orbit {
  0% { opacity: 0; transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg)) translateX(50px); }
  50% { opacity: 1; }
  100% { opacity: 0; transform: translate(-50%, -50%) rotate(calc(var(--i) * 45deg + 360deg)) translateX(150px); }
}

.rainbow-bridge {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 400px;
  height: 200px;
  background: linear-gradient(90deg, #FF6B9D, #FFD700, #4ECDC4, #A855F7, #FF6B9D);
  transform: translate(-50%, -50%) rotate(90deg);
  clip-path: ellipse(50% 30% at 50% 50%);
  animation: rainbow-pulse 0.8s ease-out forwards;
  opacity: 0;
}

@keyframes rainbow-pulse {
  0% { opacity: 0; transform: translate(-50%, -50%) rotate(90deg) scale(0.5); }
  50% { opacity: 0.6; }
  100% { opacity: 0; transform: translate(-50%, -50%) rotate(90deg) scale(1.5); }
}

/* 终极特效 */
.ultimate-effects {
  position: absolute;
  width: 100%;
  height: 100%;
}

.blackhole {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, #000 0%, #1a0033 30%, #330066 60%, transparent 80%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: blackhole-pulse 1.5s ease-out forwards;
}

@keyframes blackhole-pulse {
  0% { opacity: 0; transform: translate(-50%, -50%) scale(0); }
  30% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
  100% { opacity: 0; transform: translate(-50%, -50%) scale(2); }
}

.quantum-particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.quantum-particle {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 6px;
  height: 6px;
  background: #00FFFF;
  border-radius: 50%;
  animation: quantum-fly 1.2s ease-out forwards;
  animation-delay: calc(var(--i) * 0.02s);
}

@keyframes quantum-fly {
  0% { opacity: 0; transform: translate(-50%, -50%) scale(0); }
  20% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  100% { 
    opacity: 0; 
    transform: translate(-50%, -50%) 
      translateX(cos(var(--i) * 7.2deg) * 300px)
      translateY(sin(var(--i) * 7.2deg) * 300px)
      scale(0); 
  }
}
</style>