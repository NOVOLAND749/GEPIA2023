import GeneDetailType from "~/types/GeneDetailType";

export default defineEventHandler(async (event) => {
  const geneName = event.context.params!.geneName;
  const { apiBase } = useRuntimeConfig();
  return await $fetch<GeneDetailType>(apiBase + `/gene_info/${geneName}`);
});
