import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue({
    template: {
      compilerOptions: {
        isCustomElement: tagName => tagName === 'vue-advanced-chat' || tagName === 'emoji-picker',
        isTS: true
      }
    }
  })]
})
