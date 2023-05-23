export default defineEventHandler(async (event) => {
  const geneName = event.context.params!.geneName;
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(apiBase + `/cnv/bar_plot/${geneName}/`);
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
