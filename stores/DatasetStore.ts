import DatasetType from "~/types/DatasetType";

export const useDatasetStore = defineStore("DatasetStore", () => {
  const datasetList = ref([] as DatasetType[]);

  function saveToLocalStorage() {
    localStorage.setItem("datasetList", JSON.stringify(datasetList.value));
  }

  function loadFromLocalStorage() {
    const data = localStorage.getItem("datasetList");
    if (data) {
      datasetList.value = JSON.parse(data);
    }
  }

  async function load() {
    if (datasetList.value.length) return;
    loadFromLocalStorage();
    if (!datasetList.value.length) {
      const result = await $fetch("/api/getDataset");
      if (result) {
        datasetList.value = result;
        saveToLocalStorage();
      }
    }
  }

  return { datasetList, load };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useDatasetStore, import.meta.hot));
}
