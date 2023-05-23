export default defineEventHandler(async (event) => {
  const { genes, datasets } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase +
      `/pca/visual/${datasets?.toString().replaceAll(",", "&")}/${genes
        ?.toString()
        .replaceAll(",", "&")}/`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
