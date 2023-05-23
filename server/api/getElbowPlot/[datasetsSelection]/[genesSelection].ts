export default defineEventHandler(async (event) => {
  const genesSelection = event.context.params!.genesSelection;
  const datasetsSelection = event.context.params!.datasetsSelection;
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase + `/pca/elbow_plot/${datasetsSelection}/${genesSelection}/`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
