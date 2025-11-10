<script setup>
import { injectionKeyIsVerticalNavHovered, useLayouts } from "@layouts";
import {
  VerticalNavGroup,
  VerticalNavLink,
  VerticalNavSectionTitle,
} from "@layouts/components";
import { config } from "@layouts/config";
import { onMounted, ref } from "vue";
import { PerfectScrollbar } from "vue3-perfect-scrollbar";
import { VNodeRenderer } from "./VNodeRenderer";

// init filter
import { useFilterStore } from "@/stores/useFilterStore";
const store = useFilterStore();

import { usePostOpenStore } from "@/stores/usePostOpenStore";
const PostOpenStore = usePostOpenStore();

import { usePostsStore } from "@/stores/usePostsStore";

const storePosts = usePostsStore();

import { useNavBarStore } from "@/stores/useNavBarStore";
const NavBarStore = useNavBarStore();

const closeNavbar = ref(false);

const selectSource = (source) => {
  store.updateFilter("source", source);
};

const clearSearchQuery = () => {
  store.updateFilter("searchQuery", "");
};

const refresh = async () => {
  console.log(store.source);
  if (store.source != null) {
    NavBarStore.open();
    const rawState = toRaw(store.$state);
    const allFields = JSON.parse(JSON.stringify(rawState));
    PostOpenStore.reset();
    await storePosts.refreshFilter(allFields);
  }
};

const props = defineProps({
  tag: {
    type: [String, null],
    required: false,
    default: "aside",
  },
  navItems: {
    type: null,
    required: true,
  },
  isOverlayNavActive: {
    type: Boolean,
    required: true,
  },
  toggleIsOverlayNavActive: {
    type: Function,
    required: true,
  },
});

const refNav = ref();
const { width: windowWidth } = useWindowSize();
const isHovered = useElementHover(refNav);

provide(injectionKeyIsVerticalNavHovered, isHovered);

const {
  isVerticalNavCollapsed: isCollapsed,
  isLessThanOverlayNavBreakpoint,
  isVerticalNavMini,
  isAppRtl,
} = useLayouts();

const hideTitleAndIcon = isVerticalNavMini(windowWidth, isHovered);

const resolveNavItemComponent = (item) => {
  if ("heading" in item) return VerticalNavSectionTitle;
  if ("children" in item) return VerticalNavGroup;

  return VerticalNavLink;
};

const route = useRoute();

watch(
  () => route.name,
  () => {
    props.toggleIsOverlayNavActive(false);
  }
);

const isVerticalNavScrolled = ref(false);
const updateIsVerticalNavScrolled = (val) =>
  (isVerticalNavScrolled.value = val);

const handleNavScroll = (evt) => {
  isVerticalNavScrolled.value = evt.target.scrollTop > 0;
};

const handleClickOutside = (event) => {
  if (refNav.value && refNav.value.classList.contains("visible")) {
    if (refNav.value && !refNav.value.contains(event.target)) {
      props.toggleIsOverlayNavActive(false);
    }
  }
};

onMounted(() => {
  if (document.querySelector("main.layout-page-content") != null) {
    document
      .querySelector("main.layout-page-content")
      .addEventListener("click", handleClickOutside);
  }
  const rawState = toRaw(storePosts.$state);
  const allFields = JSON.parse(JSON.stringify(rawState));
  store.initialize(allFields);
});

onBeforeUnmount(() => {
  document.removeEventListener("click", handleClickOutside);
});

isCollapsed.value = false;
</script>

