<template>
  <div class="min-h-screen">
    <LandingHeader />

    <main>
      <HeroSection />

      <StatsSection :courses-count="courses.length" />

      <CoursesSection :courses="courses" :loading="loading" />

      <FeaturesSection />
    </main>

    <LandingFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPublicCourses } from '@/api/public.js'
import LandingHeader   from '@/components/landing/LandingHeader.vue'
import HeroSection     from '@/components/landing/HeroSection.vue'
import StatsSection    from '@/components/landing/StatsSection.vue'
import CoursesSection  from '@/components/landing/CoursesSection.vue'
import FeaturesSection from '@/components/landing/FeaturesSection.vue'
import LandingFooter   from '@/components/landing/LandingFooter.vue'

const courses = ref([])
const loading = ref(true)

onMounted(async () => {
  courses.value = await getPublicCourses()
  loading.value = false
})
</script>

<style>
/* Global smooth scroll — LandingView uchun */
html {
  scroll-behavior: smooth;
}
</style>
