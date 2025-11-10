/* eslint-disable import/order */
import '@/@iconify/icons-bundle';
import App from '@/App.vue';
import layoutsPlugin from '@/plugins/layouts';
import vuetify from '@/plugins/vuetify';
import { loadFonts } from '@/plugins/webfontloader';
import router from '@/router';
import '@core/scss/template/index.scss';
import '@styles/styles.scss';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue';
import 'vue3-perfect-scrollbar/dist/vue3-perfect-scrollbar.css';
loadFonts()


// Create vue app
const app = createApp(App)

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// Use plugins
app.use(vuetify)
app.use(pinia)
app.use(router)
app.use(layoutsPlugin)

// Mount vue app
app.mount('#app')
