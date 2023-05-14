<template>
  <div>
    <div
      v-if="showSidebar"
      class="absolute left-0 max-w-sm"
      @click="showSidebar = false"
    >
      <div v-if="abbrsPending"></div>
      <div v-else-if="!abbrs">
        <TheCard class="bg-yellow-100 mx-5 my-4">
          <h5 class="mb-2 text-2xl font-bold tracking-tight text-yellow-900">
            Something went wrong, please try again later.
          </h5>
        </TheCard>
      </div>
      <div v-else>
        <ListGroup class="w-fit mb-20 mt-2 ml-2">
          <ListGroupItem v-for="ab in abbrs">
            <div class="w-10 mr-3 text-right">
              {{ ab.abbr }}
            </div>
            {{ ab.full }}
          </ListGroupItem>
        </ListGroup>
      </div>
    </div>
    <div class="max-w-4xl mx-auto py-4">
      <Button @click="showSidebar = true">Show disease abbreviation </Button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TheCard, Button, ListGroup, ListGroupItem } from "flowbite-vue";
const { data: abbrs, pending: abbrsPending } = await useFetch(
  "/api/diseaseAbbr"
);
const showSidebar = ref(true);
</script>
