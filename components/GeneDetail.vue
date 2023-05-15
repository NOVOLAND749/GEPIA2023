<template>
  <div class="w-full">
    <TheCard class="mx-auto">
      <h3 class="text-4xl text-gray-800 font-bold pb-2">
        {{ gene.gene_name }}
      </h3>
      <p class="py-1">{{ gene.description }}</p>
      <div v-if="gene.Synonyms && gene.Synonyms != '-'" class="cardEntry">
        <h4>Synonyms</h4>
        <div class="flex flex-row flex-wrap gap-y-2.5 w-full py-2">
          <Badge v-for="syn in gene.Synonyms.split('|')">{{ syn }}</Badge>
        </div>
      </div>
      <div class="cardEntry">
        <h4>Chromosome location</h4>
        <div class="grid grid-cols-2 gap-3 pt-3 w-3/4">
          <b class="text-right">Chromosome</b>
          <p>{{ gene.chromosome.substring(3) }}</p>
          <b class="text-right">Start</b>
          <p>{{ gene.start }}</p>
          <b class="text-right">End</b>
          <p>{{ gene.end }}</p>
        </div>
      </div>
      <div class="cardEntry">
        <h4>Ensembl ID</h4>
        <div class="pt-3">
          {{ gene.ENSEMBL }}
        </div>
      </div>
      <div class="cardEntry">
        <h4>External links</h4>
        <div class="flex flex-row flex-wrap gap-y-2.5 w-full py-2">
          <a
            v-for="{ name, link } in externalLinks"
            :href="link"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Badge>
              <template #icon>
                <Icon name="material-symbols:arrow-outward"></Icon>
              </template>
              {{ name }}
            </Badge>
          </a>
        </div>
      </div>
    </TheCard>
  </div>
</template>

<script setup lang="ts">
import { TheCard, Badge } from "flowbite-vue";
import GeneDetailType from "~/types/GeneDetailType";

const props = defineProps({
  gene: {
    type: Object as PropType<GeneDetailType>,
    required: true,
  },
});
const { gene } = props;
const externalLinks = getGeneExternalLinks(gene);
</script>

<style scoped>
.cardEntry {
  @apply w-full border-t mt-2;
}
.cardEntry h4 {
  @apply text-xl pt-1;
}
</style>
