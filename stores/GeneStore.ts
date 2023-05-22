export const useGeneStore = defineStore("GeneStore", () => {
  const geneList = ref([] as string[]);

  function saveToLocalStorage() {
    localStorage.setItem("geneList", JSON.stringify(geneList.value));
  }

  function loadFromLocalStorage() {
    const data = localStorage.getItem("geneList");
    if (data) {
      geneList.value = JSON.parse(data);
    }
  }

  async function load() {
    if (geneList.value.length) return;
    loadFromLocalStorage();
    if (!geneList.value.length) {
      const result = await $fetch("/api/getGeneList");
      if (result) {
        geneList.value = result;
        saveToLocalStorage();
      }
    }
  }

  return { geneList, load };
});

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useGeneStore, import.meta.hot));
}
