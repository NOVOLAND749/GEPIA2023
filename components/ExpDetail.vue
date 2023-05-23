<template>
  <div class="w-full">
    <div v-if="pending">
      <Spinner size="12" color="white" />
    </div>
    <TableCard
      v-if="diffExpProfile.length"
      :title="`Differential expression profile ${datasetName}`"
      description=""
      :tableData="diffExpProfile"
      :tableCols="[
        { key: 'gene_name', name: 'Gene Name', precisions: null },
        { key: 'tumor_median', name: 'Median (Tumor)', precisions: 3 },
        { key: 'normal_median', name: 'Median (Normal)', precisions: 3 },
        { key: 'log2fc', name: 'Log2(Fold Change)', precisions: 9 },
        { key: 'p', name: 'P-value (adjusted)', precisions: 9 },
      ]"
      :geneNameIndex="0"
      :pageSize="pageSize"
      class="col-span-9 md:col-span-5"
    />
  </div>
</template>

<script setup lang="ts">
import { Spinner } from "flowbite-vue";
import DiffExpType from "~/types/DiffExpType";

const props = defineProps({
  datasetName: {
    type: String,
    required: true,
  },
  log2FC: {
    type: Number,
    required: true,
  },
  qValue: {
    type: Number,
    required: true,
  },
});
const { datasetName, log2FC, qValue } = props;

const diffExpProfile = ref<DiffExpType[]>([]);
const pending = ref(true);
const pageSize = ref(10);

onMounted(async () => {
  diffExpProfile.value = await $fetch<DiffExpType[]>(
    SynthUrl(["getDiffExp", datasetName], { log2FC, qValue })
  );
  pending.value = false;
});
</script>
