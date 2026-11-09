<template>
  <div class="min-h-screen flex flex-col bg-[#F2F5F1] text-[#26332E]">
    <Navbar />
    <main class="flex-1">
      <router-view />
    </main>
    <footer class="bg-white border-t border-[#A9BDAE]/40 py-4 text-center text-xs text-[#77817B]">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <p><strong>Pink Wheels</strong> — Safe rides. Fair prices. • University DSA Project</p>
        <p class="font-mono text-[11px]">Structures: Linked List | Queue | Min-Heap Priority Queue | Stack</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Navbar from './components/common/Navbar.vue'
</script>
