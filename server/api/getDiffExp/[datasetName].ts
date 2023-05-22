import DiffExpType from "~/types/DiffExpType";

export default defineEventHandler(async (event) => {
  const datasetName = event.context.params!.datasetName;
  const { log2FC, qValue } = getQuery(event);
  const { apiBase } = useRuntimeConfig();
  return await $fetch<DiffExpType[]>(
    apiBase +
      `/differential_genes/${datasetName}/?Log2FC=${log2FC || 1}&p_adj=${
        qValue || 0.05
      }`
  );
});
