<template>
  <div>
    <p class="text-sm py-2 font-medium">
      Selected 2 ~ 3 genes (click to remove)
    </p>
    <div class="flex-grow">
      <div class="h-10 rounded-md border flex flex-row">
        <Button
          v-for="gg in geneList"
          color="alternative"
          @click="geneList = geneList.filter((g) => g != gg)"
        >
          {{ gg }}
        </Button>
      </div>
    </div>
    <Input
      placeholder="Enter a gene name, e.g. ERBB2"
      label="Gene name to get survival plot"
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

    <p class="text-sm py-2 font-medium">Dataset:</p>
    <div class="flex flex-row">
      <Dropdown placement="bottom">
        <template #trigger="{ toggle }">
          <Button @click="toggle" color="alternative">
            {{ datasetSelection ? datasetSelection.db_name : "Choose one" }}
          </Button>
        </template>
        <ListGroup class="max-h-60 overflow-y-scroll">
          <ListGroupItem v-for="ds in datasets" @click="datasetSelection = ds">
            {{ ds.db_name }}
          </ListGroupItem>
        </ListGroup>
      </Dropdown>
      <div>
        <Button @click="generatePlotLink" class="h-10">Go!</Button>
      </div>
    </div>

    <div class="pt-2 px-2">
      <PlotCard
        v-if="plotLink"
        :title="`Copy number variance overlap of ${geneList.join(', ')} in ${datasetSelection!.db_name}`"
        description=""
        :imageUrl="plotLink"
        :key="plotLink"
        class="mt-4"
      />
    </div>

    <Teleport to="body">
      <div class="absolute top-20 right-0 flex flex-col gap-2 m-2">
        <Toast
          v-for="toast in toastList"
          :type="toast.type"
          class="border shadow-md"
        >
          {{ toast.message }}
        </Toast>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import {
  ListGroup,
  ListGroupItem,
  Input,
  Dropdown,
  Button,
  Toast,
} from "flowbite-vue";
import Fuse from "fuse.js";
import { ToastType } from "flowbite-vue/dist_types/components/Toast/types";
import DatasetType from "~/types/DatasetType";

const toastList = ref([] as { type: ToastType; message: string }[]);
const toastProvider = (
  toast: { type: ToastType; message: string },
  timeout: number = 3000
) => {
  toastList.value.push(toast);
  setTimeout(() => {
    toastList.value.shift();
  }, timeout);
};

const geneStore = useGeneStore();
const genes = ref(geneStore.geneList);
const geneList = ref([] as string[]);

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
watch(isExactMatch, (isExactMatch) => {
  if (isExactMatch) {
    if (geneList.value.includes(geneSearchTerm.value)) {
      toastProvider(
        {
          type: "warning",
          message: "Gene already in list",
        },
        1000
      );
    } else if (geneList.value.length >= 3) {
      toastProvider(
        {
          type: "warning",
          message: "You can only select up to 3 genes",
        },
        1000
      );
    } else {
      geneList.value.push(geneSearchTerm.value);
      geneSearchTerm.value = "";
    }
  }
});

const datasetStore = useDatasetStore();
const datasets = ref(datasetStore.datasetList);
const datasetSelection = ref(null as DatasetType | null);

const plotLink = ref("");
const generatePlotLink = () => {
  if (geneList.value.length < 2 || geneList.value.length > 3) {
    toastProvider({
      type: "danger",
      message: "You must provide at least 2 gene names, and at most 3.",
    });
    return;
  }
  if (!datasetSelection.value) {
    toastProvider({
      type: "danger",
      message: "You must select a dataset.",
    });
    return;
  }
  plotLink.value = `/api/getVennDiagramPlot/${
    datasetSelection.value.db_name
  }/?genes=${geneList.value.join(",")}`;
};

onBeforeMount(async () => {
  if (!genes.value.length) {
    if (!geneStore.geneList.length) {
      await geneStore.load();
    }
    genes.value = geneStore.geneList;
    geneSearch.setCollection(genes.value);
  }

  if (!datasets.value.length) {
    if (!datasetStore.datasetList.length) {
      await datasetStore.load();
    }
    datasets.value = datasetStore.datasetList;
  }
});
</script>
