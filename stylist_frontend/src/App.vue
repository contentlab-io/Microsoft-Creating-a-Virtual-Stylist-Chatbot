<template>
  <div class="app">
    <Header></Header>
    <div class="main">
      <ChatWindow ref="chat" />
      
    </div>
    <Footer />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
import ChatWindow from "./components/ChatWindow.vue";
import ImageUploadButton from "./components/ImageUploadButton.vue";

export default defineComponent({
  name: "App",
  components: {
    Header,
    Footer,
    ChatWindow,
    ImageUploadButton,
  },
  setup() {
    // Define a ref for the chat component
    const chat: any = ref(null);
    // Return the ref
    return {
      chat,
    };
  },
});
</script>

<style>
.app {
  @apply min-h-screen flex flex-col;
}

.main {
  @apply flex-1 flex flex-col;
}
</style>
