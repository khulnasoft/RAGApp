import { resolve } from 'path';
import { defineConfig } from 'vite';

export default defineConfig({
    build: {
        lib: {
            entry: resolve(__dirname, 'src/index.js'),
            name: 'Gantt',
            fileName: 'ragapp-gantt',
        },
        rollupOptions: {
            output: {
                format: 'cjs',
                assetFileNames: 'ragapp-gantt[extname]',
                entryFileNames: 'ragapp-gantt.[format].js'
            },
        },
    },
    output: { interop: 'auto' },
    server: { watch: { include: ['dist/*', 'src/*'] } }
});