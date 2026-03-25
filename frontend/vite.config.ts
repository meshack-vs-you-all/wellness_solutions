import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', 'VITE_');
    return {
      plugins: [react()],
      define: {
        // Only expose VITE_ prefixed variables to the client
        // This prevents accidental exposure of sensitive data
      },
      server: {
        host: true, // Allow access from network devices
        port: 5173,
        open: true,
      },
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        },
        extensions: ['.ts', '.tsx', '.js', '.jsx'],
      }
    };
});
