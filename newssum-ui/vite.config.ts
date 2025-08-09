import { defineConfig } from 'vite';
import Components from 'unplugin-vue-components/vite'
import {BootstrapVueNextResolver} from 'bootstrap-vue-next'
import vue from '@vitejs/plugin-vue';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
    Components({
      resolvers: [BootstrapVueNextResolver()],
    }),
  ],
  define: {
    'import.meta.env.DEV': process.env.NODE_ENV !== 'production',
  },
});
