export default defineEventHandler(async (event) => {
  const datasetName = event.context.params!.datasetName;
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(apiBase + `/cell_prop/${datasetName}/`);
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
