<script setup>
import { detectLanguage, timestampToDate } from '@utils';
import { defineEmits, defineProps } from 'vue';
import { PerfectScrollbar } from 'vue3-perfect-scrollbar';

const props = defineProps({
    post: Object, // Define the prop to accept data from the parent
});

const emit = defineEmits(['previousPost', 'closePost', 'nextPost', 'actionPost']);

function previousPost() {
    emit('previousPost'); // Emit the event to the parent
}
function closePost() {
    emit('closePost'); // Emit the event to the parent
}
function nextPost() {
    emit('nextPost'); // Emit the event to the parent
}
function handleActionClick(action, post) {
    emit('actionPost', action, post); // Emit the event to the parent
}
</script>
<template>
    <v-row class=" " style="height: 101%;">
        <v-col class="h-100 pb-0" cols="8">
            <VCard flat class="border-sm h-100 d-flex flex-column">
                <div class="navigate-posts position-relative ">
                    <VBtn size="large" variant="plain" class="btn-left pa-2" @click="previousPost()">
                        <v-icon icon="tabler-arrow-narrow-left"></v-icon>
                    </VBtn>
                    <VBtn size="large" variant="plain" class="btn-close pa-2" @click="closePost()">
                        <v-icon icon="mdi-close"></v-icon>
                    </VBtn>
                    <VBtn size="large" variant="plain" class="btn-right pa-2" @click="nextPost()">
                        <v-icon icon="tabler-arrow-narrow-right"></v-icon>
                    </VBtn>
                </div>


                <VDivider />
                <PerfectScrollbar :options="{ suppressScrollX: true, wheelPropagation: false }">
                    <article class="mx-5 my-8 article-open">

                        <h1 class="text-center mx-4 article-title" :dir="detectLanguage(post.title)"
                            v-html="post.title">
                        </h1>
                        <v-img class="article-img mt-5" max-height="450px" aspect-ratio="16/9" cover
                            :src="post.media_content"></v-img>
                        <div class="article-meta mt-5 d-flex justify-space-between">
                            <div class="d-flex align-center">
                                <VIcon icon="tabler-calendar" />
                                <span class="text-disabled ms-3">{{ timestampToDate(post.published)
                                    }}</span>
                            </div>
                            <div class="article-actions">
                                <IconBtn @click.stop="handleActionClick('mark_as_read', post)">
                                    <VIcon :icon="post.read ? 'tabler-eye-off' : 'tabler-eye'" />
                                    <VTooltip activator="parent" location="top">
                                        {{ post.read ? 'Marquer comme lu' : 'Marquer comme non lu' }}
                                    </VTooltip>
                                </IconBtn>
                                <IconBtn @click.stop="handleActionClick('pin', post)">
                                    <VIcon icon="tabler-pin" />
                                    <VTooltip activator="parent" location="top">
                                        Épingler
                                    </VTooltip>
                                </IconBtn>
                                <IconBtn @click.stop="handleActionClick('open', post)">
                                    <VIcon icon="tabler-external-link" />
                                    <VTooltip activator="parent" location="top">
                                        Ouvrir
                                    </VTooltip>
                                </IconBtn>
                                <IconBtn @click.stop="handleActionClick('send', post)">
                                    <VIcon icon="tabler-send" />
                                    <VTooltip activator="parent" location="top">
                                        Signaler
                                    </VTooltip>
                                </IconBtn>
                            </div>

                        </div>
                        <div class="article-content mt-4" :dir="detectLanguage(post.content)" v-html="post.content">
                        </div>

                    </article>
                </PerfectScrollbar>


            </VCard>
        </v-col>
        <v-col cols="4">
            <VCard flat class="pa-6 border-sm">
                <div>
                    <v-img class="article-img mt-5" max-height="180px" aspect-ratio="16/9"
                        :src="post.source_image"></v-img>
                </div>
                <div class="mt-4">
                    <h2 class="text-center" :dir="detectLanguage(post.source_name)" v-html="post.source_name">
                    </h2>
                </div>

            </VCard>
        </v-col>
    </v-row>
</template>

<style lang="scss">
.navigate-posts {
    margin-bottom: 50px;
}

.navigate-posts .btn-right {
    border-radius: 0;
    position: absolute;
    top: 0px;
    left: 50px;
}

.navigate-posts .btn-left {
    border-radius: 0;
    position: absolute;
    top: 0px;
    left: 0px;
}

.navigate-posts .btn-close {
    border-radius: 0;
    position: absolute;
    top: 0px;
    right: 0px;
}


article.article-open {
    position: relative;


    b {
        text-decoration-line: underline;
        text-decoration-color: rgb(var(--v-theme-primary));
    }

    .article-content {
        font-size: 1.3rem;
        font-weight: 400;
        line-height: normal;
        text-align: justify;


    }


}
</style>