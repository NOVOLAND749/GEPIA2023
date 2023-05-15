<template>
  <div>
    <div class="max-w-4xl mx-auto pt-4">
      <h1 class="py-8 text-3xl text-center text-gray-600 font-bold mx-auto">
        GEPIA 2023
      </h1>
      <Tabs v-model="activeTab" variant="underline">
        <Tab name="first" title="View genes">
          <div class="py-2">
            <Input
              placeholder="enter gene name or ENSEMBL ID"
              label="Gene name"
              v-model.trim="geneSearchTerm"
              @input="updateSearchResults"
            >
              <template #prefix>
                <Icon name="🔎"></Icon>
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
            <div v-if="isExactMatch">This will be the detail of a gene</div>
          </div>
        </Tab>
      </Tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Dropdown,
  ListGroup,
  ListGroupItem,
  Tab,
  Tabs,
  Input,
} from "flowbite-vue";
import Fuse from "fuse.js";
import GeneDetailType from "~/types/GeneDetailType";

const activeTab = ref("first");
const totalPageNum = await useLazyFetch("/api/getPageSize");
const { data: genes } = await useLazyFetch("/api/getGeneList");

const geneSearch = new Fuse(genes.value || [], { threshold: 0.3 });
const geneSearchTerm = ref("");
const geneSearchResults = ref([] as string[]);
const isExactMatch = ref(false);
const searchTimeout = ref(0 as number | ReturnType<typeof setTimeout>);

const selectSuggestion = (gene: string) => {
  geneSearchTerm.value = gene;
  geneSearchResults.value = [];
  isExactMatch.value = true;
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
</script>
