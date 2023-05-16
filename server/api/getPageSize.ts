export default defineEventHandler(async () => {
  const { apiBase } = useRuntimeConfig();
  return await $fetch<number>(apiBase + "/global_variable/PAGE_SIZE/");
});
