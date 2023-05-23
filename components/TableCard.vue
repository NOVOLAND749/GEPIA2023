<template>
  <div class="py-6 px-2 rounded-lg bg-white shadow-md border">
    <h3 class="text-lg font-bold text-center" v-html="title"></h3>
    <h4 class="text-center" v-if="description" v-html="description"></h4>

    <div class="relative overflow-x-auto rounded-lg border mt-8">
      <table class="w-full text-sm text-center text-gray-500">
        <thead class="text-sm text-gray-700 bg-gray-50 border-b">
          <tr class="border-b">
            <th
              scope="col"
              class="px-6 py-3"
              v-for="[idx, col] in tableCols.entries()"
            >
              <div
                class="flex flex-row justify-center items-center cursor-pointer hover:text-primary"
                @click="toggleSortBy(idx)"
              >
                <p>
                  {{ col.name }}
                </p>
                <Icon
                  :name="
                    matchAscend(idx)
                      ? 'material-symbols:trending-up'
                      : matchDescend(idx)
                      ? 'material-symbols:trending-down'
                      : 'material-symbols:sort'
                  "
                  size="24"
                />
              </div>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="border-b"
            v-for="[idx, entry] in slicedTableData.entries()"
            :class="{ 'bg-gray-50': idx % 2 }"
          >
            <th
              scope="row"
              class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap"
            >
              <NuxtLink
                :href="
                  geneNameIndex == 0 ? `/?gene=${entry[tableCols[0].key]}` : '#'
                "
                :class="{
                  'cursor-default pointer-events-none': !(geneNameIndex == 0),
                  'text-primary': geneNameIndex == 0,
                }"
                target="_blank"
              >
                {{ entry[tableCols[0].key] }}
              </NuxtLink>
            </th>
            <td
              class="px-6 py-4"
              v-for="[i, col] in tableCols.slice(1).entries()"
            >
              <NuxtLink
                :href="
                  geneNameIndex == i + 1 ? `/?gene=${entry[col.key]}` : '#'
                "
                :class="{
                  'cursor-default pointer-events-none': !(
                    geneNameIndex ==
                    i + 1
                  ),
                  'text-primary': geneNameIndex == i + 1,
                }"
                target="_blank"
                rel="noopener noreferrer"
              >
                {{
                  col.precisions
                    ? (entry[col.key] as number).toFixed(col.precisions)
                    : entry[col.key]
                }}
              </NuxtLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="text-center pt-2">
      <ButtonGroup>
        <Button
          color="alternative"
          class="shadow-none border-none"
          square
          @click="currentPageNum = 1"
          :disabled="currentPageNum == 1"
        >
          <Icon name="material-symbols:first-page" size="24" />
        </Button>
        <Button
          color="alternative"
          class="shadow-none border-none"
          square
          @click="currentPageNum--"
          :disabled="currentPageNum == 1"
        >
          <Icon name="material-symbols:chevron-left" size="24" />
        </Button>
        <Button
          color="alternative"
          class="shadow-none border-none"
          square
          disabled
        >
          {{ currentPageNum }} / {{ totalPages }}
        </Button>
        <Button
          color="alternative"
          class="shadow-none border-none"
          square
          @click="currentPageNum++"
          :disabled="currentPageNum == totalPages"
        >
          <Icon name="material-symbols:chevron-right" size="24" />
        </Button>
        <Button
          color="alternative"
          class="shadow-none border-none"
          square
          @click="currentPageNum = totalPages"
          :disabled="currentPageNum == totalPages"
        >
          <Icon name="material-symbols:last-page" size="24" />
        </Button>
      </ButtonGroup>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ButtonGroup, Button, Table } from "flowbite-vue";

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
  tableData: {
    type: Object as PropType<{ [key: string]: string | number }[]>,
    required: true,
  },
  geneNameIndex: {
    type: Number,
    required: false,
    default: -1,
  },
  tableCols: {
    type: Object as PropType<
      { key: string; name: string; precisions: number | null }[]
    >,
    required: true,
  },
  pageSize: {
    type: Number,
    required: false,
    default: 0,
  },
});

const { title, description, tableData, tableCols, pageSize, geneNameIndex } =
  props;

const totalPages = pageSize == 0 ? 1 : Math.ceil(tableData.length / pageSize);
const currentPageNum = ref(1);

const sortBy = ref(0);
const matchAscend = (idx: number) => {
  return sortBy.value - 1 == idx;
};
const matchDescend = (idx: number) => {
  return sortBy.value + 1 == -idx;
};
const toggleSortBy = (idx: number) => {
  if (!matchAscend(idx) && !matchDescend(idx)) {
    sortBy.value = idx + 1;
  } else if (matchAscend(idx)) {
    sortBy.value = -idx - 1;
  } else {
    sortBy.value = 0;
  }
};
const sortedTableData = computed(() => {
  if (sortBy.value == 0) {
    return tableData;
  } else {
    const idx = Math.abs(sortBy.value) - 1;
    const isAscend = sortBy.value > 0;
    return tableData.sort((a, b) => {
      if (isAscend) {
        return a[tableCols[idx].key] > b[tableCols[idx].key] ? 1 : -1;
      } else {
        return a[tableCols[idx].key] < b[tableCols[idx].key] ? 1 : -1;
      }
    });
  }
});

const slicedTableData = computed(() => {
  if (pageSize > 0) {
    return sortedTableData.value.slice(
      (currentPageNum.value - 1) * pageSize,
      currentPageNum.value * pageSize
    );
  } else {
    return sortedTableData.value;
  }
});
</script>
