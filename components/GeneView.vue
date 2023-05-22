<template>
  <div>
    <Input
      placeholder="Enter a gene name, e.g. ERBB2"
      label="Search for a gene"
      v-model.trim="geneSearchTerm"
      @input="updateSearchResults"
    >
      <template #prefix>
        <Icon
          name="material-symbols:search"
          class="transform -scale-x-100"
        ></Icon>
      </template>
    </Input>
    <div
      v-if="geneSearchResults && !isExactMatch"
      class="pt-2 w-full max-h-60 overflow-scroll"
    >
      <ListGroup class="w-full">
        <ListGroupItem
          v-for="term in geneSearchResults"
          @click="selectSuggestion(term)"
        >
          {{ term }}
        </ListGroupItem>
      </ListGroup>
    </div>
    <div v-if="isExactMatch" class="pt-2 px-2">
      <GeneDetail :gene-name="geneSearchTerm"></GeneDetail>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ListGroup, ListGroupItem, Input } from "flowbite-vue";
import Fuse from "fuse.js";

const route = useRoute();
const router = useRouter();

const geneStore = useGeneStore();
const genes = ref(geneStore.geneList);

const geneSearch = new Fuse(genes.value || [], { threshold: 0.3 });
const geneSearchTerm = ref(
  route.query.gene ? (route.query.gene as string) : ""
);
const geneSearchResults = ref([] as string[]);
const isExactMatch = ref(route.query.gene ? true : false);
const searchTimeout = ref(0 as number | ReturnType<typeof setTimeout>);

const selectSuggestion = (gene: string) => {
  geneSearchTerm.value = gene;
  geneSearchResults.value = [];
  isExactMatch.value = true;
  router.push({ query: { gene: gene } });
};
const updateSearchResults = () => {
  clearTimeout(searchTimeout.value);
  searchTimeout.value = setTimeout(() => {
    if (geneSearchTerm.value) {
      geneSearchResults.value = geneSearch
        .search(geneSearchTerm.value)
        .map((r) => r.item);
      isExactMatch.value = geneSearchResults.value[0] === geneSearchTerm.value;
    } else {
      geneSearchResults.value = [];
      isExactMatch.value = false;
    }
  }, 500);
};

onBeforeMount(async () => {
  if (!genes.value.length) {
    if (!geneStore.geneList.length) {
      await geneStore.load();
    }
    genes.value = geneStore.geneList;
    geneSearch.setCollection(genes.value);
  }
});
</script>
