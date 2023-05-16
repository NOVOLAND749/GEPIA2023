<template>
  <div class="w-full">
    <div class="grid grid-cols-9 gap-4">
      <DetailCard :gene="gene" class="col-span-9 md:col-span-4 h-fit" />

      <TableCard
        :title="`Genes similar to ${gene.gene_name}`"
        :description="`Score is given as the Pearson correlation between the expression of ${gene.gene_name} and that of others`"
        :tableData="similarGenes"
        :tableCols="[
          { key: 'gene_name', name: 'Gene Name' },
          { key: 'value', name: 'Score' },
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
      :imageUrl="genePlotLinks.StripPlot"
      yLabel="<b>T</b>ranscripts <b>P</b>er <B>M</B>illion (<b>TPM</b>)"
      class="mt-4"
    />

    <PlotCard
      :title="`Expression profile of ${gene.gene_name} across all tumor samples and
    paired normal tissues`"
      description="Bar height represents the median expression of certain sample"
      :imageUrl="genePlotLinks.BarPlot"
      yLabel="<b>T</b>ranscripts <b>P</b>er <B>M</B>illion (<b>TPM</b>)"
      class="mt-4"
    />
  </div>
</template>

<script setup lang="ts">
import GeneDetailType from "~/types/GeneDetailType";

const props = defineProps({
  gene: {
    type: Object as PropType<GeneDetailType>,
    required: true,
  },
});
const { gene } = props;

const genePlotLinks = getGenePlotLinks(gene);
const { data: similarGenes } = await useFetch(
  `/api/getSimilarGenes/${gene.gene_name}`
);
</script>
