import GeneInfoType from "~/types/GeneInfoType";

export default defineEventHandler(async () => {
  const { apiBase } = useRuntimeConfig();
  return await $fetch<GeneInfoType[]>(apiBase + "/gene_info");
});
