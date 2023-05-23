export default defineEventHandler(async (event) => {
  const datasetName = event.context.params!.datasetName;
  const { genes } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase +
      `/cnv/venn_plot/${datasetName}/${genes?.toString().split(",").join("&")}`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
