<template>
  <div>
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
            {{ ds.db_name }}
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
              {{ ds.db_name }}
            </ListGroupItem>
          </ListGroup>
        </Dropdown>
      </div>
    </div>
    <div class="flex flex-row items-end gap-2 pt-2">
      <Input
        placeholder="50.0"
        label="Cutoff High (in %)"
        class="flex-grow"
        v-model.lazy.trim.number="cutoffHigh"
      >
        <template #prefix>
          <Icon name="material-symbols:numbers" size="24"></Icon>
        </template>
      </Input>
      <Input
        placeholder="50.0"
        label="Cutoff Low (in %)"
        class="flex-grow"
        v-model.lazy.trim.number="cutoffLow"
      >
        <template #prefix>
          <Icon name="material-symbols:numbers" size="24"></Icon>
        </template>
      </Input>
      <div>
        <Button @click="generatePlotLink" class="h-10">Go!</Button>
      </div>
    </div>

    <div class="pt-2 px-2">
      <PlotCard
        v-if="plotLink"
        :title="`Survival analysis of ${geneSearchTerm} in dataset(s): ${datasetSelection
          .map((e) => e.db_name)
          .join(' ')}`"
        description="High and low expression groups are defined by the percentage cutoffs specified above."
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
import DatasetType from "~/types/DatasetType";
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

const datasetStore = useDatasetStore();
const datasets = ref(datasetStore.datasetList);
const datasetSelection = ref([] as DatasetType[]);

const availableDatasets = computed(() => {
  return datasets.value.filter((ds) => !datasetSelection.value.includes(ds));
});

const cutoffHigh = ref("50.0");
const cutoffLow = ref("50.0");
const cutoffHighNumber = computed(() => parseFloat(cutoffHigh.value));
const cutoffLowNumber = computed(() => parseFloat(cutoffLow.value));
const isvalidCutoffHigh = computed(
  () => cutoffHighNumber.value >= 0 && cutoffHighNumber.value <= 100
);
const isvalidCutoffLow = computed(
  () => cutoffLowNumber.value >= 0 && cutoffLowNumber.value <= 100
);

const updateDatasetSelection = (dataset: DatasetType) => {
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

watch(cutoffHighNumber, (cutoffHighNumber) => {
  if (!isvalidCutoffHigh.value) {
    toastProvider({
      type: "danger",
      message: `The cutoff value ${cutoffHighNumber} must be between 0 and 100.`,
    });
  }
});

watch(cutoffLowNumber, (cutoffLowNumber) => {
  if (!isvalidCutoffLow.value) {
    toastProvider({
      type: "danger",
      message: `The cutoff value ${cutoffLowNumber} must be between 0 and 100.`,
    });
  }
});

const plotLink = ref("");
const generatePlotLink = () => {
  if (!geneSearchTerm.value) {
    toastProvider({
      type: "danger",
      message: "You must provide a gene name.",
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
  if (!isvalidCutoffHigh.value) {
    toastProvider({
      type: "danger",
      message: `Fill in a valid cutoff value for cutoff high.`,
    });
    return;
  }
  if (!isvalidCutoffLow.value) {
    toastProvider({
      type: "danger",
      message: `Fill in a valid cutoff value for cutoff low.`,
    });
    return;
  }
  plotLink.value = `/api/getSurvivalPlot/${
    geneSearchTerm.value
  }/${datasetSelection.value.map((e) => e.db_name).join("&")}/?CutoffHigh=${
    cutoffHighNumber.value
  }&CutoffLow=${cutoffLowNumber.value}`;
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
