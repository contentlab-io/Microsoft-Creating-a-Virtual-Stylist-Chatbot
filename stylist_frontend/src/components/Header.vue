<template>
    <div class="header">
      <img src="/images/logo.svg" alt="Logo" class="logo" />
      <h1 class="title">Virtual Stylist Chatbot</h1>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "Header",
  });
  </script>
  
  <style scoped>
  .header {
    @apply flex items-center justify-center bg-gray-100 p-4;
  }
  
  .logo {
    @apply w-12 h-12 mr-4;
  }
  
  .title {
    @apply text-2xl font-bold text-gray-800;
  }
  </style>
  