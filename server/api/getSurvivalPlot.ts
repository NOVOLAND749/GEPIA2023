export default defineEventHandler(async (event) => {
  const { gene, datasets, high, low } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase +
      `/survival_analysis/${gene}/${datasets
        ?.toString()
        .replaceAll(",", "&")}/${high == null ? 50.0 : high}&${
        low == null ? 50.0 : low
      }/`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
