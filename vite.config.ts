import tailwindcss from '@tailwindcss/vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import {defineConfig} from 'vite';

export default defineConfig(() => {
  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
    },
    build: {
      rollupOptions: {
        input: {
          main: path.resolve(__dirname, 'index.html'),
          craftMatch: path.resolve(__dirname, 'craft-match.html'),
          potionMix: path.resolve(__dirname, 'potion-mix.html'),
          runaMaster: path.resolve(__dirname, 'runa-master.html'),
          portalArcano: path.resolve(__dirname, 'portal-arcano.html'),
          aetherRoyale: path.resolve(__dirname, 'aether-royale.html')
        }
      }
    },
    server: {
      hmr: process.env.DISABLE_HMR !== 'true',
      watch: process.env.DISABLE_HMR === 'true' ? null : {},
    },
  };
});
