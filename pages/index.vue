<template>
  <div>
    <Head>
      <Title>GEPIA 2023 - Home</Title>
    </Head>
    <div class="max-w-4xl mx-auto pt-4 px-4">
      <h1 class="py-8 text-3xl text-center text-gray-600 font-bold mx-auto">
        GEPIA 2023
      </h1>
      <Tabs v-model="activeTab" variant="underline">
        <Tab name="first" title="Gene view">
          <div class="py-2">
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
            <div v-if="geneDetail" class="pt-2 px-2">
              <GeneDetail :gene="geneDetail"></GeneDetail>
            </div>
            <div v-else-if="isExactMatch" class="w-full mx-auto pt-3">
              <Spinner size="12" color="white" />
            </div>
          </div>
        </Tab>
      </Tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Spinner,
  ListGroup,
  ListGroupItem,
  Tab,
  Tabs,
  Input,
} from "flowbite-vue";
import Fuse from "fuse.js";
import GeneDetailType from "~/types/GeneDetailType";

const route = useRoute();
const router = useRouter();

const activeTab = ref("first");
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

const geneDetail = ref(null as GeneDetailType | null);

watch(isExactMatch, async (isExactMatch) => {
  if (isExactMatch) {
    geneDetail.value = null;
    if (geneSearchTerm.value) {
      geneDetail.value = await $fetch(
        `/api/getGeneDetail/${geneSearchTerm.value}`
      );
    }
  }
});

onBeforeMount(async () => {
  if (!genes.value.length) {
    if (!geneStore.geneList.length) {
      await geneStore.loadFromLocalStorage();
    }
    genes.value = geneStore.geneList;
    geneSearch.setCollection(genes.value);
  }

  if (isExactMatch.value) {
    geneDetail.value = null;
    if (geneSearchTerm.value) {
      geneDetail.value = await $fetch(
        `/api/getGeneDetail/${geneSearchTerm.value}`
      );
    }
  }
});
</script>
