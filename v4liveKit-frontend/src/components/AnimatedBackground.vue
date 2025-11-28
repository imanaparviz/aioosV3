<template>
  <div class="animated-bg">
    <!-- Floating Orbs -->
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
    <div class="orb orb-5"></div>

    <!-- Subtle grid (optional) -->
    <div class="grid-overlay"></div>
  </div>
</template>

<script setup>
// Pure CSS - super fast performance!
</script>

<style scoped>
.animated-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
}

/* Very subtle grid */
.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(139, 92, 246, 0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139, 92, 246, 0.015) 1px, transparent 1px);
  background-size: 80px 80px;
  pointer-events: none;
}

/* Orb base style */
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.2;
  will-change: transform;
  mix-blend-mode: multiply;
  pointer-events: none;
}

/* Cyan orb - top right */
.orb-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle at center, #22D3EE 0%, #06B6D4 25%, transparent 55%);
  top: -12%;
  right: -8%;
  animation: float1 30s ease-in-out infinite;
}

/* Purple orb - bottom left */
.orb-2 {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle at center, #A78BFA 0%, #8B5CF6 25%, transparent 55%);
  bottom: -18%;
  left: -12%;
  animation: float2 35s ease-in-out infinite;
}

/* Pink orb - middle right */
.orb-3 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle at center, #F472B6 0%, #EC4899 25%, transparent 55%);
  top: 40%;
  right: -10%;
  animation: float3 25s ease-in-out infinite;
}

/* Peach/Orange orb - top left */
.orb-4 {
  width: 550px;
  height: 550px;
  background: radial-gradient(circle at center, #FDBA74 0%, #FB923C 25%, transparent 55%);
  top: 8%;
  left: 10%;
  animation: float4 28s ease-in-out infinite;
}

/* Small cyan orb - bottom center */
.orb-5 {
  width: 450px;
  height: 450px;
  background: radial-gradient(circle at center, #67E8F9 0%, #22D3EE 25%, transparent 55%);
  bottom: 12%;
  left: 48%;
  animation: float5 23s ease-in-out infinite;
}

/* Smooth animations */
@keyframes float1 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(-40px, 50px) scale(1.05);
  }
  50% {
    transform: translate(-70px, 30px) scale(0.95);
  }
  75% {
    transform: translate(-30px, 70px) scale(1.02);
  }
}

@keyframes float2 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(50px, -40px) scale(1.08);
  }
  50% {
    transform: translate(30px, -60px) scale(0.92);
  }
  75% {
    transform: translate(60px, -30px) scale(1.04);
  }
}

@keyframes float3 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(-50px, -40px) scale(1.06);
  }
  66% {
    transform: translate(-30px, 50px) scale(0.94);
  }
}

@keyframes float4 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(40px, 40px) scale(0.96);
  }
  50% {
    transform: translate(60px, -30px) scale(1.04);
  }
  75% {
    transform: translate(30px, 50px) scale(1);
  }
}

@keyframes float5 {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(-50px, -50px) scale(1.1);
  }
}

/* Mobile optimization */
@media (max-width: 768px) {
  .orb {
    filter: blur(70px);
    opacity: 0.18;
  }

  .orb-1, .orb-2 {
    width: 400px;
    height: 400px;
  }

  .orb-3, .orb-4, .orb-5 {
    width: 300px;
    height: 300px;
  }
}

/* Accessibility - reduce motion */
@media (prefers-reduced-motion: reduce) {
  .orb {
    animation: none;
  }
}
</style>
