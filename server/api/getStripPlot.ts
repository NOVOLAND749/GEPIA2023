export default defineEventHandler(async (event) => {
  const { gene } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(apiBase + `/gene_plot/strip/${gene}/`);
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
