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
              v-model="geneSearchTerm"
            >
              <template #prefix>
                <Icon name="🔎"></Icon>
              </template>
            </Input>
            <ListGroup class="w-full" v-if="geneSearchResults && !isExactMatch">
              <ListGroupItem
                v-for="term in geneSearchResults"
                @click="geneSearchTerm = term.item.gene_name"
              >
                <b>
                  {{ term.item.gene_name }}
                </b>
                - {{ term.item.ENSEMBL }}
              </ListGroupItem>
            </ListGroup>
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

const activeTab = ref("first");
const { data: genes } = await useLazyFetch("/api/getGeneList");

const geneSearch = new Fuse(genes.value || [], {
  keys: ["gene_name", "ENSEMBL"],
});
const geneSearchTerm = ref("");
const geneSearchResults = computed(() => {
  if (geneSearchTerm.value == "") return [];
  return geneSearch.search(geneSearchTerm.value);
});
const isExactMatch = computed(() => {
  return (
    geneSearchResults.value.length != 0 &&
    geneSearchTerm.value == geneSearchResults.value[0].item.gene_name
  );
});
</script>
