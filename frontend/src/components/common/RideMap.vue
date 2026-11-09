<template>
  <div class="relative w-full h-full min-h-[420px] rounded-2xl overflow-hidden shadow border border-[#A9BDAE]/40">
    <div ref="mapContainer" class="w-full h-full min-h-[420px] z-10"></div>

    <!-- Map Info Overlay / Legend -->
    <div class="absolute bottom-3 left-3 z-20 bg-white/95 backdrop-blur-sm px-3 py-2 rounded-xl text-xs text-[#26332E] shadow-md border border-[#A9BDAE]/50 flex flex-wrap items-center gap-3">
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-emerald-600 inline-block"></span>
        <span>Pickup</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-rose-600 inline-block"></span>
        <span>Destination</span>
      </div>
      <div class="flex items-center gap-1.5">
        <span class="w-3 h-3 rounded-full bg-[#174C43] inline-block"></span>
        <span>Active Driver (Linked List)</span>
      </div>
      <div v-if="routeType" class="text-[11px] text-[#77817B] border-l border-[#A9BDAE] pl-2 font-mono">
        Route: {{ routeType }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import L from 'leaflet'

const props = defineProps({
  pickup: {
    type: Object, // { lat, lon, label }
    default: null,
  },
  destination: {
    type: Object, // { lat, lon, label }
    default: null,
  },
  drivers: {
    type: Array, // list of driver nodes from Linked List
    default: () => [],
  },
  interactive: {
    type: Boolean,
    default: true,
  },
})

const emit = defineEmits(['select-pickup', 'select-destination'])

const mapContainer = ref(null)
let map = null
let pickupMarker = null
let destMarker = null
let driverLayer = null
let routePolyline = null
const routeType = ref('')

// Karachi Center (Default)
const KARACHI_CENTER = [24.8607, 67.0011]

// Custom Icons with clean SVG
const createCustomIcon = (color, text) => {
  return L.divIcon({
    className: 'custom-map-marker',
    html: `
      <div style="background-color: ${color}; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 13px; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.35);">
        ${text}
      </div>
    `,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
    popupAnchor: [0, -14],
  })
}

const pickupIcon = createCustomIcon('#059669', 'P')
const destIcon = createCustomIcon('#e11d48', 'D')
const driverIcon = createCustomIcon('#174C43', '🛵')

onMounted(() => {
  if (!mapContainer.value) return

  map = L.map(mapContainer.value).setView(KARACHI_CENTER, 12)

  // Standard OpenStreetMap tiles
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map)

  driverLayer = L.layerGroup().addTo(map)

  // Map Click Handler for selecting pickup or destination
  if (props.interactive) {
    map.on('click', (e) => {
      const { lat, lng } = e.latlng
      if (!props.pickup) {
        emit('select-pickup', { lat: parseFloat(lat.toFixed(4)), lon: parseFloat(lng.toFixed(4)), label: 'Selected on Map' })
      } else {
        emit('select-destination', { lat: parseFloat(lat.toFixed(4)), lon: parseFloat(lng.toFixed(4)), label: 'Selected on Map' })
      }
    })
  }

  updateMarkers()
  updateDrivers()
  updateRoute()
})

onUnmounted(() => {
  if (map) {
    map.remove()
    map = null
  }
})

function updateMarkers() {
  if (!map) return

  // Pickup marker
  if (props.pickup && props.pickup.lat && props.pickup.lon) {
    if (!pickupMarker) {
      pickupMarker = L.marker([props.pickup.lat, props.pickup.lon], { icon: pickupIcon }).addTo(map)
    } else {
      pickupMarker.setLatLng([props.pickup.lat, props.pickup.lon])
    }
    pickupMarker.bindPopup(`<b>Pickup:</b> ${props.pickup.label || 'Pickup Location'}`)
  } else if (pickupMarker) {
    map.removeLayer(pickupMarker)
    pickupMarker = null
  }

  // Destination marker
  if (props.destination && props.destination.lat && props.destination.lon) {
    if (!destMarker) {
      destMarker = L.marker([props.destination.lat, props.destination.lon], { icon: destIcon }).addTo(map)
    } else {
      destMarker.setLatLng([props.destination.lat, props.destination.lon])
    }
    destMarker.bindPopup(`<b>Destination:</b> ${props.destination.label || 'Destination'}`)
  } else if (destMarker) {
    map.removeLayer(destMarker)
    destMarker = null
  }

  // Auto-fit bounds if both are set
  if (props.pickup && props.destination && props.pickup.lat && props.destination.lat) {
    const bounds = L.latLngBounds(
      [props.pickup.lat, props.pickup.lon],
      [props.destination.lat, props.destination.lon]
    )
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 })
  }
}

function updateDrivers() {
  if (!map || !driverLayer) return
  driverLayer.clearLayers()

  props.drivers.forEach((d) => {
    if (d.current_latitude && d.current_longitude) {
      const marker = L.marker([d.current_latitude, d.current_longitude], { icon: driverIcon })
      marker.bindPopup(`
        <div class="text-xs">
          <p class="font-bold text-[#174C43]">${d.driver_name}</p>
          <p class="text-gray-600">ID: #${d.driver_id} | ${d.vehicle_number || 'Bike'}</p>
          <p class="mt-1 font-semibold ${d.is_available ? 'text-emerald-600' : 'text-amber-600'}">
            ${d.is_available ? '● Available' : '○ Busy'}
          </p>
        </div>
      `)
      driverLayer.addLayer(marker)
    }
  })
}

async function updateRoute() {
  if (!map) return

  if (routePolyline) {
    map.removeLayer(routePolyline)
    routePolyline = null
  }

  if (props.pickup && props.destination && props.pickup.lat && props.destination.lat) {
    const pLat = props.pickup.lat
    const pLon = props.pickup.lon
    const dLat = props.destination.lat
    const dLon = props.destination.lon

    // Try OSRM public demo routing service
    try {
      const url = `https://router.project-osrm.org/route/v1/driving/${pLon},${pLat};${dLon},${dLat}?overview=full&geometries=geojson`
      const res = await fetch(url)
      const data = await res.json()

      if (data.routes && data.routes.length > 0) {
        const coords = data.routes[0].geometry.coordinates.map(c => [c[1], c[0]])
        routePolyline = L.polyline(coords, {
          color: '#174C43',
          weight: 4,
          opacity: 0.85,
        }).addTo(map)
        routeType.value = 'OSRM Road Network'
        return
      }
    } catch {
      // Fallback below
    }

    // Straight-line fallback if offline or OSRM unavailable
    routePolyline = L.polyline([[pLat, pLon], [dLat, dLon]], {
      color: '#174C43',
      weight: 3,
      dashArray: '6, 6',
      opacity: 0.8,
    }).addTo(map)
    routeType.value = 'Straight-Line (Demo Fallback)'
  } else {
    routeType.value = ''
  }
}

watch(() => [props.pickup, props.destination], () => {
  updateMarkers()
  updateRoute()
}, { deep: true })

watch(() => props.drivers, () => {
  updateDrivers()
}, { deep: true })
</script>
