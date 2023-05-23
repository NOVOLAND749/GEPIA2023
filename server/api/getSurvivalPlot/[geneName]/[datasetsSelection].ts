export default defineEventHandler(async (event) => {
  const geneName = event.context.params!.geneName;
  const datasetsSelection = event.context.params!.datasetsSelection;
  const { CutoffHigh, CutoffLow } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  const blob = await $fetch<Blob>(
    apiBase +
      `/survival_analysis/${geneName}/${datasetsSelection}/?High_cutoff=${
        CutoffHigh == null ? 100.0 : CutoffHigh
      }&Low_cutoff=${CutoffLow == null ? 0.0 : CutoffLow}`
  );
  const arrayBuffer = blob.arrayBuffer();
  const buffer = Buffer.from(await arrayBuffer);
  return buffer;
});
