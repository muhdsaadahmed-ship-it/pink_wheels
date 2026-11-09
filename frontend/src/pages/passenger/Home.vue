<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
    <!-- Top Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-[#A9BDAE]/40 gap-4">
      <div>
        <h1 class="text-2xl font-bold text-[#174C43]">Passenger Ride Booking</h1>
        <p class="text-sm text-[#77817B]">Book a safe, verified bike ride across Karachi with automated DSA matchmaking.</p>
      </div>
      <div class="flex items-center gap-2">
        <router-link
          to="/passenger/history"
          class="px-3.5 py-2 text-xs font-semibold rounded-xl border border-[#174C43] text-[#174C43] hover:bg-[#174C43] hover:text-white transition-colors"
        >
          View Ride History
        </router-link>
      </div>
    </div>

    <!-- Main Grid: Booking Controls on Left, Map on Right -->
    <div class="mt-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Left Panel: Request Form & Fare Breakdown -->
      <div class="lg:col-span-5 space-y-6">
        <div class="bg-white rounded-2xl p-6 shadow-sm border border-[#A9BDAE]/40 space-y-5">
          <h2 class="text-lg font-bold text-[#174C43] flex items-center gap-2">
            <span>📍</span> Plan Your Journey
          </h2>

          <!-- Quick Landmark Selector -->
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-[#26332E] uppercase tracking-wider mb-1">
                Pickup Location
              </label>
              <div class="space-y-1.5">
                <select
                  v-model="selectedPickupIndex"
                  @change="applyPreset('pickup')"
                  class="w-full text-sm rounded-xl border border-[#A9BDAE] bg-[#F2F5F1] p-2.5 text-[#26332E] focus:ring-2 focus:ring-[#174C43] focus:outline-none"
                >
                  <option v-for="(loc, idx) in PRESET_LOCATIONS" :key="'p-' + idx" :value="idx">
                    {{ loc.label }}
                  </option>
                </select>
                <input
                  v-model="pickupText"
                  type="text"
                  placeholder="Or enter custom pickup address"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 text-[#26332E] focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-[#26332E] uppercase tracking-wider mb-1">
                Destination
              </label>
              <div class="space-y-1.5">
                <select
                  v-model="selectedDestIndex"
                  @change="applyPreset('destination')"
                  class="w-full text-sm rounded-xl border border-[#A9BDAE] bg-[#F2F5F1] p-2.5 text-[#26332E] focus:ring-2 focus:ring-[#174C43] focus:outline-none"
                >
                  <option v-for="(loc, idx) in PRESET_LOCATIONS" :key="'d-' + idx" :value="idx">
                    {{ loc.label }}
                  </option>
                </select>
                <input
                  v-model="destText"
                  type="text"
                  placeholder="Or enter custom destination address"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 text-[#26332E] focus:outline-none"
                />
              </div>
            </div>
          </div>

          <!-- Vehicle Category Selection -->
          <div>
            <label class="block text-xs font-semibold text-[#26332E] uppercase tracking-wider mb-2">
              Select Ride Category
            </label>
            <div class="grid grid-cols-3 gap-2">
              <button
                type="button"
                @click="vehicleType = 'Bike'"
                :class="vehicleType === 'Bike' ? 'border-[#174C43] bg-[#174C43]/10 text-[#174C43] font-bold' : 'border-gray-200 text-[#77817B]'"
                class="border rounded-xl p-2.5 text-center text-xs transition-all flex flex-col items-center"
              >
                <span class="text-xl mb-1">🛵</span>
                <span>Bike</span>
                <span class="text-[10px] text-[#77817B]">PKR 15/km</span>
              </button>

              <button
                type="button"
                @click="vehicleType = 'Car'"
                :class="vehicleType === 'Car' ? 'border-[#174C43] bg-[#174C43]/10 text-[#174C43] font-bold' : 'border-gray-200 text-[#77817B]'"
                class="border rounded-xl p-2.5 text-center text-xs transition-all flex flex-col items-center"
              >
                <span class="text-xl mb-1">🚗</span>
                <span>Car</span>
                <span class="text-[10px] text-[#77817B]">PKR 18/km</span>
              </button>

              <button
                type="button"
                @click="vehicleType = 'Good Car'"
                :class="vehicleType === 'Good Car' ? 'border-[#174C43] bg-[#174C43]/10 text-[#174C43] font-bold' : 'border-gray-200 text-[#77817B]'"
                class="border rounded-xl p-2.5 text-center text-xs transition-all flex flex-col items-center"
              >
                <span class="text-xl mb-1">✨</span>
                <span>Premium</span>
                <span class="text-[10px] text-[#77817B]">PKR 22/km</span>
              </button>
            </div>
          </div>

          <!-- Fare Estimation Box -->
          <div v-if="fareEstimate" class="bg-[#F2F5F1] rounded-xl p-4 border border-[#A9BDAE]/50 space-y-2">
            <div class="flex justify-between items-center text-xs text-[#77817B]">
              <span>Trip Distance (Haversine):</span>
              <span class="font-bold text-[#26332E]">{{ fareEstimate.distance_km }} km</span>
            </div>
            <div class="flex justify-between items-center text-xs text-[#77817B]">
              <span>Base Fare:</span>
              <span>PKR {{ fareEstimate.base_fare }}</span>
            </div>
            <div class="flex justify-between items-center text-xs text-[#77817B]">
              <span>Distance Charge (Rs. {{ fareEstimate.rate_per_km }}/km):</span>
              <span>PKR {{ fareEstimate.distance_charge }}</span>
            </div>
            <div class="pt-2 border-t border-[#A9BDAE]/40 flex justify-between items-center text-sm font-bold text-[#174C43]">
              <span>Total Estimated Fare:</span>
              <span class="text-base">PKR {{ fareEstimate.total_fare }}</span>
            </div>
          </div>

          <!-- Request Button -->
          <button
            @click="handleRequestRide"
            :disabled="!canRequest || isSubmitting"
            class="w-full py-3.5 px-4 rounded-xl text-white font-bold text-sm shadow-md transition-all flex items-center justify-center gap-2"
            :class="canRequest && !isSubmitting ? 'bg-[#174C43] hover:bg-[#113932] cursor-pointer' : 'bg-gray-300 text-gray-500 cursor-not-allowed'"
          >
            <span v-if="isSubmitting">Processing Queue & Matchmaking...</span>
            <span v-else>Request Ride Now 🛵</span>
          </button>
        </div>
      </div>

      <!-- Right Panel: Interactive Map -->
      <div class="lg:col-span-7 flex flex-col">
        <div class="bg-white p-4 rounded-2xl shadow-sm border border-[#A9BDAE]/40 flex-1 flex flex-col">
          <div class="flex items-center justify-between pb-3 mb-2 border-b border-gray-100">
            <span class="text-xs font-semibold text-[#174C43]">
              Karachi Live Map • Click map to set Pickup (P) & Destination (D)
            </span>
            <span class="text-[11px] text-[#77817B]">
              {{ availableDriversCount }} available drivers in Linked List
            </span>
          </div>

          <div class="flex-1 min-h-[460px]">
            <RideMap
              :pickup="pickupCoords"
              :destination="destCoords"
              :drivers="driversList"
              @select-pickup="onMapPickup"
              @select-destination="onMapDest"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import RideMap from '../../components/common/RideMap.vue'
import { estimateFare, getDrivers, requestRide } from '../../services/api'

const router = useRouter()

const PRESET_LOCATIONS = [
  { label: 'Saddar Empress Market', lat: 24.8615, lon: 67.0099 },
  { label: 'Clifton Beach / Seaview', lat: 24.8138, lon: 67.0300 },
  { label: 'Tariq Road PECHS', lat: 24.8719, lon: 67.0594 },
  { label: 'Gulshan-e-Iqbal Block 6', lat: 24.9180, lon: 67.0971 },
  { label: 'IBA Karachi / University Rd', lat: 24.9400, lon: 67.1140 },
  { label: 'Cantt Station Karachi', lat: 24.8472, lon: 67.0450 },
  { label: 'North Nazimabad Block H', lat: 24.9298, lon: 67.0425 },
  { label: 'Dolmen Mall Clifton', lat: 24.8115, lon: 67.0335 },
]

const selectedPickupIndex = ref(0)
const selectedDestIndex = ref(1)
const pickupText = ref(PRESET_LOCATIONS[0].label)
const destText = ref(PRESET_LOCATIONS[1].label)

const pickupCoords = ref({ lat: PRESET_LOCATIONS[0].lat, lon: PRESET_LOCATIONS[0].lon, label: PRESET_LOCATIONS[0].label })
const destCoords = ref({ lat: PRESET_LOCATIONS[1].lat, lon: PRESET_LOCATIONS[1].lon, label: PRESET_LOCATIONS[1].label })
const vehicleType = ref('Bike')

const driversList = ref([])
const fareEstimate = ref(null)
const isSubmitting = ref(false)

const availableDriversCount = computed(() => {
  return driversList.value.filter(d => d.is_available).length
})

const canRequest = computed(() => {
  return pickupCoords.value && destCoords.value && fareEstimate.value
})

onMounted(async () => {
  await loadDrivers()
  await calculateCurrentFare()
})

async function loadDrivers() {
  try {
    const res = await getDrivers()
    driversList.value = res.drivers || []
  } catch (err) {
    console.error('Failed to load drivers:', err)
  }
}

function applyPreset(type) {
  if (type === 'pickup' && selectedPickupIndex.value !== null) {
    const loc = PRESET_LOCATIONS[selectedPickupIndex.value]
    pickupCoords.value = {
      lat: loc.lat,
      lon: loc.lon,
      label: loc.label,
    }
    pickupText.value = loc.label
  } else if (type === 'destination' && selectedDestIndex.value !== null) {
    const loc = PRESET_LOCATIONS[selectedDestIndex.value]
    destCoords.value = {
      lat: loc.lat,
      lon: loc.lon,
      label: loc.label,
    }
    destText.value = loc.label
  }
}

function onMapPickup(data) {
  pickupCoords.value = data
  pickupText.value = `Map Point (${data.lat}, ${data.lon})`
}

function onMapDest(data) {
  destCoords.value = data
  destText.value = `Map Point (${data.lat}, ${data.lon})`
}

async function calculateCurrentFare() {
  if (pickupCoords.value && destCoords.value) {
    try {
      const res = await estimateFare(
        pickupCoords.value.lat,
        pickupCoords.value.lon,
        destCoords.value.lat,
        destCoords.value.lon,
        vehicleType.value
      )
      fareEstimate.value = res
    } catch (e) {
      console.error(e)
    }
  }
}

watch([pickupCoords, destCoords, vehicleType], () => {
  calculateCurrentFare()
}, { deep: true })

async function handleRequestRide() {
  if (!canRequest.value) return
  isSubmitting.value = true

  try {
    const res = await requestRide({
      passenger_id: 1, // Demo Fatima Noor
      pickup_location: pickupText.value || 'Selected Pickup',
      destination: destText.value || 'Selected Destination',
      pickup_latitude: pickupCoords.value.lat,
      pickup_longitude: pickupCoords.value.lon,
      destination_latitude: destCoords.value.lat,
      destination_longitude: destCoords.value.lon,
      vehicle_type: vehicleType.value,
    })

    // Navigate to ride status page
    router.push({
      path: `/passenger/status/${res.ride_id}`,
      query: { new: '1' }
    })
  } catch (err) {
    alert('Error requesting ride: ' + (err.response?.data?.detail || err.message))
  } finally {
    isSubmitting.value = false
  }
}
</script>
