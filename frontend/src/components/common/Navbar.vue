<template>
  <header class="bg-[#174C43] text-white shadow-md sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Title -->
        <router-link to="/" class="flex items-center space-x-3 group">
          <div class="w-10 h-10 rounded-full bg-[#A9BDAE] flex items-center justify-center text-[#174C43] font-bold text-xl shadow-inner group-hover:scale-105 transition-transform">
            🛵
          </div>
          <div>
            <div class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
              Pink Wheels
              <span class="text-[10px] uppercase font-semibold px-2 py-0.5 rounded bg-[#A9BDAE]/20 text-[#A9BDAE] border border-[#A9BDAE]/30">DSA Project</span>
            </div>
            <p class="text-xs text-[#A9BDAE]">Safe rides. Fair prices. (Karachi Demo)</p>
          </div>
        </router-link>

        <!-- Role Switcher (No Auth / Simple Demo Switching) -->
        <nav class="flex items-center space-x-1 sm:space-x-2 bg-black/20 p-1 rounded-xl">
          <router-link
            to="/passenger"
            class="px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5"
            :class="$route.path.startsWith('/passenger') ? 'bg-white text-[#174C43] shadow-sm font-semibold' : 'text-[#A9BDAE] hover:text-white hover:bg-white/10'"
          >
            <span>👩</span>
            <span>Passenger</span>
          </router-link>

          <router-link
            to="/driver"
            class="px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5"
            :class="$route.path.startsWith('/driver') ? 'bg-white text-[#174C43] shadow-sm font-semibold' : 'text-[#A9BDAE] hover:text-white hover:bg-white/10'"
          >
            <span>🛵</span>
            <span>Driver</span>
          </router-link>

          <router-link
            to="/admin/dsa"
            class="px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors flex items-center gap-1.5"
            :class="$route.path.startsWith('/admin') ? 'bg-white text-[#174C43] shadow-sm font-semibold' : 'text-[#A9BDAE] hover:text-white hover:bg-white/10'"
          >
            <span>🧠</span>
            <span>DSA Dashboard</span>
          </router-link>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
</script>
