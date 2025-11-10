<script setup>
import novagios from '@images/novagios.png'
</script>

<template>
  <div class="h-100 d-flex align-center justify-space-between">
    <!-- 👉 Footer: left content -->
    <span class="d-flex align-center">
      &copy;
      {{ new Date().getFullYear() }}
      Made
      By <a
        href="https://novagios.com/"
        target="_blank"
        rel="noopener noreferrer"
        class="text-primary ms-1"
      ><v-img
          :width="80"
          aspect-ratio="16/9"
          cover
          :src="novagios"
        ></v-img></a>
    </span>
    <!-- 👉 Footer: right content -->
  </div>
</template>
