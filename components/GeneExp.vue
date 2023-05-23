<template>
  <div>
    <Input
      placeholder="Enter a gene name, e.g. ERBB2"
      label="Gene name to view"
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
              :disabled="!ds.has_normal"
              @click="updateDatasetSelection(ds)"
            >
              {{ ds.db_name }}
            </ListGroupItem>
          </ListGroup>
        </Dropdown>
      </div>
      <div>
        <Button @click="generatePlotLink">Go!</Button>
      </div>
    </div>

    <div class="pt-2 px-2">
      <PlotCard
        v-if="plotLink"
        :title="`Expression profile of ${geneSearchTerm} across tumor samples and
  paired normal tissues`"
        :description="`Dataset(s): ${datasetSelection
          .map((e) => e.db_name)
          .join(' ')}`"
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
  ToastProvider,
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
  plotLink.value = `/api/getBoxPlot/${
    geneSearchTerm.value
  }/${datasetSelection.value.map((e) => e.db_name).join("&")}/`;
};

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
  if (dataset.has_normal) {
    datasetSelection.value.push(dataset);
  } else {
    toastProvider({
      type: "warning",
      message: `You cannot select the ${dataset.db_name} dataset as it does not have normal samples.`,
    });
  }
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