<template>
  <Component
    :is="props.tag"
    ref="refNav"
    id="asideNavBar"
    class="layout-vertical-nav"
    :class="[
      {
        'overlay-nav':
          closeNavbar == true || isLessThanOverlayNavBreakpoint(windowWidth),
        hovered: isHovered,
        visible: isOverlayNavActive,
        scrolled: isVerticalNavScrolled,
      },
    ]"
  >
    <!-- 👉 Header -->
    <div class="nav-header">
      <slot name="nav-header">
        <RouterLink
          to="/"
          class="app-logo d-flex align-center gap-x-1 app-title-wrapper"
        >
          <VNodeRenderer :nodes="config.app.logo" />

          <Transition name="vertical-nav-app-title">
            <h1
              v-show="!hideTitleAndIcon"
              class="app-title font-weight-bold text-capitalize leading-normal text-xl"
            >
              {{ config.app.title }}
            </h1>
          </Transition>
        </RouterLink>
        <!-- 👉 Vertical nav actions -->
        <!-- Show toggle collapsible in >md and close button in <md -->
        <template v-if="!isLessThanOverlayNavBreakpoint(windowWidth)">
          <!--
          <Component :is="config.app.iconRenderer || 'div'" v-show="isCollapsed && !hideTitleAndIcon"
            class="header-action" v-bind="config.icons.verticalNavUnPinned" @click="isCollapsed = !isCollapsed" />
          <Component :is="config.app.iconRenderer || 'div'" v-show="!isCollapsed && !hideTitleAndIcon"
            class="header-action" v-bind="config.icons.verticalNavPinned" @click="isCollapsed = !isCollapsed" />
            -->
        </template>
        <template v-else>
          <Component
            :is="config.app.iconRenderer || 'div'"
            class="header-action"
            v-bind="config.icons.close"
            @click="toggleIsOverlayNavActive(false)"
          />
        </template>
        <!--
        <v-btn @click="closeAside" icon="tabler-x" size="sm" class="pa-1" variant="tonal"
          style="color:white !important">
        </v-btn>
        -->
      </slot>
    </div>
    <slot name="before-nav-items">
      <div class="vertical-nav-items-shadow" />
    </slot>
    <slot
      name="nav-items"
      :update-is-vertical-nav-scrolled="updateIsVerticalNavScrolled"
    >
      <PerfectScrollbar
        :key="isAppRtl"
        tag="ul"
        class="nav-items"
        :options="{ wheelPropagation: false }"
        @ps-scroll-y="handleNavScroll"
      >
        <div id="sideBarMenu">
          <div class="sources mb-4">
            <h3 class="py-3 ps-4 d-flex">
              <VIcon
                icon="tabler-folder"
                class="me-3 section-icon"
                size="small"
              />
              <span class="section-title">Sources</span>
            </h3>
            <div class="section-content">
              <v-list-item
                v-for="source in store.sources"
                :title="source.source_name"
                @click="selectSource(source)"
                class="source-item"
                :class="
                  store.source != null && store.source.id == source.id
                    ? 'active'
                    : ''
                "
              >
                <template v-slot:append>
                  <v-icon
                    icon="mdi-check-circle"
                    v-if="store.source != null && store.source.id == source.id"
                  ></v-icon>
                </template>
              </v-list-item>
            </div>
          </div>
          <v-divider></v-divider>
          <div class="tri mb-5">
            <h3 class="py-3 ps-4 mb-2 d-flex">
              <VIcon
                icon="tabler-arrows-down-up"
                class="me-3 section-icon"
                size="small"
              />
              <span class="section-title">Tri</span>
            </h3>
            <div class="section-content">
              <v-radio-group class="mx-2 mb-2 mb-0" v-model="store.tri">
                <v-radio label="Tri par date" value="date"></v-radio>
                <v-radio
                  label="Tri par pertinence"
                  value="pertinence"
                ></v-radio>
              </v-radio-group>
            </div>
          </div>
          <v-divider></v-divider>
          <div class="date-range mb-5">
            <h3 class="py-3 ps-4 mb-2 d-flex">
              <VIcon
                icon="tabler-calendar-week"
                class="me-3 section-icon"
                size="small"
                tag="i"
              /><span class="section-title">Période</span>
            </h3>
            <div class="section-content">
              <v-select
                class="mx-2"
                :items="[
                  { value: 1, title: 'Moins d\'une heure' },
                  { value: 24, title: 'Moins de 24 heures' },
                  { value: 48, title: 'Moins de 48 heures' },
                  { value: 168, title: 'Moins d\'une semaine' },
                  { value: 720, title: 'Moins d\'un mois' },
                  { value: 8760, title: 'Moins d\'un an' },
                  { value: 0, title: 'Tout' },
                ]"
                item-title="title"
                item-value="value"
                v-model="store.window"
                variant="outlined"
                hide-details
              ></v-select>
            </div>
          </div>
          <v-divider></v-divider>
          <div class="date-range mb-5">
            <h3 class="py-3 ps-4 mb-2 d-flex">
              <VIcon
                icon="tabler-search"
                class="me-3 section-icon"
                size="small"
                tag="i"
              /><span class="section-title">Recherche</span>
            </h3>
            <div class="section-content">
              <AppTextField
                clearable
                class="mx-2"
                id="firstName"
                v-model="store.searchQuery"
                @click:clear="clearSearchQuery"
              />
            </div>
          </div>
          <v-divider></v-divider>
          <div class="refresh d-flex justify-center mt-5">
            <VBtn color="primary" @click="refresh()">
              <VIcon start icon="tabler-refresh" />Actualiser
            </VBtn>
          </div>
        </div>
      </PerfectScrollbar>
    </slot>
  </Component>
