<template>
  <div class="space-background" :class="currentPhase">
    <!-- Canvas 背景层 -->
    <canvas ref="canvasRef" class="space-canvas"></canvas>
    
    <!-- 阶段标题提示 -->
    <div class="phase-indicator" v-if="showPhaseTransition">
      <div class="phase-badge" :style="{ background: phaseColors[phase].gradient }">
        <span class="phase-icon">{{ phaseIcons[phase] }}</span>
        <span class="phase-text">{{ phaseNames[phase] }}</span>
      </div>
    </div>
    
    <!-- 过渡闪光 -->
    <div class="transition-flash" v-if="showFlash"></div>
  </div>
</template>

<script setup>import { ref, watch, onMounted, onUnmounted, defineProps, defineEmits } from 'vue';
const props = defineProps({
 score: { type: Number, default: 0 }
});
const emit = defineEmits(['phase-change']);
const canvasRef = ref(null);
const currentPhase = ref('earth');
const showPhaseTransition = ref(false);
const showFlash = ref(false);
const animationId = ref(null);
const stars = ref([]);
const planets = ref([]);
const nebulas = ref([]);
const galaxies = ref([]);
const clouds = ref([]);
const phaseIcons = {
 earth: '🌍',
 solar: '☀️',
 galaxy: '🌌',
 universe: '🔭'
};
const phaseNames = {
 earth: '地球',
 solar: '太阳系',
 galaxy: '银河系',
 universe: '宇宙'
};
const phaseColors = {
 earth: {
 bg: '#0a1628',
 gradient: 'linear-gradient(135deg, #006994, #003366)',
 accent: '#4ECDC4',
 planet: '#2E86DE'
 },
 solar: {
 bg: '#050a14',
 gradient: 'linear-gradient(135deg, #FFD700, #FF6B35)',
 accent: '#FFD700',
 planet: '#FFD700'
 },
 galaxy: {
 bg: '#020512',
 gradient: 'linear-gradient(135deg, #A855F7, #667eea)',
 accent: '#A855F7',
 planet: '#A855F7'
 },
 universe: {
 bg: '#000000',
 gradient: 'linear-gradient(135deg, #FF6B9D, #A855F7, #4ECDC4)',
 accent: '#FF6B9D',
 planet: '#FF6B9D'
 }
};
const getPhase = (score) => {
 if (score >= 2000)
 return 'universe';
 if (score >= 1500)
 return 'galaxy';
 if (score >= 1000)
 return 'solar';
 return 'earth';
};
const initStars = (count = 100) => {
 stars.value = [];
 for (let i = 0; i < count; i++) {
 stars.value.push({
 x: Math.random() * 100,
 y: Math.random() * 100,
 size: Math.random() * 3 + 1,
 opacity: Math.random() * 0.8 + 0.2,
 twinkleSpeed: Math.random() * 2 + 1,
 twinkleOffset: Math.random() * Math.PI * 2
 });
 }
};
const initPlanets = () => {
 planets.value = [];
 const planetConfigs = [
 { radius: 20, speed: 0.5, color: '#FFD700', orbitRadius: 100, angle: 0 },
 { radius: 15, speed: 0.8, color: '#C0C0C0', orbitRadius: 150, angle: Math.PI / 4 },
 { radius: 18, speed: 1.2, color: '#FF6B35', orbitRadius: 200, angle: Math.PI / 2 },
 { radius: 12, speed: 1.5, color: '#4ECDC4', orbitRadius: 250, angle: 3 * Math.PI / 4 },
 { radius: 8, speed: 1.8, color: '#FFE66D', orbitRadius: 300, angle: Math.PI }
 ];
 planetConfigs.forEach((config, i) => {
 planets.value.push({
 ...config,
 x: 50,
 y: 50,
 id: i
 });
 });
};
const initNebulas = () => {
 nebulas.value = [];
 const colors = ['rgba(168, 85, 247, 0.2)', 'rgba(255, 107, 157, 0.15)', 'rgba(78, 205, 196, 0.15)', 'rgba(255, 230, 109, 0.1)'];
 for (let i = 0; i < 5; i++) {
 nebulas.value.push({
 x: Math.random() * 100,
 y: Math.random() * 100,
 width: Math.random() * 200 + 150,
 height: Math.random() * 100 + 80,
 color: colors[i % colors.length],
 rotation: Math.random() * Math.PI * 2,
 rotationSpeed: (Math.random() - 0.5) * 0.002,
 opacity: Math.random() * 0.3 + 0.2,
 pulseSpeed: Math.random() * 0.003 + 0.001
 });
 }
};
const initGalaxies = () => {
 galaxies.value = [];
 for (let i = 0; i < 8; i++) {
 galaxies.value.push({
 x: Math.random() * 100,
 y: Math.random() * 100,
 radius: Math.random() * 80 + 50,
 arms: Math.floor(Math.random() * 3) + 2,
 color: `rgba(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255}, 0.3)`,
 rotation: Math.random() * Math.PI * 2,
 rotationSpeed: (Math.random() - 0.5) * 0.001,
 stars: []
 });
 galaxies.value[i].stars = Array(Math.floor(Math.random() * 50) + 30).fill(null).map(() => ({
 angle: Math.random() * Math.PI * 2,
 radius: Math.random() * galaxies.value[i].radius * 0.8,
 size: Math.random() * 2 + 0.5,
 opacity: Math.random() * 0.6 + 0.2
 }));
 }
};
const initClouds = () => {
 clouds.value = [];
 for (let i = 0; i < 10; i++) {
 clouds.value.push({
 x: Math.random() * 100,
 y: Math.random() * 100,
 width: Math.random() * 150 + 100,
 height: Math.random() * 40 + 30,
 speed: Math.random() * 0.02 + 0.01,
 opacity: Math.random() * 0.3 + 0.1,
 offset: Math.random() * Math.PI * 2
 });
 }
};
const playPhaseSound = (phase) => {
 if (!window.audioContext) {
 window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
 }
 const ctx = window.audioContext;
 const now = ctx.currentTime;
 const notes = {
 earth: [261.63, 329.63, 392.00],
 solar: [329.63, 440.00, 523.25],
 galaxy: [440.00, 587.33, 698.46],
 universe: [523.25, 659.25, 783.99, 1046.50]
 };
 notes[phase].forEach((freq, i) => {
 const osc = ctx.createOscillator();
 const gain = ctx.createGain();
 osc.type = 'sine';
 osc.frequency.value = freq;
 gain.gain.setValueAtTime(0, now + i * 0.1);
 gain.gain.linearRampToValueAtTime(0.1, now + i * 0.1 + 0.05);
 gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.5);
 osc.connect(gain);
 gain.connect(ctx.destination);
 osc.start(now + i * 0.1);
 osc.stop(now + i * 0.1 + 0.5);
 });
};
const drawEarth = (ctx, width, height, time) => {
 const centerX = width * 0.8;
 const centerY = height * 0.3;
 const radius = Math.min(width, height) * 0.15;
 ctx.save();
 ctx.beginPath();
 ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
 const gradient = ctx.createRadialGradient(centerX - radius * 0.3, centerY - radius * 0.3, 0, centerX, centerY, radius);
 gradient.addColorStop(0, '#6EC6FF');
 gradient.addColorStop(0.4, '#006994');
 gradient.addColorStop(0.7, '#003366');
 gradient.addColorStop(1, '#001a33');
 ctx.fillStyle = gradient;
 ctx.fill();
 ctx.beginPath();
 ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
 ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
 ctx.lineWidth = 2;
 ctx.stroke();
 for (let i = 0; i < 5; i++) {
 ctx.beginPath();
 ctx.arc(centerX, centerY, radius * (0.3 + i * 0.15), 0, Math.PI * 2);
 ctx.strokeStyle = `rgba(255, 255, 255, ${0.05 - i * 0.008})`;
 ctx.stroke();
 }
 clouds.value.forEach(cloud => {
 const x = ((cloud.x + time * cloud.speed * 50) % 100) / 100 * width;
 const y = ((cloud.y + Math.sin(time * cloud.speed * 2 + cloud.offset) * 10) / 100) * height;
 const opacity = cloud.opacity + Math.sin(time * cloud.pulseSpeed * 1000) * 0.05;
 ctx.beginPath();
 ctx.ellipse(x, y, cloud.width / 2, cloud.height / 2, 0, 0, Math.PI * 2);
 ctx.fillStyle = `rgba(255, 255, 255, ${opacity})`;
 ctx.fill();
 });
 const glowRadius = radius * 1.5;
 const glowGradient = ctx.createRadialGradient(centerX, centerY, radius, centerX, centerY, glowRadius);
 glowGradient.addColorStop(0, 'rgba(78, 205, 196, 0.3)');
 glowGradient.addColorStop(0.5, 'rgba(0, 105, 148, 0.1)');
 glowGradient.addColorStop(1, 'transparent');
 ctx.fillStyle = glowGradient;
 ctx.beginPath();
 ctx.arc(centerX, centerY, glowRadius, 0, Math.PI * 2);
 ctx.fill();
 ctx.restore();
};
const drawSolarSystem = (ctx, width, height, time) => {
 const centerX = width / 2;
 const centerY = height / 2;
 const scale = Math.min(width, height) / 800;
 ctx.save();
 const sunGlow = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, 100 * scale);
 sunGlow.addColorStop(0, 'rgba(255, 215, 0, 0.8)');
 sunGlow.addColorStop(0.3, 'rgba(255, 170, 0, 0.4)');
 sunGlow.addColorStop(0.6, 'rgba(255, 107, 53, 0.2)');
 sunGlow.addColorStop(1, 'transparent');
 ctx.fillStyle = sunGlow;
 ctx.beginPath();
 ctx.arc(centerX, centerY, 100 * scale, 0, Math.PI * 2);
 ctx.fill();
 const sunGradient = ctx.createRadialGradient(centerX - 15 * scale, centerY - 15 * scale, 0, centerX, centerY, 40 * scale);
 sunGradient.addColorStop(0, '#FFFACD');
 sunGradient.addColorStop(0.5, '#FFD700');
 sunGradient.addColorStop(1, '#FF6B35');
 ctx.fillStyle = sunGradient;
 ctx.beginPath();
 ctx.arc(centerX, centerY, 40 * scale, 0, Math.PI * 2);
 ctx.fill();
 ctx.shadowColor = '#FFD700';
 ctx.shadowBlur = 30;
 ctx.fillStyle = '#FFD700';
 ctx.beginPath();
 ctx.arc(centerX, centerY, 40 * scale, 0, Math.PI * 2);
 ctx.fill();
 ctx.shadowBlur = 0;
 planets.value.forEach(planet => {
 const angle = planet.angle + time * planet.speed * 0.05;
 const px = centerX + Math.cos(angle) * planet.orbitRadius * scale;
 const py = centerY + Math.sin(angle) * planet.orbitRadius * scale;
 ctx.beginPath();
 ctx.arc(centerX, centerY, planet.orbitRadius * scale, 0, Math.PI * 2);
 ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
 ctx.lineWidth = 1;
 ctx.stroke();
 ctx.beginPath();
 ctx.arc(px, py, planet.radius * scale * 0.6, 0, Math.PI * 2);
 const planetGradient = ctx.createRadialGradient(px - planet.radius * scale * 0.2, py - planet.radius * scale * 0.2, 0, px, py, planet.radius * scale * 0.6);
 planetGradient.addColorStop(0, '#ffffff');
 planetGradient.addColorStop(0.3, planet.color);
 planetGradient.addColorStop(1, '#333');
 ctx.fillStyle = planetGradient;
 ctx.fill();
 });
 ctx.restore();
};
const drawGalaxy = (ctx, width, height, time) => {
 ctx.save();
 nebulas.value.forEach(nebula => {
 nebula.rotation += nebula.rotationSpeed;
 const opacity = nebula.opacity + Math.sin(time * 1000 * nebula.pulseSpeed) * 0.1;
 ctx.save();
 ctx.translate((nebula.x / 100) * width, (nebula.y / 100) * height);
 ctx.rotate(nebula.rotation);
 ctx.beginPath();
 ctx.ellipse(0, 0, nebula.width / 2, nebula.height / 2, 0, 0, Math.PI * 2);
 ctx.fillStyle = nebula.color.replace('0.15', opacity.toString()).replace('0.2', opacity.toString()).replace('0.1', opacity.toString());
 ctx.fill();
 ctx.restore();
 });
 galaxies.value.forEach(galaxy => {
 galaxy.rotation += galaxy.rotationSpeed;
 const cx = (galaxy.x / 100) * width;
 const cy = (galaxy.y / 100) * height;
 ctx.save();
 ctx.translate(cx, cy);
 ctx.rotate(galaxy.rotation);
 galaxy.stars.forEach(star => {
 const starAngle = star.angle + galaxy.rotation;
 const sx = Math.cos(starAngle) * star.radius * (Math.min(width, height) / 1000);
 const sy = Math.sin(starAngle) * star.radius * (Math.min(width, height) / 1000);
 const twinkle = Math.sin(time * 2 + starAngle) * 0.3 + 0.7;
 ctx.beginPath();
 ctx.arc(sx, sy, star.size * (Math.min(width, height) / 1000), 0, Math.PI * 2);
 ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity * twinkle})`;
 ctx.fill();
 });
 const coreGlow = ctx.createRadialGradient(0, 0, 0, 0, 0, galaxy.radius * 0.2 * (Math.min(width, height) / 1000));
 coreGlow.addColorStop(0, 'rgba(255, 255, 255, 0.5)');
 coreGlow.addColorStop(0.5, galaxy.color);
 coreGlow.addColorStop(1, 'transparent');
 ctx.fillStyle = coreGlow;
 ctx.beginPath();
 ctx.arc(0, 0, galaxy.radius * 0.2 * (Math.min(width, height) / 1000), 0, Math.PI * 2);
 ctx.fill();
 ctx.restore();
 });
 ctx.restore();
};
const drawUniverse = (ctx, width, height, time) => {
 ctx.save();
 galaxies.value.forEach(galaxy => {
 galaxy.rotation += galaxy.rotationSpeed * 0.5;
 const cx = (galaxy.x / 100) * width;
 const cy = (galaxy.y / 100) * height;
 const sizeScale = 0.5 + Math.sin(time * 0.5 + galaxy.x) * 0.2;
 ctx.save();
 ctx.translate(cx, cy);
 ctx.rotate(galaxy.rotation);
 ctx.scale(sizeScale, sizeScale);
 galaxy.stars.forEach(star => {
 const starAngle = star.angle + galaxy.rotation * 2;
 const sx = Math.cos(starAngle) * star.radius * (Math.min(width, height) / 1200);
 const sy = Math.sin(starAngle) * star.radius * (Math.min(width, height) / 1200);
 const twinkle = Math.sin(time * 3 + starAngle * 2) * 0.4 + 0.6;
 const colors = ['#ffffff', '#FFD700', '#FF6B9D', '#A855F7', '#4ECDC4'];
 const color = colors[Math.floor(starAngle * 10) % colors.length];
 ctx.beginPath();
 ctx.arc(sx, sy, star.size * (Math.min(width, height) / 1200), 0, Math.PI * 2);
 ctx.fillStyle = color;
 ctx.shadowColor = color;
 ctx.shadowBlur = star.size * 2;
 ctx.fill();
 ctx.shadowBlur = 0;
 });
 ctx.restore();
 });
 for (let i = 0; i < 3; i++) {
 const x = ((time * 20 + i * 300) % width);
 const y = height * 0.3 + Math.sin(time * 0.5 + i) * height * 0.2;
 const trailLength = 150;
 const gradient = ctx.createLinearGradient(x - trailLength, y, x, y);
 gradient.addColorStop(0, 'transparent');
 gradient.addColorStop(0.7, 'rgba(255, 255, 255, 0.3)');
 gradient.addColorStop(1, 'rgba(255, 255, 255, 0.8)');
 ctx.strokeStyle = gradient;
 ctx.lineWidth = 2;
 ctx.beginPath();
 ctx.moveTo(x - trailLength, y);
 ctx.lineTo(x, y);
 ctx.stroke();
 ctx.beginPath();
 ctx.arc(x, y, 3, 0, Math.PI * 2);
 ctx.fillStyle = '#ffffff';
 ctx.fill();
 }
 ctx.restore();
};
const drawStars = (ctx, width, height, time) => {
 stars.value.forEach(star => {
 const twinkle = Math.sin(time * star.twinkleSpeed + star.twinkleOffset) * 0.3 + 0.7;
 const x = (star.x / 100) * width;
 const y = (star.y / 100) * height;
 ctx.beginPath();
 ctx.arc(x, y, star.size, 0, Math.PI * 2);
 ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity * twinkle})`;
 ctx.fill();
 if (star.size > 2) {
 ctx.shadowColor = '#ffffff';
 ctx.shadowBlur = star.size * 3;
 ctx.fill();
 ctx.shadowBlur = 0;
 }
 });
};
const drawBackground = (ctx, width, height) => {
 ctx.fillStyle = phaseColors[currentPhase.value].bg;
 ctx.fillRect(0, 0, width, height);
};
const animate = () => {
 const canvas = canvasRef.value;
 if (!canvas)
 return;
 const ctx = canvas.getContext('2d');
 const width = canvas.width;
 const height = canvas.height;
 const time = Date.now() * 0.001;
 drawBackground(ctx, width, height);
 drawStars(ctx, width, height, time);
 switch (currentPhase.value) {
 case 'earth':
 drawEarth(ctx, width, height, time);
 break;
 case 'solar':
 drawSolarSystem(ctx, width, height, time);
 break;
 case 'galaxy':
 drawGalaxy(ctx, width, height, time);
 break;
 case 'universe':
 drawUniverse(ctx, width, height, time);
 break;
 }
 animationId.value = requestAnimationFrame(animate);
};
const handleResize = () => {
 const canvas = canvasRef.value;
 if (!canvas)
 return;
 canvas.width = window.innerWidth;
 canvas.height = window.innerHeight;
};
const triggerPhaseTransition = (newPhase) => {
 showFlash.value = true;
 setTimeout(() => {
 showFlash.value = false;
 currentPhase.value = newPhase;
 showPhaseTransition.value = true;
 playPhaseSound(newPhase);
 emit('phase-change', newPhase);
 setTimeout(() => {
 showPhaseTransition.value = false;
 }, 2000);
 }, 300);
};
watch(() => props.score, (newScore) => {
 const newPhase = getPhase(newScore);
 if (newPhase !== currentPhase.value) {
 triggerPhaseTransition(newPhase);
 }
});
onMounted(() => {
 const canvas = canvasRef.value;
 if (!canvas)
 return;
 canvas.width = window.innerWidth;
 canvas.height = window.innerHeight;
 initStars(150);
 initPlanets();
 initNebulas();
 initGalaxies();
 initClouds();
 currentPhase.value = getPhase(props.score);
 animate();
 window.addEventListener('resize', handleResize);
});
onUnmounted(() => {
 if (animationId.value) {
 cancelAnimationFrame(animationId.value);
 }
 window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.space-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
  transition: background-color 1s ease;
}

.space-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* 阶段指示器 */
.phase-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  animation: phase-appear 2s ease-out forwards;
}

@keyframes phase-appear {
  0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
  20% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
  30% { transform: translate(-50%, -50%) scale(1); }
  80% { opacity: 1; }
  100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
}

.phase-badge {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px 40px;
  border-radius: 50px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.phase-icon {
  font-size: 3rem;
  animation: icon-bounce 0.5s ease-out;
}

@keyframes icon-bounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}

.phase-text {
  font-size: 2rem;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
}

/* 过渡闪光 */
.transition-flash {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  animation: flash-fade 0.3s ease-out forwards;
  pointer-events: none;
}

@keyframes flash-fade {
  0% { opacity: 1; }
  100% { opacity: 0; }
}

/* 各阶段主题样式 */
.space-background.earth {
  background: linear-gradient(135deg, #0a1628 0%, #003366 50%, #0a1628 100%);
}

.space-background.solar {
  background: linear-gradient(135deg, #050a14 0%, #1a1000 50%, #050a14 100%);
}

.space-background.galaxy {
  background: linear-gradient(135deg, #020512 0%, #1a0a2e 50%, #020512 100%);
}

.space-background.universe {
  background: linear-gradient(135deg, #000000 0%, #0a0515 50%, #000000 100%);
}
</style>