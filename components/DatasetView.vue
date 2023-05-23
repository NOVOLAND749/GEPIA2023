<template>
  <div>
    <p class="my-1">Dataset:</p>
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

    <div class="pt-2">
      <PlotCard
        v-if="plotLink"
        :key="plotLink"
        :title="`Cell type distribution of ${datasetSelection!.db_name}`"
        :image-url="plotLink"
      ></PlotCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ListGroup, ListGroupItem, Button, Dropdown } from "flowbite-vue";
import DatasetType from "~/types/DatasetType";

const datasetStore = useDatasetStore();
const datasets = ref(datasetStore.datasetList);
const datasetSelection = ref(null as DatasetType | null);

const plotLink = computed(() => {
  if (!datasetSelection.value) return "";
  return SynthUrl(["getCellTypePlot"], {
    dataset: datasetSelection.value.db_name,
  });
});

onBeforeMount(async () => {
  if (!datasets.value.length) {
    if (!datasetStore.datasetList.length) {
      await datasetStore.load();
    }
    datasets.value = datasetStore.datasetList;
  }
});
</script>
