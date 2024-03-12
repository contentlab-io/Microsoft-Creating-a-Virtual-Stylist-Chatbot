<template>
    <div class="footer">
      <p class="info">
        This app is part of a tutorial series on creating a virtual stylist chatbot using Azure and OpenAI. You can find the tutorial and the code on
        <a href="https://example.com/tutorial" class="link" target="_blank"
          >this website</a
        >.
      </p>
      <p class="info">
        The app uses Azure Functions, Azure Cognitive Services, and GPT-4 Vision on Azure OpenAI to analyze images and generate natural language responses and recommendations. The app also uses Vite, Vue, TypeScript, Tailwind CSS, and vue-advanced-chat to create the chatbot interface.
      </p>
      <p class="info">
        The images used in the app are from the
        <a
          href="https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small"
          class="link"
          target="_blank"
          >Fashion Product Images Dataset</a
        >
        by Param Aggarwal on Kaggle.
      </p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "Footer",
  });
  </script>
  
  <style scoped>
  .footer {
    @apply bg-gray-100 p-4;
  }
  
  .info {
    @apply text-sm text-gray-800 mb-2;
  }
  
  .link {
    @apply text-blue-600 underline;
  }
  </style>
  