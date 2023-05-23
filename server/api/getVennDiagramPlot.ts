export default defineEventHandler(async (event) => {
  const { genes, dataset } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase +
      `/cnv/venn_plot/${dataset}/${genes?.toString().split(",").join("&")}`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
