export default defineEventHandler(async () => {
  const { apiBase } = useRuntimeConfig();
  return await $fetch<string[]>(apiBase + "/gene_info");
});
