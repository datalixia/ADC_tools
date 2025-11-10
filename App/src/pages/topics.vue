<script setup>
import { fetchTopics, fetchPosts } from "@apis";
const posts = ref(null);
const topics = ref(null);
const filter = ref({
  sources: [],
  search: null,
  start_date: null,
  end_date: null,
  sort: "By Date",
});
onMounted(async () => {
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
});
</script>

<template>
  <div>
    <h1 class="font-weight-regular mb-4">Topics</h1>
    <v-row>
      <v-col cols="6" v-for="(topic, title) in topics">
        <v-card class="pa-5 mb-3 h-100">
          <div class="mb-5">
            <h2 class="font-weight-regular text-capitalize">
              {{ title }}
            </h2>
          </div>
          <div class="my-4">
            <span>{{ topic.count }} Articles</span>
          </div>
          <div>
            <h4 class="font-weight-light text-capitalize">Sub topics</h4>
            <VList :items="Object.keys(topic.subtopics)" />
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
