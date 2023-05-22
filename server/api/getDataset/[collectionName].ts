import DatasetType from "~/types/DatasetType";

export default defineEventHandler(async (event) => {
  const collectionName = event.context.params!.collectionName;
  const { apiBase } = useRuntimeConfig();
  return await $fetch<DatasetType>(apiBase + `/datasets/${collectionName}/`);
});
