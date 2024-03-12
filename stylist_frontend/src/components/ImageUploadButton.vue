<template>
    <div class="image-upload-button">
      <label for="image-upload" class="label">
        <img src="/images/camera.svg" alt="Camera" class="icon" />
        Upload an image
      </label>
      <input
        type="file"
        id="image-upload"
        class="input"
        accept="image/*"
        @change="onFileChange"
      />
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import ChatWindow from "./ChatWindow.vue";
  
  export default defineComponent({
    name: "ImageUploadButton",
    props: {
      chat: {
        type: ChatWindow,
        required: true,
      },
    },
    setup(props) {
      // Define the function to handle the file change event
      const onFileChange = (event: Event) => {
        // Get the file object from the event target
        const file = (event.target as HTMLInputElement).files?.[0];
        if (file) {
          // Call the onFileUpload method of the chat component with the file object
          props.chat.onFileUpload(file);
        }
      };
  
      // Return the event handler
      return {
        onFileChange,
      };
    },
  });
  </script>
  
  <style scoped>
  .image-upload-button {
    @apply flex items-center justify-center bg-gray-100 p-4;
  }
  
  .label {
    @apply flex items-center cursor-pointer;
  }
  
  .icon {
    @apply w-6 h-6 mr-2;
  }
  
  .input {
    @apply hidden;
  }
  </style>