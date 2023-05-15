export default defineEventHandler(async (event) => {
  const collectionName = event.context.params!.collectionName;
  const { apiBase } = useRuntimeConfig();
  return await $fetch(apiBase + `/datasets/${collectionName}`);
});
