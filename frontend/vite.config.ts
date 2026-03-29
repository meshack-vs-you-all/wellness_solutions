import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, '.', 'VITE_');
  const isWordPressBuild = mode === 'wordpress';

  return {
    plugins: [react()],
    base: env.VITE_APP_BASE || (isWordPressBuild ? './' : '/'),
    build: {
      outDir:
        env.VITE_BUILD_OUT_DIR ||
        (isWordPressBuild
          ? '../wordpress/wp-content/themes/wellness-solutions/assets/app'
          : 'dist'),
      emptyOutDir: true,
      manifest: isWordPressBuild,
    },
    server: {
      host: true,
      port: 5173,
      open: !isWordPressBuild,
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, '.'),
      },
      extensions: ['.ts', '.tsx', '.js', '.jsx'],
    },
  };
});
