<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8 space-y-6">
    <!-- Top Driver Identity Selector & Availability -->
    <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
      <div class="space-y-1">
        <span class="text-xs uppercase tracking-wider font-semibold text-[#77817B]">Driver Role Mode</span>
        <div class="flex items-center gap-3">
          <label class="text-xs font-semibold text-[#26332E]">Active Driver:</label>
          <select
            v-model="selectedDriverId"
            @change="handleDriverSwitch"
            class="text-sm font-bold text-[#174C43] rounded-xl border border-[#A9BDAE] bg-[#F2F5F1] p-2 focus:ring-2 focus:ring-[#174C43] focus:outline-none"
          >
            <option v-for="d in drivers" :key="d.driver_id" :value="d.driver_id">
              {{ d.driver_name }} (#{{ d.driver_id }}) — {{ d.vehicle_number }}
            </option>
          </select>
        </div>
      </div>

      <!-- Availability Toggle (Direct Linked List Manipulation) -->
      <div v-if="currentDriver" class="flex items-center gap-4 bg-[#F2F5F1] p-3 rounded-2xl border border-[#A9BDAE]/40">
        <div class="text-right">
          <span class="text-xs text-[#77817B] block font-semibold">Linked List Status</span>
          <span
            class="text-xs font-bold"
            :class="currentDriver.is_available ? 'text-emerald-700' : 'text-amber-700'"
          >
            {{ currentDriver.is_available ? '● Available for Matches' : '○ Busy / Offline' }}
          </span>
        </div>

        <button
          @click="toggleAvailability"
          class="px-4 py-2 rounded-xl text-xs font-bold transition-all shadow-sm cursor-pointer"
          :class="currentDriver.is_available ? 'bg-amber-600 hover:bg-amber-700 text-white' : 'bg-emerald-600 hover:bg-emerald-700 text-white'"
        >
          {{ currentDriver.is_available ? 'Go Offline' : 'Go Available' }}
        </button>
      </div>
    </div>

    <!-- Incoming Requests (Status: OFFERED) -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-[#174C43] flex items-center gap-2">
          <span>🔔</span> Incoming Ride Offers (Selected by Min-Heap Priority Queue)
        </h2>
        <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800 border border-amber-200">
          {{ incomingOffers.length }} Pending Offer(s)
        </span>
      </div>

      <div v-if="incomingOffers.length === 0" class="bg-white rounded-2xl p-8 text-center border border-[#A9BDAE]/40 text-[#77817B] text-xs">
        No incoming ride requests offered to you right now. Submit a ride from the Passenger view to test matchmaking!
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="offer in incomingOffers"
          :key="offer.id"
          class="bg-white rounded-2xl p-5 border-2 border-amber-400 shadow-sm space-y-4"
        >
          <div class="flex justify-between items-start">
            <div>
              <span class="text-xs font-bold font-mono text-[#174C43]">Ride #{{ offer.id }}</span>
              <h4 class="text-sm font-bold text-[#26332E]">New Ride Match Offer</h4>
              <p class="text-[11px] text-[#77817B]">Priority Queue selected you based on lowest ETA!</p>
            </div>
            <div class="text-right">
              <span class="text-sm font-bold text-[#174C43]">PKR {{ offer.fare }}</span>
              <span class="block text-[10px] text-[#77817B]">{{ offer.distance_km }} km</span>
            </div>
          </div>

          <div class="space-y-1.5 text-xs bg-[#F2F5F1] p-3 rounded-xl border border-[#A9BDAE]/30">
            <div>
              <strong class="text-[#77817B]">Pickup:</strong>
              <span class="text-[#26332E] ml-1">{{ offer.pickup_location }}</span>
            </div>
            <div>
              <strong class="text-[#77817B]">Destination:</strong>
              <span class="text-[#26332E] ml-1">{{ offer.destination }}</span>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2 pt-2">
            <button
              @click="handleAccept(offer.id)"
              class="py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-sm transition-colors cursor-pointer"
            >
              Accept Ride ✓
            </button>
            <button
              @click="handleReject(offer.id)"
              class="py-2.5 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs shadow-sm transition-colors cursor-pointer"
            >
              Reject (Next Driver) ✗
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Active Rides (Status: ACCEPTED) -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-[#174C43] flex items-center gap-2">
          <span>🛵</span> Active Ongoing Rides
        </h2>
        <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-200">
          {{ activeRides.length }} Active
        </span>
      </div>

      <div v-if="activeRides.length === 0" class="bg-white rounded-2xl p-8 text-center border border-[#A9BDAE]/40 text-[#77817B] text-xs">
        No active ongoing trips.
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="active in activeRides"
          :key="active.id"
          class="bg-white rounded-2xl p-6 border-2 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6"
        >
          <div class="space-y-2 flex-1">
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold font-mono text-[#174C43]">Ride #{{ active.id }}</span>
              <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-teal-100 text-teal-800 border border-teal-300">
                IN PROGRESS
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              <div>
                <span class="text-[#77817B] font-semibold">Pickup:</span>
                <span class="text-[#26332E] ml-1 font-bold">{{ active.pickup_location }}</span>
              </div>
              <div>
                <span class="text-[#77817B] font-semibold">Destination:</span>
                <span class="text-[#26332E] ml-1 font-bold">{{ active.destination }}</span>
              </div>
            </div>

            <div class="text-[11px] text-[#77817B] flex items-center gap-3">
              <span>Category: <strong class="text-[#26332E]">{{ active.vehicle_type }}</strong></span>
              <span>Distance: <strong class="text-[#26332E]">{{ active.distance_km }} km</strong></span>
              <span>Fare to Collect: <strong class="text-[#174C43]">PKR {{ active.fare }}</strong></span>
            </div>
          </div>

          <div>
            <button
              @click="handleComplete(active.id)"
              class="w-full md:w-auto px-6 py-3 rounded-xl bg-[#174C43] hover:bg-[#113932] text-white font-bold text-xs shadow-md transition-colors cursor-pointer"
            >
              Complete Trip & Free Driver ✓
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import {
  acceptRide,
  completeRide,
  getDrivers,
  listRides,
  rejectRide,
  updateDriverAvailability,
} from '../../services/api'

const drivers = ref([])
const selectedDriverId = ref(102) // Default to Hina Tariq
const rides = ref([])
let pollTimer = null

onMounted(async () => {
  await fetchDrivers()
  await fetchRides()
  pollTimer = setInterval(fetchRides, 3000)
})

onUnmounted(() => {
  if (pollTimer) clearInterval(pollTimer)
})

async function fetchDrivers() {
  try {
    const res = await getDrivers()
    drivers.value = res.drivers || []
    if (drivers.value.length > 0) {
      const exists = drivers.value.some(d => d.driver_id === selectedDriverId.value)
      if (!exists) {
        selectedDriverId.value = drivers.value[0].driver_id
      }
    }
  } catch (err) {
    console.error(err)
  }
}

async function fetchRides() {
  try {
    const res = await listRides()
    rides.value = res.rides || []
  } catch (err) {
    console.error(err)
  }
}

const currentDriver = computed(() => {
  return drivers.value.find(d => d.driver_id === selectedDriverId.value)
})

const incomingOffers = computed(() => {
  return rides.value.filter(
    r => r.status === 'OFFERED' && r.driver_id === selectedDriverId.value
  )
})

const activeRides = computed(() => {
  return rides.value.filter(
    r => r.status === 'ACCEPTED' && r.driver_id === selectedDriverId.value
  )
})

async function toggleAvailability() {
  if (!currentDriver.value) return
  const newStatus = !currentDriver.value.is_available
  try {
    await updateDriverAvailability(selectedDriverId.value, newStatus)
    await fetchDrivers()
  } catch (e) {
    alert('Error toggling availability: ' + e.message)
  }
}

async function handleAccept(rideId) {
  try {
    await acceptRide(rideId, selectedDriverId.value)
    await fetchDrivers()
    await fetchRides()
  } catch (e) {
    alert('Error accepting ride: ' + e.message)
  }
}

async function handleReject(rideId) {
  try {
    await rejectRide(rideId, selectedDriverId.value)
    await fetchDrivers()
    await fetchRides()
  } catch (e) {
    alert('Error rejecting ride: ' + e.message)
  }
}

async function handleComplete(rideId) {
  try {
    await completeRide(rideId)
    await fetchDrivers()
    await fetchRides()
  } catch (e) {
    alert('Error completing ride: ' + e.message)
  }
}

function handleDriverSwitch() {
  fetchRides()
}
</script>
