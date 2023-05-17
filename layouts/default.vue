<template>
  <div>
    <header>
      <Navbar
        class="fixed w-full bg-white bg-opacity-50 backdrop-blur-sm shadow-md z-50"
      >
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
              <NavbarLink>
                <Icon name="material-symbols:house" class="mb-0.5" /> Home
              </NavbarLink>
            </NuxtLink>
            <NuxtLink to="/about">
              <NavbarLink>
                <Icon name="material-symbols:info" class="mb-0.5" /> About
              </NavbarLink>
            </NuxtLink>
            <NuxtLink to="/contact">
              <NavbarLink>
                <Icon name="material-symbols:contact-support" class="mb-0.5" />
                Contact
              </NavbarLink>
            </NuxtLink>
          </NavbarCollapse>
        </template>
      </Navbar>
    </header>

    <Sidebar class="z-10" />

    <div class="py-20">
      <slot></slot>
    </div>

    <footer
      class="fixed bottom-0 z-50 border-t w-full bg-transparent bg-white bg-opacity-50 backdrop-blur-sm shadow-3xl"
    >
      <div class="w-full mx-auto p-4 text-center">
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
