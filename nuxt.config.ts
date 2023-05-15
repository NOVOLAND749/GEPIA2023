// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    "@nuxtjs/tailwindcss",
    ["@pinia/nuxt", { autoImports: ["defineStore", "acceptHMRUpdate"] }],
    "nuxt-icon",
  ],
  imports: {
    dirs: ["stores"],
  },
  runtimeConfig: {
    apiBase: process.env.API_BASE_URL,
  },
});
