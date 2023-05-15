import DiseaseAbbrType from "~/types/DiseaseAbbrType";

export default defineEventHandler(async () => {
  const { apiBase } = useRuntimeConfig();
  return await $fetch<DiseaseAbbrType[]>(apiBase + "/disease_abbr");
});
