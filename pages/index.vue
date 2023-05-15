<template>
  <div>
    <div class="absolute left-0 max-w-sm mb-20 mt-2 ml-2 flex flex-row">
      <div v-if="showSidebar">
        <div v-if="abbrsPending"></div>
        <div v-else-if="!abbrs">
          <TheCard class="bg-yellow-100">
            <h5 class="mb-2 text-2xl font-bold tracking-tight text-yellow-900">
              Something went wrong, please try again later.
            </h5>
          </TheCard>
        </div>
        <div v-else>
          <ListGroup class="w-fit">
            <ListGroupItem v-for="ab in abbrs">
              <div class="w-10 mr-3 text-right font-bold">
                {{ ab.abbr }}
              </div>
              {{ ab.full }}
            </ListGroupItem>
          </ListGroup>
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
    <div class="max-w-4xl mx-auto py-4">Main content</div>
  </div>
</template>

<script setup lang="ts">
import { TheCard, ListGroup, ListGroupItem } from "flowbite-vue";
const { data: abbrs, pending: abbrsPending } = await useFetch(
  "/api/getDiseaseAbbr"
);
const showSidebar = ref(false);
</script>
