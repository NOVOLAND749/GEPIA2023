<template>
  <div>
    <div class="flex flex-row gap-2">
      <div class="flex-grow min-w-fit my-auto">
        Dataset:
        <Dropdown placement="bottom">
          <template #trigger="{ toggle }">
            <Button @click="toggle">
              {{ datasetSelection ? datasetSelection.db_name : "Choose one" }}
            </Button>
          </template>
          <ListGroup class="max-h-60 overflow-y-scroll">
            <ListGroupItem
              v-for="ds in datasets"
              :disabled="!ds.has_normal"
              @click="
                datasetSelection = ds.has_normal ? ds : datasetSelection;
                catchDatasetError(ds);
              "
            >
              {{ ds.db_name }}
            </ListGroupItem>
          </ListGroup>
        </Dropdown>
      </div>
      <div class="w-1/3 min-w-fit">
        <Input
          placeholder="1.00"
          label="|log₂ Fold-Change| Cutoff"
          v-model.lazy.trim.number="log2FC"
        >
          <template #prefix>
            <Icon name="material-symbols:123" size="24"></Icon>
          </template>
        </Input>
      </div>
      <div class="w-1/3 min-w-fit">
        <Input
          placeholder="1.00"
          label="Q-value Cutoff"
          v-model.lazy.trim.number="qValue"
        >
          <template #prefix>
            <Icon name="material-symbols:123" size="24"></Icon>
          </template>
        </Input>
      </div>
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
  Spinner,
  ListGroup,
  ListGroupItem,
  Input,
  Button,
  Dropdown,
  Toast,
} from "flowbite-vue";
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

const datasetStore = useDatasetStore();
const datasets = ref(datasetStore.datasetList);
const datasetSelection = ref(null as DatasetType | null);

const catchDatasetError = (dataset: DatasetType) => {
  if (!dataset.has_normal) {
    toastProvider({
      type: "warning",
      message: `You cannot select the ${dataset.db_name} dataset as it does not have normal samples.`,
    });
  }
};

const log2FC = ref("1.0");
const qValue = ref("0.01");

const log2FCNumber = computed(() => {
  return parseFloat(log2FC.value);
});
const qValueNumber = computed(() => {
  return parseFloat(qValue.value);
});

watch(log2FCNumber, (log2FCNumber) => {
  if (log2FCNumber <= 0.0) {
    toastProvider({
      type: "danger",
      message: `The log₂ Fold-Change cutoff value ${log2FCNumber} must be positive.`,
    });
  }
});

watch(qValueNumber, (qValueNumber) => {
  if (qValueNumber <= 0.0 || qValueNumber >= 1.0) {
    toastProvider({
      type: "danger",
      message: `The Q-value cutoff value ${qValueNumber} must be between 0 and 1.`,
    });
  }
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
