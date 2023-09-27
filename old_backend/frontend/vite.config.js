import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
    build: {
        // generate manifest.json in outDir
        watch: "./templates",
        manifest: true,
        outDir: "../static/dist",
        publicDir: './assets',
        rollupOptions: {
            input: {
                layout: resolve(__dirname, 'templates/layout.html'),
                index: resolve(__dirname, 'templates/index.html'),
                upload: resolve(__dirname, 'templates/upload.html'),
                dashboard: resolve(__dirname, 'templates/dashboard.html'),
                tables: resolve(__dirname, 'templates/tables.html'),
                signup: resolve(__dirname, 'templates/signup.html'),
                login: resolve(__dirname, 'templates/login.html'),
                sth: resolve(__dirname, 'templates/sth.html'),
                404: resolve(__dirname, 'templates/404.html'),
                400: resolve(__dirname, 'templates/400.html'),
                test_view: resolve(__dirname, 'templates/test_view.html'),
                flash_message: resolve(__dirname, 'templates/components/flash_message.html'),
                table: resolve(__dirname, 'templates/htmx_response/table.html'),
                validate_form: resolve(__dirname, 'templates/htmx_response/validate_form.html'),
            }
        },
    },
})