<script setup>
import { fetchTopics, fetchPosts } from "@apis";


const filter = ref({
  date: "Last week",
});


const topics = ref(null)
const load_topics = async () => {
  const posts_response = await fetchPosts(filter, 900,  0);
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
  console.log("topics", topics.value);
}


const browserStates = [
  {
    title: 'Google Chrome',
    stats: '90.4',
    progress: 'secondary',
  },
  {
    title: 'Apple Safari',
    stats: '70.6',
    progress: 'success',
  },
  {
    title: 'Mozilla Firefox',
    stats: '35.5',
    progress: 'primary',
  },
  {
    title: 'Opera Mini',
    stats: '80.0',
    progress: 'error',
  },
  {
    title: 'Internet Explorer',
    stats: '62.2',
    progress: 'info',
  },
  {
    title: 'Brave',
    stats: '46.3',
    progress: 'warning',
  },
]

onMounted(async () => {

  await load_topics();
});
</script>

<template>
  <div>
    <h1 class="font-weight-regular mb-4">Dashboard</h1>
    <v-row class="match-height">
      <v-col>
        
      </v-col>
    </v-row>
    <div class="d-flex  justify-space-between ">
      

      <div>
        <v-select
            min-width="200"
            class="mt-2"
            v-model="filter.date"
            :items="['Last week', 'Last 15 days', 'Last month', 'Last year']"
          ></v-select>
      </div>
      
    </div>
    
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

            <h5 class="text-h5 mt-4">
              Total Sources
            </h5>
            <VChip color="disabled" label>
              2
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

            <h5 class="text-h5 mt-4">
              Total Articles
            </h5>
            <VChip color="disabled" label>
              100
            </VChip>
          </VCardText>
        </VCard>
    </v-col>

    <v-col  cols="12"
        sm="12"
        md="4"
        lg="8">
        <VCard>
          <VCardText>
            <v-chip-group>
              <template v-for="(topic, title) in topics"><v-chip size="large" variant="outlined" class="py-4 ms-2" v-if="topic.count != 0">
                    {{ title }}
                    <template v-slot:append>
                    <v-badge color="info" :content="topic.count " inline></v-badge>
                  </template>
                  </v-chip></template>
                  
                </v-chip-group>
          </VCardText>
        </VCard>
    </v-col>

    </v-row>

    <v-row>
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
          v-for="state in browserStates"
          :key="state.title"
        >
          <template #prepend>
            <VAvatar size="28">
              <VImg src="" />
            </VAvatar>
          </template>

          <VListItemTitle class="font-weight-medium">
            {{ state.title }}
          </VListItemTitle>

          <template #append>
            <span class="font-weight-medium text-medium-emphasis me-3">{{ state.stats }}%</span>
            <VProgressCircular
              :model-value="state.stats"
              :color="state.progress"
              width="3"
              size="28"
            />
          </template>
        </VListItem>
      </VList>
    </VCardText>
  </VCard>
    </VCol>
    </v-row>
  </div>
</template>


<style lang="scss" scoped>
.sources-stats .card-list {
  --v-card-list-gap: 30px;
}
</style>