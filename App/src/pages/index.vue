<script setup>
import {
    formatTimestamp,
} from "@utils";

import { fetchSources, fetchTopics, fetchPosts, sourcesStats, sourcesChart } from "@apis";


// variables 
const sources = ref([]);

const today = new Date();
const sevenDaysAgo = new Date();
today.setDate(today.getDate() + 1);
sevenDaysAgo.setDate(today.getDate() - 7);

const filter = ref({
  sources: [],
  start_date: sevenDaysAgo.toLocaleDateString('en-CA') ,
  end_date: today.toLocaleDateString('en-CA') ,
});


const stats = ref({
    articles_count : null,
    source_count : null
})


const sources_stats = ref(null)
const sources_chart = ref(null)

const topics = ref(null)


const alert = ref({
  show: false,
  message: "",
  color: "success",
})

const loading = ref(false)

// function 


const load_topics = async () => {
  const posts_response = await fetchPosts(filter.value, 900,  0);
  stats.value.articles_count = posts_response.total
  let articles = []
        posts_response.data.forEach((post, index) => {
          articles.push({
            source: post.source_name,
            title: post.title,
            url: post.url,
            content: post.content,
            date_time: String(post.date_time),
          });
        });
  
  
  const response = await fetchTopics(articles);
  topics.value = response.results;
  
}


const load_sources_stats = async () => {

    const response = await sourcesStats(filter.value);

    if ('error' in response){
        alert.value.show = true
        alert.value.message = response.message
        alert.value.color = "error"
        loading.value = false
        return
    }

    sources_stats.value = response
    stats.value.source_count = response.length
    console.log(sources_stats.value)
}

const load_sources_chart = async () => {

    const response = await sourcesChart(filter.value);

    if ('error' in response){
        alert.value.show = true
        alert.value.message = response.message
        alert.value.color = "error"
        loading.value = false
        return
    }

    sources_chart.value = response
    

}


const source_logo = (source) => {
  const iconFileName = source + ".png";
  const iconName = "/src/assets/images/sources/" + iconFileName;
  const iconModule = new URL(iconName, import.meta.url).href;
  return iconModule || iconSocial;
};


const refresh = async () => {
    
    try{
        if(filter.value.start_date == null && filter.value.end_date == null){
        alert.value.show = true
        alert.value.message = "must specify start date or end date"
        alert.value.color = "error"
        return
        }

        loading.value = true
        await load_topics();
        await load_sources_stats();
        await load_sources_chart();
        loading.value = false
    }
    catch{
        loading.value = false
        alert.value.show = true
        alert.value.message = "error loading dashboard"
        alert.value.color = "error"
    }
    
}



onMounted(async () => {
    sources.value = await fetchSources();
    await refresh();
});
</script>

<template>
  <div>

    <v-overlay
      :model-value="loading"
      class="align-center justify-center"
    >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>


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
    <h1 class="text-4xl font-bold mb-4">Dashboard</h1>
    <v-row class="match-height">
      <v-col>
        <VCard
    title="Filter"
  >
  <VCardText>
  <v-row>
    <!--
        <v-col cols="5">
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
        -->
        <v-col cols="4">
          <label
            ><v-icon icon="tabler-calendar-week"></v-icon> Start Date</label
          >
          <AppDateTimePicker
            class="mt-2"
            v-model="filter.start_date"
            placeholder="Select date"
          />
        </v-col>
        <v-col cols="4">
          <label
            ><v-icon icon="tabler-calendar-week"></v-icon> End Date</label
          >
          <AppDateTimePicker
            class="mt-2"
            v-model="filter.end_date"
            placeholder="Select date"
          />
        </v-col>
        <v-col cols="1" class="ms-auto">
          <div class="d-flex align-end justify-end h-100">
            <v-btn @click="refresh"
              ><v-icon icon="tabler-refresh"></v-icon> Refresh</v-btn
            >
          </div>
        </v-col>
    </v-row>

</VCardText>
      </VCard>
      </v-col>
    </v-row>

    
    <v-row class="match-height">
      <v-col  cols="12"
        sm="6"
        md="4"
        lg="2">
      
        <VCard >
          <VCardText>
            <VAvatar color="error" variant="tonal" rounded size="42">
              <VIcon icon="tabler-world-www" />
            </VAvatar>

            <h5 class="text-h5 my-4">
              Total Sources
            </h5>
            <VChip color="disabled" label>
              {{stats.source_count}}
            </VChip>
          </VCardText>
        </VCard>
      </v-col>

      <v-col  cols="12"
        sm="6"
        md="4"
        lg="2">
        <VCard >
          <VCardText>
            <VAvatar color="info" variant="tonal" rounded size="42">
              <VIcon icon="tabler-rss" />
            </VAvatar>

            <h5 class="text-h5 my-4">
              Total Articles
            </h5>
            <VChip color="disabled" label>
              {{stats.articles_count}}
            </VChip>
          </VCardText>
        </VCard>
    </v-col>

    <v-col  cols="12"
        sm="12"
        md="4"
        lg="8">
        <VCard title="Top Topics">
          <VCardText>
            <v-chip-group>
              <template v-for="(topic, title) in topics">
                <v-chip size="large" variant="outlined" class="py-4 ms-2" v-if="topic.count != 0">
                    {{ title }}
                    <template v-slot:append>
                    <v-badge color="info" :content="topic.count " inline></v-badge>
                  </template>
                  </v-chip>
                </template>
                  
            </v-chip-group>
          </VCardText>
        </VCard>
    </v-col>

    </v-row>

    <v-row class="match-height">
      <VCol
      cols="12"
      md="4"
    >
    <VCard
    class="sources-stats"
    title="Sources States"
  >


    <VCardText>
      <VList class="card-list">
        <VListItem
          v-for="state in sources_stats"
          :key="state.source_name"
        >
          <template #prepend>
            <VAvatar size="28">
              <VImg :src="source_logo(state.source_name)" />
            </VAvatar>
          </template>

          <VListItemTitle class="font-weight-medium">
            {{ state.source_name }}
          </VListItemTitle>

          <template #append>
            <v-badge color="success" :content="state.count " inline></v-badge>
          </template>
        </VListItem>
      </VList>
    </VCardText>
  </VCard>
    </VCol>
    <VCol
      cols="12"
      md="8"
    >
    <StatsChart :data="sources_chart" />
</VCol>

    </v-row>
  </div>
  
</template>


<style lang="scss" scoped>
.sources-stats .card-list {
  --v-card-list-gap: 30px;
}
</style>