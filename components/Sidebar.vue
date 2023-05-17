<template>
  <div class="fixed left-0 top-16 max-w-sm flex flex-row">
    <div
      v-if="showSidebar"
      class="px-2 py-4 max-h-[calc(100vh-7rem)] overflow-y-scroll"
    >
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
        <Accordion flush always-open>
          <AccordionPanel class="rounded-lg overflow-hidden border shadow-lg">
            <AccordionHeader class="bg-gray-50">
              <Icon name="material-symbols:match-word" size="24" class="pb-1" />
              Disease Abbreviations
            </AccordionHeader>
            <AccordionContent v-for="ab in abbrs" class="bg-white border-x">
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
    <div
      @click="showSidebar = !showSidebar"
      class="cursor-pointer h-[calc(100vh-7rem)] flex justify-center items-center hover:bg-white hover:bg-opacity-50 hover:shadow-md hover:backdrop-blur-[1px]"
    >
      <Icon
        name="material-symbols:chevron-right-rounded"
        size="32"
        class="ease-out duration-100"
        :class="{ 'rotate-180': showSidebar }"
      ></Icon>
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
