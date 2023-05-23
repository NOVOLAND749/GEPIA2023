<template>
  <div class="w-full">
    <div v-if="genePending">
      <Spinner size="12" color="white" />
    </div>
    <div v-else-if="gene">
      <div class="grid grid-cols-9 gap-4">
        <DetailCard :gene="gene" class="col-span-9 md:col-span-4 h-fit" />
        <TableCard
          v-if="similarGenes.length"
          :title="`Genes similar to ${gene.gene_name}`"
          :description="`Score is given as the Pearson correlation between the expression of ${gene.gene_name} and that of others`"
          :tableData="similarGenes"
          :tableCols="[
            { key: 'gene_name', name: 'Gene Name', precisions: null },
            { key: 'value', name: 'Score', precisions: null },
          ]"
          :geneNameIndex="0"
          :pageSize="10"
          class="col-span-9 md:col-span-5"
        />
      </div>

      <PlotCard
        :title="`Expression profile of ${gene.gene_name} across all tumor samples and
    paired normal tissues`"
        description="Each dot represents an expression of certain sample"
        :imageUrl="genePlotLinks!.StripPlot"
        yLabel="<b>T</b>ranscripts <b>P</b>er <B>M</B>illion (<b>TPM</b>)"
        class="mt-4"
      />

      <PlotCard
        :title="`Expression profile of ${gene.gene_name} across all tumor samples and
    paired normal tissues`"
        description="Bar height represents the median expression of certain sample"
        :imageUrl="genePlotLinks!.BarPlot"
        yLabel="<b>T</b>ranscripts <b>P</b>er <B>M</B>illion (<b>TPM</b>)"
        class="mt-4"
      />

      <PlotCard
        :title="`Copy number variance of ${gene.gene_name} across all datasets`"
        description="Bar height represents the percentage of samples that has a certain type of copy number variant"
        :imageUrl="genePlotLinks!.CopyNumberPlot"
        class="mt-4"
      />
    </div>
    <div v-else>
      <Alert type="warning" class="mx-auto">
        Something went wrong, please try again later.
      </Alert>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Spinner, Alert } from "flowbite-vue";
import GeneDetailType from "~/types/GeneDetailType";
import SimilarGeneType from "~/types/SimilarGeneType";

const props = defineProps({
  geneName: {
    type: String,
    required: true,
  },
});
const { geneName } = props;
const gene = ref<GeneDetailType | null>(null);
const genePending = ref(true);
const genePlotLinks = computed(() => {
  if (!gene.value) return null;
  return getGenePlotLinks(gene.value);
});
const similarGenes = ref<SimilarGeneType[]>([]);

onMounted(async () => {
  gene.value = await $fetch<GeneDetailType>(`/api/getGeneDetail/${geneName}`);
  genePending.value = false;
  similarGenes.value = await $fetch<SimilarGeneType[]>(
    `/api/getSimilarGenes/${gene.value.gene_name}`
  );
});
</script>
