<script setup>
import { onMounted } from 'vue'
import { useHealthStore } from '../stores/health'

const health = useHealthStore()

onMounted(() => {
  health.check()
})
</script>

<template>
  <main class="min-h-screen flex flex-col items-center justify-center px-6">
    <div class="w-full max-w-md">
      <p class="text-sm font-medium text-muted tracking-wide uppercase">Pink Wheels</p>
      <h1 class="mt-2 text-4xl font-semibold text-teal-deep">Safe rides. Fair prices.</h1>
      <p class="mt-4 text-muted">
        A women-only bike ride-hailing platform for Karachi. Currently under development.
      </p>

      <div class="mt-10 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-sage/40">
        <h2 class="text-sm font-semibold text-ink">System status</h2>
        <dl class="mt-4 space-y-3 text-sm">
          <div class="flex items-center justify-between">
            <dt class="text-muted">Backend API</dt>
            <dd
              class="font-medium"
              :class="health.status === 'ok' ? 'text-teal-deep' : 'text-red-600'"
            >
              {{ health.loading ? 'Checking…' : health.status || 'Not checked' }}
            </dd>
          </div>
          <div class="flex items-center justify-between">
            <dt class="text-muted">Database</dt>
            <dd
              class="font-medium"
              :class="health.database === 'connected' ? 'text-teal-deep' : 'text-red-600'"
            >
              {{ health.loading ? 'Checking…' : health.database || 'Unknown' }}
            </dd>
          </div>
        </dl>
        <p v-if="health.error" class="mt-3 text-xs text-red-600">{{ health.error }}</p>
        <button
          type="button"
          class="mt-6 w-full rounded-xl bg-teal-deep px-4 py-2.5 text-sm font-medium text-white hover:bg-teal-deep/90"
          @click="health.check()"
        >
          Re-check connection
        </button>
      </div>
    </div>
  </main>
</template>
