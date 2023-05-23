export default defineEventHandler(async (event) => {
  const geneName = event.context.params!.geneName;
  const datasetsSelection = event.context.params!.datasetsSelection;
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase + `/box_plot/${geneName}/${datasetsSelection}`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
