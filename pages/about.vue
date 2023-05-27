<template>
  <div>
    <Head>
      <Title>GEPIA 2023 - About</Title>
    </Head>

    <div class="max-w-5xl mx-auto p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="flex flex-col gap-4">
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              GeneView
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              GeneView module is used to provide general information of a
              specified gene across all datasets. By entering gene name in the
              search box, you will get the following information:
            </AccordionContent>
            <AccordionContent class="bg-white border-x">
              <ol>
                <li>General description of the gene.</li>
                <li>
                  Expression level in all datasets. The data was shown by dot
                  plot and bar plot.
                </li>
                <li>
                  Similar genes calculated by Pearson Correlation
                  Coefficient(PCC). The list is ranked by the PCC score.
                </li>
                <li>
                  Copy Number Variation in all samples across the datasets.
                </li>
              </ol>
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              DiffExp
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              DiffExp module is used to apply statistical methods and threshold
              on a given dataset to dynamically obtain differentially expressed
              genes.
            </AccordionContent>
            <AccordionContent class="bg-white border-x">
              Users can set the Log2FC and q-value threshold to filter genes.
              Genes with higher Log2FC value and lower q-value will be kept.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              GeneExp
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              GeneExp module is used to apply statistical methods on the chosen
              dataset to compare gene expression level between the tumor and
              normal samples.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
      <div class="flex flex-col gap-4">
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              GeneSurvival
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              GeneSurvival module is used to perform survival analysis in a
              gene's high expressed and low expressed group.
            </AccordionContent>
            <AccordionContent class="bg-white border-x">
              Users can set the High and Low cutoff to determine the high
              expressed and low expressed group.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              GenePCA
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              GenePCA module is used to perform dimension reduction by PCA.
            </AccordionContent>
            <AccordionContent class="bg-white border-x">
              Users can enter the gene of interest list and choose different
              datasets. This will return a variation bar plot and a 2D
              visualization figure on all samples.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              DataSetView
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              DataSetView module provide information about dataset.
            </AccordionContent>
            <AccordionContent class="bg-white border-x">
              It return the cell type proportion of the given dataset by
              non-reference deconvolution methods. It can be a reference for
              users to know the general cell composition. To use reference
              deconvolution method, please jump to GEPIA2021.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:info" size="24" class="pb-1" />
              CopyNumVar
            </AccordionHeader>
            <AccordionContent class="bg-white border-x">
              CopyNumVar module show the intersection in different genes’ copy
              number variation. Users can select genes of interest for 2-3 and
              given dataset, then the result will show in Venn Plot.
            </AccordionContent>
          </AccordionPanel>
        </Accordion>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Accordion,
  AccordionPanel,
  AccordionHeader,
  AccordionContent,
} from "flowbite-vue";
</script>

<style scoped>
ol {
  @apply space-y-2 text-gray-500 list-disc list-outside;
}
</style>
