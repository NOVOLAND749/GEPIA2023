export default defineEventHandler(async (event) => {
  const { dataset } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(apiBase + `/cell_prop/${dataset}/`);
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
