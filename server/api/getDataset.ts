import DatasetType from "~/types/DatasetType";

export default defineEventHandler(async () => {
  const { apiBase } = useRuntimeConfig();
  return await $fetch<DatasetType[]>(apiBase + "/datasets/");
});