</template>

<style lang="scss">
@use "@configured-variables" as variables;
@use "@layouts/styles/mixins";

// my style

.source-item.active {
  color: rgb(var(--v-theme-primary));
}

.acteur-item.active {
  color: rgb(var(--v-theme-primary));
}

.platformes-item {
  width: fit-content;
  border-radius: 50%;
  border: 2px solid transparent !important;
  cursor: pointer;
}

.platformes-item.active {
  width: fit-content;
  border-radius: 50%;
  border: 2px solid rgb(var(--v-theme-primary)) !important;
}

.platformes-item:hover {
  width: fit-content;
  border-radius: 50%;
  border: 2px solid rgb(var(--v-theme-primary)) !important;
}

.section-title {
  overflow: hidden;
}

.layout-vertical-nav-collapsed .layout-vertical-nav #sideBarMenu {
  display: none;
}

.layout-vertical-nav-collapsed .layout-vertical-nav.hovered #sideBarMenu {
  display: block;
}

// 👉 Vertical Nav
.layout-vertical-nav {
  position: fixed;
  z-index: variables.$layout-vertical-nav-z-index;
  display: flex;
  flex-direction: column;
  block-size: 100%;
  inline-size: variables.$layout-vertical-nav-width;
  inset-block-start: 0;
  inset-inline-start: 0;
  transition: transform 0.25s ease-in-out, inline-size 0.25s ease-in-out,
    box-shadow 0.25s ease-in-out;
  will-change: transform, inline-size;

  .nav-header {
    display: flex;
    align-items: center;

    .header-action {
      cursor: pointer;
    }
  }

  .app-title-wrapper {
    margin-inline-end: auto;
  }

  .nav-items {
    block-size: 100%;

    // ℹ️ We no loner needs this overflow styles as perfect scrollbar applies it
    // overflow-x: hidden;

    // // ℹ️ We used `overflow-y` instead of `overflow` to mitigate overflow x. Revert back if any issue found.
    // overflow-y: auto;
  }

  .nav-item-title {
    overflow: hidden;
    margin-inline-end: auto;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  // 👉 Collapsed
  .layout-vertical-nav-collapsed & {
    &:not(.hovered) {
      inline-size: variables.$layout-vertical-nav-collapsed-width;
    }
  }

  // 👉 Overlay nav
  &.overlay-nav {
    &:not(.visible) {
      transform: translateX(-#{variables.$layout-vertical-nav-width});

      @include mixins.rtl {
        transform: translateX(variables.$layout-vertical-nav-width);
      }
    }
  }
}
</style>
