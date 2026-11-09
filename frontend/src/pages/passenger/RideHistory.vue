<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-[#174C43]">Passenger Ride History</h1>
        <p class="text-sm text-[#77817B]">Permanent records stored in PostgreSQL</p>
      </div>
      <router-link
        to="/passenger"
        class="text-xs font-semibold px-4 py-2 rounded-xl bg-[#174C43] text-white hover:bg-[#113932] transition-colors"
      >
        + Request New Ride
      </router-link>
    </div>

    <div v-if="loading" class="bg-white p-8 rounded-2xl text-center text-sm text-[#77817B] border border-[#A9BDAE]/40">
      Loading ride history...
    </div>

    <div v-else-if="rides.length === 0" class="bg-white p-12 rounded-2xl text-center border border-[#A9BDAE]/40">
      <span class="text-4xl block mb-2">🛵</span>
      <h3 class="text-base font-bold text-[#26332E]">No Rides Recorded Yet</h3>
      <p class="text-xs text-[#77817B] mt-1">Book your first ride to see it tracked here in PostgreSQL.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="ride in rides"
        :key="ride.id"
        class="bg-white rounded-2xl p-5 border border-[#A9BDAE]/40 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-[#174C43] transition-colors"
      >
        <div class="space-y-2 flex-1">
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold font-mono text-[#174C43]">Ride #{{ ride.id }}</span>
            <span
              class="text-[11px] font-bold px-2.5 py-0.5 rounded-full"
              :class="getStatusBadge(ride.status)"
            >
              {{ ride.status }}
            </span>
            <span class="text-[11px] text-[#77817B]">{{ ride.created_at }}</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
            <div>
              <span class="text-[#77817B] font-semibold">From:</span>
              <span class="text-[#26332E] ml-1 font-medium">{{ ride.pickup_location }}</span>
            </div>
            <div>
              <span class="text-[#77817B] font-semibold">To:</span>
              <span class="text-[#26332E] ml-1 font-medium">{{ ride.destination }}</span>
            </div>
          </div>

          <div class="text-[11px] text-[#77817B] flex items-center gap-3">
            <span>Category: <strong class="text-[#26332E]">{{ ride.vehicle_type }}</strong></span>
            <span>Distance: <strong class="text-[#26332E]">{{ ride.distance_km }} km</strong></span>
            <span>Driver: <strong class="text-[#26332E]">{{ ride.driver_name || 'Unassigned' }}</strong></span>
          </div>
        </div>

        <div class="flex md:flex-col items-center md:items-end justify-between border-t md:border-t-0 pt-3 md:pt-0 border-gray-100">
          <div class="text-base font-bold text-[#174C43]">
            PKR {{ ride.fare }}
          </div>
          <router-link
            :to="`/passenger/status/${ride.id}`"
            class="text-xs font-semibold text-[#174C43] hover:underline mt-1"
          >
            Track Status →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { listRides } from '../../services/api'

const rides = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await listRides()
    rides.value = res.rides || []
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})

function getStatusBadge(status) {
  switch (status) {
    case 'COMPLETED':
      return 'bg-emerald-100 text-emerald-800 border border-emerald-300'
    case 'ACCEPTED':
      return 'bg-teal-100 text-teal-800 border border-teal-300'
    case 'OFFERED':
      return 'bg-amber-100 text-amber-800 border border-amber-300'
    case 'CANCELLED':
    case 'REJECTED':
      return 'bg-rose-100 text-rose-800 border border-rose-300'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>
