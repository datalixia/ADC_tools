<script setup>
import not_found from "@images/plateformes/not_found.jpg"; // Default icon
import { detectLanguage, getIconPlateformes, getIconSource, timestampToDate } from '@utils';
import { defineEmits, defineProps } from 'vue';

const props = defineProps({
    posts: Array, // Define the prop to accept data from the parent
    openPost: Object,
});
// Define an emit event
const emit = defineEmits(['openPost', 'actionPost']);

function clickPost(post) {
    emit('openPost', post); // Emit the event to the parent
}
function handleActionClick(action, post) {
    emit('actionPost', action, post); // Emit the event to the parent
}

</script>
<template>
    <!-- :breakpoint=" open : notOpen" -->
    <v-col class="cards-col" :data-id="post.id" @click="clickPost(post)" v-for="post in posts" cols="12"
        :xxl="openPost != null ? 4 : 2" :xl="openPost != null ? 6 : 3" :lg="openPost != null ? 12 : 4"
        :md="openPost != null ? 12 : 6" :sm="openPost != null ? 12 : 12" :class="[{ 'post-read': post.read }, {
            'open': openPost != null && openPost.id === post.id
        }]">
        <VCard class="cards-item h-100">
            <div class="plat pa-1">
                <v-avatar class="border" :image="getIconPlateformes(post.plateforme)" size="30"></v-avatar>
            </div>
            <div class="cards-tools">
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
            <VImg class="cards-img" v-if="post.media_content" :src="post.media_content" cover />
            <VImg class="cards-img" v-else :src="not_found" cover />
            <div class="card-body h-100 pa-4">

                <div class="card-content-meta mt-3 mb-5 d-flex align-center justify-space-between">
                    <div class="source pa-1 me-auto">
                        <VAvatar class="mx-0" size="30">
                            <VImg :src="getIconSource(post.source_id)" />
                        </VAvatar>
                    </div>
                    <div class="">
                        <span class="text-muted date">{{ timestampToDate(post.published) }}</span>
                    </div>

                </div>
                <div class="card-content-title">

                    <h3 v-if="post.title != null && post.title != ''" class="title" :dir="detectLanguage(post.title)"
                        v-html="post.title">
                    </h3>
                    <h3 v-else class="title" :dir="detectLanguage(post.content)" v-html="post.content"></h3>
                </div>
            </div>
        </VCard>
    </v-col>
</template>



<style lang="scss">
.cards-item {
    cursor: pointer;
    border: 1px solid rgba(144, 141, 141, 0.2) !important;

    .card-body {
        border: 1px solid rgba(144, 141, 141, 0.2) !important;

        .title b {
            text-decoration-line: underline !important;
            text-decoration-color: rgb(var(--v-theme-primary)) !important;
        }
    }

    .source {
        margin-right: 5px !important;
        margin-left: 5px !important;
        border-radius: 50%;
        border: 1px solid grey;
        background-color: white;
    }

    .source.open {
        border: 1px solid rgb(var(--v-theme-primary));
    }
}

.cards-item .v-img {
    height: 200px !important;
}

div.cards-col.post-read .cards-item {
    background-color: rgba(133, 133, 135, 0.27);

}

div.cards-col.open .cards-item {
    -webkit-box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);
    -moz-box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);
    box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);

}

div.cards-col.open .cards-item .plat {
    border: 3px solid rgb(var(--v-theme-primary));

}




.cards-item:hover .cards-tools {
    opacity: 1;
    visibility: visible !important;
}

.cards-item:hover .cards-img .v-img .v-responsive__sizer {
    background-color: rgba(0, 0, 0, 0.563);
}

.cards-item:hover {
    -webkit-box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);
    -moz-box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);
    box-shadow: -1px 1px 14px 10px rgba(47, 43, 61, 0.14);

}

.cards-item .plat {
    position: absolute;
    top: 5px;
    left: 5px;
    z-index: 100;
    background-color: rgba(58, 51, 51, 0.86);
    border-radius: 50%;
}

.cards-item .cards-tools {

    position: absolute;
    top: 5px;
    right: 5px;
    z-index: 100;
    color: white;

    opacity: 0;
    visibility: hidden;
    transition: opacity .5s ease;
}



.card-content-title .title {
    line-clamp: 3;
    -webkit-line-clamp: 3;
    white-space: pre-wrap;
    overflow: clip;
    display: -webkit-box;
    -webkit-box-orient: vertical;

}
</style>