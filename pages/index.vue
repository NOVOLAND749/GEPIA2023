<template>
  <div class="mb-20">
    <div class="absolute left-0 max-w-sm mt-2 ml-2 flex flex-row">
      <div v-if="showSidebar" class="mb-20">
        <div v-if="abbrsPending" class="w-full">
          <div class="w-full mx-auto">
            <Spinner size="8" color="white" />
          </div>
        </div>
        <div v-else-if="!abbrs">
          <Alert type="warning">
            Something went wrong, please try again later.
          </Alert>
        </div>
        <div v-else>
          <Accordion flush>
            <AccordionPanel>
              <AccordionHeader class="bg-gray-100"
                >Disease Abbreviations</AccordionHeader
              >
              <AccordionContent v-for="ab in abbrs" class="bg-gray-50">
                <div class="flex flex-row">
                  <div class="w-10 mr-4 text-right font-bold my-auto">
                    {{ ab.abbr }}
                  </div>
                  <div class="text-sm my-auto">
                    {{ ab.full }}
                  </div>
                </div>
              </AccordionContent>
            </AccordionPanel>
          </Accordion>
        </div>
      </div>
      <div @click="showSidebar = !showSidebar" class="cursor-pointer">
        <Icon
          name="material-symbols:chevron-right-rounded"
          size="2rem"
          class="ease-out duration-100"
          :class="{ 'rotate-180': showSidebar }"
        ></Icon>
      </div>
    </div>
    <div class="max-w-4xl mx-auto pt-4">
      <div>Main content</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Spinner,
  Alert,
  Accordion,
  AccordionPanel,
  AccordionHeader,
  AccordionContent,
} from "flowbite-vue";
const { data: abbrs, pending: abbrsPending } = await useLazyFetch(
  "/api/getDiseaseAbbr"
);
const showSidebar = ref(false);
</script>
