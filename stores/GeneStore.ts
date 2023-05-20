export const useGeneStore = defineStore("GeneStore", () => {
  const geneList = ref([] as string[]);

  function saveToLocalStorage() {
    localStorage.setItem("geneList", JSON.stringify(geneList.value));
  }

  async function loadFromLocalStorage() {
    const data = localStorage.getItem("geneList");
    if (data) {
      geneList.value = JSON.parse(data);
    } else {
      const result = await $fetch("/api/getGeneList");
      if (result) {
        geneList.value = result;
        saveToLocalStorage();
      }
    }
  }

  return { geneList, saveToLocalStorage, loadFromLocalStorage };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useGeneStore, import.meta.hot));
}