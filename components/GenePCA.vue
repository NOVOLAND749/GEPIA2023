<template>
  <div>
    <p class="text-sm py-2 font-medium">
      Selected at least 5 genes (click to remove)
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

    <p class="text-sm py-2 font-medium">Selected datasets (click to remove)</p>
    <div class="flex flex-row items-center gap-2">
      <div class="flex-grow">
        <div class="h-10 rounded-md border flex flex-row">
          <Button
            v-for="ds in datasetSelection"
            color="alternative"
            @click="datasetSelection = datasetSelection.filter((d) => d != ds)"
          >
            {{ ds }}
          </Button>
        </div>
      </div>
      <div>
        <Dropdown placement="left">
          <template #trigger="{ trigger }">
            <Button @click="trigger" color="alternative">
              <Icon name="material-symbols:add" size="24"></Icon>
            </Button>
          </template>
          <ListGroup class="max-h-60 overflow-y-scroll">
            <ListGroupItem
              v-for="ds in availableDatasets"
              @click="updateDatasetSelection(ds)"
            >
              {{ ds }}
            </ListGroupItem>
          </ListGroup>
        </Dropdown>
      </div>
      <div>
        <Button @click="generatePlotLink" class="h-10">Go!</Button>
      </div>
    </div>

    <div class="pt-2 px-2">
      <PlotCard
        v-if="elbowPlotLink"
        title="Explained variance of principal components"
        description=""
        :imageUrl="elbowPlotLink"
        :key="elbowPlotLink"
        class="mt-4"
      />
      <PlotCard
        v-if="scatterPlotLink"
        title="Scatter plot of samples in the first two principal components"
        description=""
        :imageUrl="scatterPlotLink"
        :key="scatterPlotLink"
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
    } else {
      geneList.value.push(geneSearchTerm.value);
      geneSearchTerm.value = "";
    }
  }
});

const datasetStore = useDatasetStore();
const datasets = ref(datasetStore.datasetList);
const datasetSelection = ref([] as string[]);

const availableDatasets = computed(() => {
  return [
    ...datasets.value
      .filter((d) => d.has_normal)
      .map((d) => d.db_name + "-normal"),
    ...datasets.value.map((d) => d.db_name + "-tumor"),
  ]
    .filter((d) => !datasetSelection.value.includes(d))
    .sort();
});

const updateDatasetSelection = (dataset: string) => {
  if (datasetSelection.value.includes(dataset)) {
    return;
  }
  if (datasetSelection.value.length >= 5) {
    toastProvider({
      type: "warning",
      message: "You may only select up to 5 datasets.",
    });
    return;
  }
  datasetSelection.value.push(dataset);
};

const elbowPlotLink = ref("");
const scatterPlotLink = ref("");
const generatePlotLink = () => {
  if (geneList.value.length < 5) {
    toastProvider({
      type: "danger",
      message: "You must provide at least 5 gene names.",
    });
    return;
  }
  if (!datasetSelection.value.length) {
    toastProvider({
      type: "danger",
      message: "You must select at least one dataset.",
    });
    return;
  }
  elbowPlotLink.value = SynthUrl(["getElbowPlot"], {
    datasets: datasetSelection.value,
    genes: geneList.value,
  });
  scatterPlotLink.value = SynthUrl(["getPCAScatterPlot"], {
    datasets: datasetSelection.value,
    genes: geneList.value,
  });
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
