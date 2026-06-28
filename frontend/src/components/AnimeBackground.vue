<template>
  <div class="anime-background">
    <!-- 渐变背景层 -->
    <div class="gradient-layer"></div>
    
    <!-- 星空层 -->
    <div class="stars-layer">
      <div 
        v-for="star in stars" 
        :key="star.id" 
        class="star"
        :style="{
          left: star.x + '%',
          top: star.y + '%',
          width: star.size + 'px',
          height: star.size + 'px',
          animationDelay: star.delay + 's',
          animationDuration: star.duration + 's'
        }"
      ></div>
    </div>
    
    <!-- 樱花层 -->
    <div class="sakura-layer">
      <div 
        v-for="petal in sakuraPetals" 
        :key="petal.id" 
        class="sakura-petal"
        :style="{
          left: petal.x + '%',
          top: petal.y + '%',
          animationDelay: petal.delay + 's',
          animationDuration: petal.duration + 's',
          opacity: petal.opacity
        }"
      ></div>
    </div>
    
    <!-- 速度线层 -->
    <div class="speedlines-layer">
      <div class="speedline" v-for="i in 8" :key="i" :style="{ '--i': i }"></div>
    </div>
    
    <!-- 魔法圆环层 -->
    <div class="magic-rings">
      <div class="magic-ring ring-1"></div>
      <div class="magic-ring ring-2"></div>
      <div class="magic-ring ring-3"></div>
    </div>
    
    <!-- 光晕层 -->
    <div class="glow-orbs">
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const stars = ref([])
const sakuraPetals = ref([])

const generateStars = () => {
  const starCount = 80
  for (let i = 0; i < starCount; i++) {
    stars.value.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 3 + 1,
      delay: Math.random() * 5,
      duration: Math.random() * 3 + 2
    })
  }
}

const generateSakura = () => {
  const petalCount = 30
  for (let i = 0; i < petalCount; i++) {
    sakuraPetals.value.push({
      id: i,
      x: Math.random() * 100,
      y: Math.random() * -100,
      delay: Math.random() * 10,
      duration: Math.random() * 10 + 15,
      opacity: Math.random() * 0.5 + 0.3
    })
  }
}

onMounted(() => {
  generateStars()
  generateSakura()
})
</script>

<style scoped>
.anime-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

/* 渐变背景 */
.gradient-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    #0a0a1a 0%,
    #1a1a3a 25%,
    #2a1a4a 50%,
    #1a1a3a 75%,
    #0a0a1a 100%
  );
}

/* 星空层 */
.stars-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.star {
  position: absolute;
  background: #fff;
  border-radius: 50%;
  box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #a855f7;
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.3; transform: scale(0.8); }
}

/* 樱花层 */
.sakura-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.sakura-petal {
  position: absolute;
  width: 12px;
  height: 12px;
  background: radial-gradient(circle, #ffb7c5 0%, #ff69b4 50%, transparent 100%);
  border-radius: 50% 0 50% 50%;
  animation: fall 15s linear infinite;
}

@keyframes fall {
  0% {
    transform: translateY(-100px) rotate(0deg) translateX(0);
    opacity: 1;
  }
  25% {
    transform: translateY(25vh) rotate(90deg) translateX(50px);
  }
  50% {
    transform: translateY(50vh) rotate(180deg) translateX(-30px);
  }
  75% {
    transform: translateY(75vh) rotate(270deg) translateX(40px);
  }
  100% {
    transform: translateY(110vh) rotate(360deg) translateX(-20px);
    opacity: 0;
  }
}

/* 速度线层 */
.speedlines-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.speedline {
  position: absolute;
  width: 2px;
  height: 100%;
  background: linear-gradient(
    to bottom,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
  left: calc(var(--i) * 12.5%);
  animation: speedline 4s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.3s);
}

@keyframes speedline {
  0%, 100% { opacity: 0; transform: translateY(-100%); }
  50% { opacity: 0.5; transform: translateY(200%); }
}

/* 魔法圆环层 */
.magic-rings {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  pointer-events: none;
}

.magic-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid transparent;
  border-radius: 50%;
}

.ring-1 {
  width: 400px;
  height: 400px;
  border-top-color: rgba(168, 85, 247, 0.3);
  border-right-color: rgba(255, 107, 157, 0.3);
  animation: rotate-ring 20s linear infinite;
}

.ring-2 {
  width: 500px;
  height: 500px;
  border-bottom-color: rgba(78, 205, 196, 0.3);
  border-left-color: rgba(255, 230, 109, 0.3);
  animation: rotate-ring 25s linear infinite reverse;
}

.ring-3 {
  width: 600px;
  height: 600px;
  border-top-color: rgba(255, 107, 157, 0.2);
  border-bottom-color: rgba(168, 85, 247, 0.2);
  animation: rotate-ring 30s linear infinite;
}

@keyframes rotate-ring {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

/* 光晕球层 */
.glow-orbs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: orb-float 15s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #ff6b9d, transparent);
  top: 10%;
  right: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 250px;
  height: 250px;
  background: radial-gradient(circle, #a855f7, transparent);
  bottom: 20%;
  left: 10%;
  animation-delay: -5s;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, #4ecdc4, transparent);
  top: 50%;
  right: 30%;
  animation-delay: -10s;
}

@keyframes orb-float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(30px, -30px) scale(1.1); }
  50% { transform: translate(-20px, 20px) scale(0.9); }
  75% { transform: translate(20px, 10px) scale(1.05); }
}
</style>