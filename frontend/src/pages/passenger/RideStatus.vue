<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-[#174C43]">Live Ride Status</h1>
        <p class="text-sm text-[#77817B]">Tracking ride request #{{ rideId }}</p>
      </div>
      <router-link
        to="/passenger"
        class="text-xs font-semibold px-3 py-1.5 rounded-lg border border-[#A9BDAE] text-[#174C43] hover:bg-[#F2F5F1]"
      >
        ← Book Another Ride
      </router-link>
    </div>

    <div v-if="loading" class="bg-white p-8 rounded-2xl text-center text-sm text-[#77817B] border border-[#A9BDAE]/40">
      Loading ride data...
    </div>

    <div v-else-if="!ride" class="bg-white p-8 rounded-2xl text-center text-sm text-rose-600 border border-rose-200">
      Ride not found.
    </div>

    <div v-else class="space-y-6">
      <!-- Status Banner -->
      <div
        class="rounded-2xl p-6 text-white shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4"
        :class="statusBadgeClass"
      >
        <div>
          <span class="text-xs uppercase tracking-wider font-semibold opacity-80">Current Status</span>
          <h2 class="text-2xl font-bold mt-0.5 flex items-center gap-2">
            <span>{{ statusIcon }}</span>
            <span>{{ ride.status }}</span>
          </h2>
          <p class="text-xs opacity-90 mt-1">{{ statusDescription }}</p>
        </div>

        <div v-if="canCancel" class="flex items-center">
          <button
            @click="handleCancel"
            class="bg-white/20 hover:bg-white/30 text-white border border-white/40 px-4 py-2 rounded-xl text-xs font-bold transition-colors cursor-pointer"
          >
            Cancel Ride
          </button>
        </div>
      </div>

      <!-- Assigned Driver Card (From Linked List & Priority Queue) -->
      <div v-if="ride.driver_id" class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm">
        <h3 class="text-sm font-bold text-[#174C43] uppercase tracking-wider mb-4 flex items-center gap-2">
          <span>🛵</span> Assigned Driver (Priority Queue Match)
        </h3>

        <div class="flex items-center gap-4">
          <div class="w-14 h-14 rounded-full bg-[#174C43] text-white flex items-center justify-center font-bold text-xl shadow-inner">
            {{ (ride.driver_name || 'D').charAt(0) }}
          </div>
          <div class="space-y-0.5">
            <h4 class="font-bold text-base text-[#26332E]">{{ ride.driver_name }}</h4>
            <p class="text-xs text-[#77817B]">Vehicle: {{ ride.vehicle_number || 'Bike' }}</p>
            <p class="text-xs text-[#77817B]">Phone: {{ ride.driver_phone || '+92 300 0000000' }}</p>
          </div>
        </div>
      </div>

      <!-- Journey Details -->
      <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
        <h3 class="text-sm font-bold text-[#174C43] uppercase tracking-wider">Journey Summary</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
          <div class="bg-[#F2F5F1] p-3.5 rounded-xl border border-[#A9BDAE]/30">
            <span class="text-[#77817B] block font-semibold mb-1">Pickup</span>
            <span class="font-bold text-[#26332E]">{{ ride.pickup_location }}</span>
          </div>

          <div class="bg-[#F2F5F1] p-3.5 rounded-xl border border-[#A9BDAE]/30">
            <span class="text-[#77817B] block font-semibold mb-1">Destination</span>
            <span class="font-bold text-[#26332E]">{{ ride.destination }}</span>
          </div>
        </div>

        <div class="flex flex-wrap items-center justify-between pt-2 border-t border-gray-100 text-xs">
          <div>
            <span class="text-[#77817B]">Category:</span>
            <span class="font-semibold text-[#26332E] ml-1">{{ ride.vehicle_type }}</span>
          </div>
          <div>
            <span class="text-[#77817B]">Total Distance:</span>
            <span class="font-semibold text-[#26332E] ml-1">{{ ride.distance_km }} km</span>
          </div>
          <div>
            <span class="text-[#77817B]">Fare:</span>
            <span class="font-bold text-[#174C43] text-sm ml-1">PKR {{ ride.fare }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { cancelRide, getRide } from '../../services/api'

const route = useRoute()
const rideId = ref(route.params.id)
const ride = ref(null)
const loading = ref(true)
let pollTimer = null

onMounted(async () => {
  await fetchRide()
  pollTimer = setInterval(fetchRide, 3000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

async function fetchRide() {
  if (!rideId.value) return
  try {
    const data = await getRide(rideId.value)
    ride.value = data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const canCancel = computed(() => {
  return ride.value && (ride.value.status === 'PENDING' || ride.value.status === 'OFFERED')
})

const statusBadgeClass = computed(() => {
  if (!ride.value) return 'bg-gray-500'
  switch (ride.value.status) {
    case 'OFFERED':
      return 'bg-amber-600'
    case 'ACCEPTED':
      return 'bg-[#174C43]'
    case 'COMPLETED':
      return 'bg-emerald-700'
    case 'CANCELLED':
    case 'REJECTED':
      return 'bg-rose-700'
    default:
      return 'bg-[#174C43]'
  }
})

const statusIcon = computed(() => {
  if (!ride.value) return '●'
  switch (ride.value.status) {
    case 'OFFERED':
      return '⏳'
    case 'ACCEPTED':
      return '🛵'
    case 'COMPLETED':
      return '✅'
    case 'CANCELLED':
      return '❌'
    default:
      return '📍'
  }
})

const statusDescription = computed(() => {
  if (!ride.value) return ''
  switch (ride.value.status) {
    case 'OFFERED':
      return 'Ride has entered the Queue, and Priority Queue selected the closest driver. Waiting for driver response.'
    case 'ACCEPTED':
      return 'Driver accepted the ride! Driver is marked busy in the Singly Linked List.'
    case 'COMPLETED':
      return 'Trip has ended safely. Driver availability is restored in the Linked List.'
    case 'CANCELLED':
      return 'This ride was cancelled.'
    default:
      return ''
  }
})

async function handleCancel() {
  if (!confirm('Are you sure you want to cancel this ride?')) return
  try {
    await cancelRide(rideId.value)
    await fetchRide()
  } catch (e) {
    alert('Cancel failed: ' + e.message)
  }
}
</script>
