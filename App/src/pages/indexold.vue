<script setup>
import { onMounted } from "vue";

import { PerfectScrollbar } from "vue3-perfect-scrollbar";

import { usePostsStore } from "@/stores/usePostsStore";
const store = usePostsStore();

import { useNavBarStore } from "@/stores/useNavBarStore";
const NavBarStore = useNavBarStore();

import { usePostOpenStore } from "@/stores/usePostOpenStore";
const PostOpenStore = usePostOpenStore();

const toggleView = () => {
  store.toggleView();
};

const post_list_scrollbar = ref();

const loadData = async () => {
  if (store.endLoad == true) return;

  try {
    await store.loadPosts();
  } catch (error) {
    console.error("Failed to load data:", error);
  } finally {
    //loading.value = false;
  }
};

const postSendDialogVisible = ref(false);

const postSend = ref(null);

const onScroll = (e) => {
  const { scrollTop, scrollHeight, clientHeight } = e.target;

  if (scrollTop + clientHeight >= scrollHeight - 50) {
    loadData();
  }
};

const openPost = async (post) => {
  await PostOpenStore.update(post);
  post.read = true;
  markAsReadPost({ article_id: post.id, value: true });

  NavBarStore.close();
};

const actionPost = async (action, post) => {
  // mark as read
  if (action == "mark_as_read") {
    if (post.read == true) {
      post.read = false;
      markAsReadPost({ article_id: post.id, value: false });
    } else {
      post.read = true;
      markAsReadPost({ article_id: post.id, value: true });
    }
  }

  // open
  if (action == "open") {
    if (post.url != null) {
      window.open(post.url, "_blank");
    }
  }

  // send
  if (action == "send") {
    postSend.value = post;
    postSendDialogVisible.value = true;
  }
};

const closePost = () => {
  PostOpenStore.reset();
  NavBarStore.open();
};

const closeDialog = () => {
  postSendDialogVisible.value = false;
};

const nextPost = async () => {
  let target;
  if (store.viewType == "list") {
    target = "li.open";
  } else {
    target = "div.cards-col.open";
  }
  const next = document.querySelector(target).nextElementSibling;
  if (next != null) {
    const next_id = next.getAttribute("data-id");
    const next_post = store.posts.find((item) => item.id === next_id);
    await openPost(next_post);
    next.scrollIntoView({
      behavior: "instant",
      block: "center",
    });
  }
};

const previousPost = async () => {
  let target;
  if (store.viewType == "list") {
    target = "li.open";
  } else {
    target = "div.cards-col.open";
  }
  const previous = document.querySelector(target).previousElementSibling;
  if (previous != null) {
    const previous_id = previous.getAttribute("data-id");
    const previous_post = JSON.parse(
      JSON.stringify(store.posts.filter((item) => item.id === previous_id))
    );
    await openPost(previous_post[0]);
    previous.scrollIntoView({
      behavior: "instant",
      block: "center",
    });
  }
};

onMounted(async () => {
  store.initialize();

  await store.refreshPosts();
});

//layout-vertical-nav overlay-nav
//layout-wrapper layout-nav-type-vertical layout-navbar-sticky layout-footer-static layout-content-width-fluid layout-content-height-fixed
//layout-wrapper layout-nav-type-vertical layout-navbar-sticky layout-footer-static layout-content-width-fluid layout-overlay-nav layout-content-height-fixed
//id="vertical-nav-toggle-btn"
</script>

