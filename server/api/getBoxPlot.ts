export default defineEventHandler(async (event) => {
  const { gene, datasets } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase + `/box_plot/${gene}/${datasets?.toString().replaceAll(",", "&")}/`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
