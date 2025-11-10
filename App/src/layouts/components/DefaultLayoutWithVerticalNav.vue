<script setup>
import navItems from "@/navigation/vertical";
import { useThemeConfig } from "@core/composable/useThemeConfig";

// Components
import Footer from "@/layouts/components/Footer.vue";
import NavBarNotifications from "@/layouts/components/NavBarNotifications.vue";
import NavbarThemeSwitcher from "@/layouts/components/NavbarThemeSwitcher.vue";

import UserProfile from "@/layouts/components/UserProfile.vue";
// @layouts plugin
import { VerticalNavLayout } from "@layouts";
const { appRouteTransition, isLessThanOverlayNavBreakpoint } = useThemeConfig();
const { width: windowWidth } = useWindowSize();

import { useNavBarStore } from "@/stores/useNavBarStore";
const NavBarStore = useNavBarStore();
</script>

<template>
  <VerticalNavLayout :nav-items="navItems">
    <!-- 👉 navbar -->
    <template #navbar="{ toggleVerticalOverlayNavActive }">
      <div class="d-flex h-100 align-center">
        <IconBtn
          v-if="isLessThanOverlayNavBreakpoint(windowWidth)"
          id="vertical-nav-toggle-btn"
          class="ms-n3 me-4"
          @click="toggleVerticalOverlayNavActive(true)"
        >
          <VIcon size="26" icon="tabler-menu-2" />
        </IconBtn>

        <!-- 👉 Vertical nav actions -->

        <VSpacer />
        <!--<NavbarThemeSwitcher class="me-1" />-->
        <!--<NavBarNotifications class="me-2" />-->
        <UserProfile />
      </div>
    </template>

    <!-- 👉 Pages -->
    <RouterView v-slot="{ Component }">
      <Transition :name="appRouteTransition" mode="out-in">
        <Component :is="Component" />
      </Transition>
    </RouterView>

    <!-- 👉 Footer -->
    <template #footer>
      <Footer />
    </template>

    <!-- 👉 Customizer -->
    <!-- <TheCustomizer /> -->
  </VerticalNavLayout>
</template>

<style lang="scss" scoped>
.nav-header-container {
  background-color: rgb(var(--v-theme-surface)) !important;
}
</style>
