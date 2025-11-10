<script setup>
import { fetchSources, fetchPosts } from "@apis";
const sources = ref([]);

const size = ref(40)
const page = ref(0)
const loading = ref(true)
const filter = ref({
  sources: [],
  search: null,
  start_date: null,
  end_date: null,
  sort: "By Date",
});

// load posts
const stop_load = ref(false)
const posts = ref([]);
const loadData = async () => {
  loading.value = true
  const response = await fetchPosts(filter.value, size.value, page.value);

  if ('error' in response){
    alert.value.show = true
    alert.value.message = response.message
    alert.value.color = "error"
    loading.value = false
    return
  }

  if(response.data.length == 0){
    stop_load.value = true
  }
  posts.value.push(...response.data);
  loading.value = false
};

// refresh posts
const refresh = async () => {
  page.value = 0
  posts.value = []
  stop_load.value = false
  await loadData()
};

onMounted(async () => {
  sources.value = await fetchSources();
  loadData();
  window.addEventListener('scroll', checkWindowScrollBottom)
});

// load posts on scroll to bottom
const checkWindowScrollBottom = async () => {
  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight) {
    if(stop_load.value) return
    page.value += 1
    await loadData()
  }
}

// Clean up the event listener when the component is about to be unmounted
onBeforeUnmount(() => {
  window.removeEventListener('scroll', checkWindowScrollBottom)
})

const alert = ref({
  show: false,
  message: "",
  color: "success",
})
</script>

<template>
  <div>
    <v-snackbar
    :color="alert.color"
      v-model="alert.show"
    >
      {{alert.message}}

      <template v-slot:actions>
        <v-btn
          color="pink"
          variant="text"
          @click="alert.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <h1 class="text-4xl font-bold mb-4">Feeds</h1>
    <v-card class="pa-5">
      <v-row>
        <v-col cols="6">
          <label><v-icon icon="tabler-world-www"></v-icon> Sources</label>
          <AppAutocomplete
            class="mt-2"
            placeholder="Select source"
            :items="sources"
            item-value="id"
            item-title="name"
            v-model="filter.sources"
            chips
            multiple
            closable-chips
            clearable
          />
        </v-col>
        <v-col cols="6">
          <label><v-icon icon="tabler-search"></v-icon> Keyword ( separate with space)</label>
          <AppTextField
            class="mt-2"
            placeholder="Search query"
            v-model="filter.search"
          />
        </v-col>
        <v-col cols="3">
          <label
            ><v-icon icon="tabler-calendar-week"></v-icon> Start Date</label
          >
          <AppDateTimePicker
            class="mt-2"
            v-model="filter.start_date"
            placeholder="Select date"
          />
        </v-col>
        <v-col cols="3">
          <label
            ><v-icon icon="tabler-calendar-week"></v-icon> End Date</label
          >
          <AppDateTimePicker
            class="mt-2"
            v-model="filter.end_date"
            placeholder="Select date"
          />
        </v-col>
        <v-col cols="3">
          <label><v-icon icon="tabler-sort-descending-2"></v-icon> Sort</label>
          <v-select
            class="mt-2"
            v-model="filter.sort"
            :items="['By date', 'By relevance', 'By title']"
          ></v-select>
        </v-col>
        <v-col cols="2">
          <div class="d-flex align-end justify-end h-100">
            <v-btn @click="refresh"
              ><v-icon icon="tabler-refresh"></v-icon> Refresh</v-btn
            >
          </div>
        </v-col>
      </v-row>
    </v-card>
    <v-card class="mt-4 pa-5">
      <v-row class="h-100">
        <v-col class="h-100" :cols="12">
            <!-- 👉 post list -->
            <ListView :posts="posts"> </ListView>
            <!--  loading icon -->
            <div style="min-height: 50px; width: 100%;" class="d-flex justify-center">
                <VProgressCircular class="my-5" :class="(loading == true) ? 'd-block' : 'd-none'"
                  :size="40" color="primary" indeterminate />
              </div>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>
