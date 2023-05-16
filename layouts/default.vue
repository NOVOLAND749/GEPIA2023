<template>
  <div>
    <header>
      <Navbar class="bg-white shadow-md">
        <template #logo>
          <NuxtLink to="/">
            <NavbarLogo
              alt="GEPIA logo"
              imageUrl="http://gepia.cancer-pku.cn/assets/logo/faviconb.png"
              class="h-full"
            />
          </NuxtLink>
        </template>
        <template #default="{ isShowMenu }">
          <NavbarCollapse :isShowMenu="isShowMenu">
            <NuxtLink to="/">
              <NavbarLink>Home</NavbarLink>
            </NuxtLink>
            <NuxtLink to="/about">
              <NavbarLink>About</NavbarLink>
            </NuxtLink>
            <NuxtLink to="/contact">
              <NavbarLink>Contact</NavbarLink>
            </NuxtLink>
          </NavbarCollapse>
        </template>
      </Navbar>
    </header>

    <Sidebar />

    <div class="mb-20">
      <slot></slot>
    </div>

    <footer
      class="fixed bottom-0 z-20 border-t w-full bg-transparent backdrop-blur-sm shadow-3xl"
    >
      <div class="w-full mx-auto p-6 text-center">
        2023 &copy; Yifei Hu, Nan Huang. All rights reserved.
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import {
  Navbar,
  NavbarLogo,
  NavbarCollapse,
  NavbarLink,
  Footer,
} from "flowbite-vue";
</script>

<style scoped></style>
