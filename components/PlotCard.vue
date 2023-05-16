<template>
  <div class="py-6 px-2 rounded-2xl bg-white shadow-md border">
    <h3 class="text-lg font-bold text-center" v-html="title"></h3>
    <h4 class="text-center" v-if="description" v-html="description"></h4>
    <div class="w-full h-fit flex flex-row items-center">
      <div class="w-10 h-72 flex justify-center items-center" v-if="yLabel">
        <p
          class="transform -rotate-90 whitespace-nowrap text-lg tracking-wide"
          v-html="yLabel"
        ></p>
      </div>
      <img class="flex-auto w-full" :src="imageUrl" loading="lazy" />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: false,
    default: "",
  },
  imageUrl: {
    type: String,
    required: true,
  },
  yLabel: {
    type: String,
    required: false,
    default: "",
  },
});

const { title, description, imageUrl, yLabel } = props;
</script>