<template>
  <VLayout class="email-app-layout">
    <VMain>
      <v-row class="h-100">
        <v-col class="h-100" :cols="PostOpenStore.post == null ? 12 : 4">
          <VCard
            flat
            class="email-content-list h-100 d-flex flex-column border-sm"
          >
            <!-- 👉 post list header -->
            <div class="news-header d-flex align-center px-4 py-5">
              <v-row class="" justify="space-between">
                <v-col cols="auto">
                  <div
                    v-if="store.current_title != null"
                    class="d-flex align-center"
                  >
                    <VBtn variant="text" class="btn-dossier" color="black">
                      <v-icon
                        v-if="store.dossier != null"
                        class="me-4"
                        icon="mdi-folder-check-outline"
                      ></v-icon>
                      <v-icon
                        v-if="store.acteur != null"
                        class="me-4"
                        icon="mdi-account-check-outline"
                      ></v-icon>
                      <span v-if="store.current_title != null">{{
                        store.current_title
                      }}</span>
                    </VBtn>
                    <VBadge
                      :content="store.total_unread + '/' + store.total"
                      color="error"
                    >
                      <VIcon
                        size="25"
                        icon="tabler-bell-filled"
                        color="warning"
                      />
                    </VBadge>
                  </div>
                </v-col>
                <v-col cols="auto">
                  <div class="d-flex align-center">
                    <div class="me-4" v-if="store.current_title != null">
                      <span
                        >page {{ store.next_page / store.size }} sur
                        {{ Math.ceil(store.total / store.size) }}</span
                      >
                    </div>

                    <div
                      class="news-lis-tools"
                      v-if="store.current_title != null"
                    >
                      <div>
                        <VBtn
                          v-if="store.viewType == 'list'"
                          variant="outlined"
                          color="secondary"
                          @click="toggleView()"
                        >
                          <v-icon
                            class="me-2"
                            icon="tabler-list-details"
                          ></v-icon>
                          Liste
                        </VBtn>
                        <VBtn
                          v-if="store.viewType == 'cards'"
                          variant="outlined"
                          color="secondary"
                          @click="toggleView()"
                        >
                          <v-icon
                            class="me-2"
                            icon="tabler-layout-grid"
                          ></v-icon>
                          Cards
                        </VBtn>
                      </div>
                    </div>
                  </div>
                </v-col>
              </v-row>
            </div>

            <VDivider />

            <!-- 👉 post list -->

            <PerfectScrollbar
              ref="post_list_scrollbar"
              @ps-scroll-y="onScroll"
              tag="ul"
              :options="{ suppressScrollX: true, wheelPropagation: false }"
              class="email-list"
            >
              <!--  list view -->
              <div v-if="store.viewType == 'list'">
                <ListView
                  @openPost="openPost"
                  @actionPost="actionPost"
                  :posts="store.posts"
                  :openPost="PostOpenStore.post"
                >
                </ListView>
              </div>

              <!--  cards view -->
              <div v-if="store.viewType == 'cards'" class="pa-4">
                <v-row>
                  <CardView
                    @openPost="openPost"
                    @actionPost="actionPost"
                    :posts="store.posts"
                    :openPost="PostOpenStore.post"
                  ></CardView>
                </v-row>
              </div>

              <!--  loading icon -->
              <div
                style="min-height: 50px; width: 100%"
                class="d-flex justify-center"
              >
                <VProgressCircular
                  class="my-5"
                  :class="store.$state.loading == true ? 'd-block' : 'd-none'"
                  :size="40"
                  color="primary"
                  indeterminate
                />
              </div>
            </PerfectScrollbar>
          </VCard>
        </v-col>
        <v-col
          v-if="PostOpenStore.post != null"
          class="h-100"
          :class="{ 'd-none': !PostOpenStore.post }"
          cols="8"
        >
          <!--  article open -->
          <ArticleView
            :post="PostOpenStore.post"
            @previousPost="previousPost"
            @closePost="closePost"
            @nextPost="nextPost"
            @actionPost="actionPost"
          ></ArticleView>
        </v-col>
      </v-row>
    </VMain>
  </VLayout>
</template>

<route lang="yml">
meta:
  layoutWrapperClasses: layout-content-height-fixed
</route>

<style lang="scss">
@use "@styles/variables/_vuetify.scss";
@use "@core/scss/base/_mixins.scss";
@import url("https://fonts.googleapis.com/css2?family=Cairo:wght@200..1000&family=Noto+Kufi+Arabic:wght@100..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:ital,wght@0,100..700;1,100..700&display=swap");
// Remove border. Using variant plain cause UI issue, caret isn't align in center

body {
  font-family: "IBM Plex Sans", sans-serif;
}

.news-header {
  .btn-dossier {
    cursor: auto;
  }

  .btn-dossier:hover .v-btn__overlay {
    opacity: 0 !important;
  }
}

.email-app-layout {
  box-shadow: none !important;
  border-radius: vuetify.$card-border-radius;

  @include mixins.elevation(vuetify.$card-elevation);

  $sel-email-app-layout: &;

  @at-root {
    .skin--bordered {
      @include mixins.bordered-skin($sel-email-app-layout);
    }
  }
}

.email-content-list {
  border-end-start-radius: 0;
  border-start-start-radius: 0;
}

.email-list {
  white-space: nowrap;

  .email-item {
    block-size: 3.75rem;
    transition: all 0.2s ease-in-out;
    will-change: transform, box-shadow;

    &.email-read {
      background-color: rgba(var(--v-theme-on-surface), var(--v-hover-opacity));
    }

    & + .email-item {
      border-block-start: 1px solid
        rgba(var(--v-border-color), var(--v-border-opacity));
    }
  }

  .email-item:hover {
    transform: translateY(-2px);

    @include mixins.elevation(3);

    .email-actions {
      display: block !important;
    }

    .email-meta {
      display: none;
    }

    + .email-item {
      border-color: transparent;
    }

    @media screen and (max-width: 600px) {
      .email-actions {
        display: none !important;
      }
    }
  }
}
</style>
