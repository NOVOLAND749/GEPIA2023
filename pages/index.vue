<template>
  <div>
    <Head>
      <Title>GEPIA 2023 - Home</Title>
    </Head>
    <div class="max-w-4xl mx-auto pt-4 px-4">
      <h1 class="py-8 text-3xl text-center text-gray-600 font-bold mx-auto">
        GEPIA 2023
      </h1>
      <Tabs v-model="activeTab" variant="underline">
        <Tab name="first" title="GeneView">
          <GeneView class="py-2"></GeneView>
        </Tab>
        <Tab name="second" title="DiffExp">
          <DiffExp class="py-2"></DiffExp>
        </Tab>
        <Tab name="third" title="GeneExp">
          <GeneExp class="py-2"></GeneExp>
        </Tab>
      </Tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Tab, Tabs } from "flowbite-vue";

const activeTab = ref("first");
</script>
