import SimilarGeneType from "~/types/SimilarGeneType";

export default defineEventHandler(async (event) => {
  const geneName = event.context.params!.geneName;
  const { apiBase } = useRuntimeConfig();
  return await $fetch<SimilarGeneType[]>(
    apiBase + `/similar_genes/${geneName}/`
  );
});
