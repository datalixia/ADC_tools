<script setup>
import {
  detectLanguage,
  getIconPlateformes,
  getIconSource,
  timestampToDate,
} from "@utils";

import { markasread, analyze_article, article_ner } from "@apis";


const props = defineProps({
  posts: Array, // Define the prop to accept data from the parent
});


const openedpost = ref(null);
const dialog = ref(false);
const openedPostAnalyze = ref(null);
const openedPostNER = ref(null);
const openPost = async (post) => {
  const result = await analyze_article(post)
  openedPostAnalyze.value = result

  const ner_result = await article_ner(post)
  openedPostNER.value = ner_result
  console.log(openedPostNER.value.entities)

  openedpost.value = post;
  dialog.value = true;
};

const source_logo = (source) => {
  const iconFileName = source + ".png";
  const iconName = "/src/assets/images/sources/" + iconFileName;
  const iconModule = new URL(iconName, import.meta.url).href;
  return iconModule || iconSocial;
};


const formatTimestamp = (timestamp) => {
  // Create a new Date object from the timestamp
  const date = new Date(timestamp);

  // Use toLocaleDateString with options for YYYY-MM-DD format
  return date.toLocaleDateString('en-CA'); // 'en-CA' gives the format YYYY-MM-DD
}


const handlemarkasread = (post) => {
  post.read = true;

  markasread(post.id);
}


</script>
<template>
  <v-dialog v-model="dialog" width="auto" class="post-dialog">
    <v-card class="py-5 px-7 position-relative" max-width="1200">
      <IconBtn class="position-absolute" style="top:0;right:0;margin: 10px;" color="secondary" variant="tonal" @click="dialog = false">
              <VIcon  color="secondary" icon="tabler-x" />
            </IconBtn>
      <v-row>
        <v-col md="7" cols="12">
          <a :href="openedpost.url" target="_blank">
            <h2 class="font-weight-medium mb-3" v-html="openedpost.title">
            </h2>
          </a>
          <div class="mb-5 d-flex align-center">
            <VAvatar class="me-3" size="40">
              <VImg :src="source_logo(openedpost.source_name)" />
            </VAvatar>
            <h3 class="me-5 text-capitalize font-weight-medium">
              {{ openedpost.source_name }}
            </h3>
            <span>
              <v-icon icon="tabler-calendar-week" class="me-2"></v-icon>{{ timestampToDate(openedpost.date_time)
              }}</span>
          </div>

          <p v-html="openedpost.content"></p>
          <template v-slot:actions>
            <div class="d-flex justify-end w-100">
              <div>
                <v-btn variant="tonal" class="ms-auto mt-5 me-5" color="secondary" text="Mark as read"
                  @click="handlemarkasread(openedpost)"></v-btn>
              </div>
              <div>
                <v-btn variant="tonal" class="ms-auto mt-5" text="Close" @click="dialog = false"></v-btn>
              </div>

            </div>

          </template>
        </v-col>
        <v-col md="5" cols="12">
          <div class="border-s-sm h-100 pa-5">
            <div>
              <h2 class>Topics</h2>
              <v-list>
                <v-list-item v-for="(value, key) in Object.fromEntries(
                  Object.entries(openedPostAnalyze.analysis.topic_scores)
                    .sort((a, b) => b[1] - a[1])  // Sort by score (value) in descending order
                )" :key="value" :title="key" :value="key">
                  <template v-slot:append>
                    <v-badge color="info" :content="value" inline></v-badge>
                  </template></v-list-item>
              </v-list>
            </div>
            <div class="mt-6">
              <h2 class="my-2">Keywords</h2>
              <div>
                <v-chip-group>
                  <v-chip v-for="keyword in openedPostAnalyze.analysis.keywords">
                    {{ keyword }}
                  </v-chip>
                </v-chip-group>
              </div>
            </div>
            <div class="mt-6">
              <h2 class="my-2">Entities</h2>
              <div v-for="(entities, title) in openedPostNER.entities">
                <div v-if="entities.length > 0">
                  <h4 class="ms-3 font-weight-meduim">{{ title.replace('_',' ') }}</h4>
                <v-chip-group>
                  <v-chip variant="outlined" class="ms-2" v-for="entity in entities">
                    {{ entity.entity }}
                  </v-chip>
                </v-chip-group>
                </div>
                
              </div>
            </div>
          </div>
        </v-col>
      </v-row>

    </v-card>
  </v-dialog>


  <li v-for="post in posts" :key="post.id" :data-id="post.id"
    class="email-item d-flex align-center py-2 px-5 cursor-pointer" :class="[{ 'email-read': post.read }]"
    @click="openPost(post)">
    <div class="source pa-1">
      <VAvatar class="mx-0" size="40">
        <VImg :src="source_logo(post.source_name)" />
      </VAvatar>
    </div>
    <h6 class="font-weight-bold mx-3 text-body-1 font-weight-medium text-high-emphasis text-capitalize"
      v-html="post.source_name" :dir="detectLanguage(post.source_name)"></h6>
    <span v-if="post.title != null && post.title != ''" class="truncate" :dir="detectLanguage(post.title)"
      v-html="post.title"></span>
    <span v-else class="truncate" :dir="detectLanguage(post.content)" v-html="post.content"></span>
    <VSpacer />

    <div class="email-meta" :class="$vuetify.display.xs ? 'd-none' : 'd-block'">
      <small class="font-weight-black text-disabled text-sm ms-2">
        {{ timestampToDate(post.date_time) }}
      </small>
    </div>

  </li>
  <!--  loading icon -->


</template>

<style lang="scss">
@use "@styles/variables/_vuetify.scss";
@use "@core/scss/base/_mixins.scss";

.email-item {
  .source {
    margin-right: 5px !important;
    margin-left: 5px !important;
    border-radius: 50%;
    border: 1px solid grey;
  }

  .source.open {
    border: 1px solid rgb(var(--v-theme-primary));
  }

  .plat {
    margin-right: 5px !important;
    margin-left: 5px !important;
    border-radius: 50%;
    border: 1px solid grey;
    background-color: grey;
  }

  b {
    text-decoration-line: underline;
    text-decoration-color: rgb(var(--v-theme-primary));
  }
}

.post-dialog {
  b {
    text-decoration-line: underline;
    text-decoration-color: rgb(var(--v-theme-primary));
  }
}


.email-item {
  block-size: 3.75rem;
  transition: all 0.2s ease-in-out;
  will-change: transform, box-shadow;

  &.email-read {
    background-color: rgba(var(--v-theme-on-surface), var(--v-hover-opacity));
  }

  &+.email-item {
    border-block-start: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  }
}

.email-item.open {
  transform: translateY(-2px);

  @include mixins.elevation(3);

  .email-meta {
    display: none;
  }

  +.email-item {
    border-color: transparent;
  }

  @media screen and (max-width: 600px) {
    .email-actions {
      display: none !important;
    }
  }

  .source {
    border: 3px solid rgb(var(--v-theme-primary));
  }
}
</style>
