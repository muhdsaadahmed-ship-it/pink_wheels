<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
    <!-- Header -->
    <div class="border-b border-[#A9BDAE]/40 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-[#174C43] flex items-center gap-2">
          <span>🧠</span> DSA Demonstration Dashboard
        </h1>
        <p class="text-xs text-[#77817B]">Interactive visual inspection of the 4 core Data Structures & Matchmaking Algorithm</p>
      </div>

      <!-- Navigation Tabs -->
      <div class="flex flex-wrap gap-1.5 bg-[#F2F5F1] p-1.5 rounded-2xl border border-[#A9BDAE]/40">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer flex items-center gap-1.5"
          :class="activeTab === tab.id ? 'bg-[#174C43] text-white shadow-sm' : 'text-[#77817B] hover:text-[#174C43] hover:bg-white/50'"
        >
          <span>{{ tab.icon }}</span>
          <span>{{ tab.label }}</span>
        </button>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 1: LINKED LIST & DRIVER REGISTRATION (PRIMARY FEATURE) -->
    <!-- ============================================================== -->
    <div v-if="activeTab === 'linked_list'" class="space-y-6">
      <!-- Academic Concept Callout -->
      <div class="bg-white rounded-2xl p-5 border-l-4 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 class="text-sm font-bold text-[#174C43]">Data Structure 1: Singly Linked List (Driver Registration)</h3>
          <p class="text-xs text-[#77817B] mt-0.5">
            Nodes represent registered drivers linked via memory pointers (<code class="text-emerald-700 font-mono">current.next</code>).
            Registered drivers remain in memory even when offline/busy (<code class="text-emerald-700 font-mono">is_available: false</code>).
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-center px-4 py-2 bg-[#F2F5F1] rounded-xl border border-[#A9BDAE]/40">
            <span class="text-[10px] uppercase font-bold text-[#77817B] block">Total Nodes</span>
            <span class="text-lg font-black text-[#174C43]">{{ linkedListSize }}</span>
          </div>
        </div>
      </div>

      <!-- Visual Pointer Chain -->
      <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-3">
        <div class="flex items-center justify-between">
          <h4 class="text-xs font-bold text-[#174C43] uppercase tracking-wider">Memory Pointer Visualization</h4>
          <span class="text-[11px] text-[#77817B] font-mono">Head → [Node] → [Node] ... → NULL</span>
        </div>

        <div class="overflow-x-auto pb-4 pt-2">
          <div class="flex items-center gap-2 min-w-max">
            <div class="px-3 py-2 rounded-xl bg-[#174C43] text-white text-xs font-black shadow-sm">
              HEAD
            </div>
            <span class="text-[#174C43] font-bold">→</span>

            <template v-for="(node, idx) in linkedListNodes" :key="node.driver_id">
              <div
                class="rounded-xl border p-3 bg-[#F2F5F1] shadow-sm space-y-1 min-w-[170px]"
                :class="node.is_available ? 'border-emerald-300' : 'border-amber-300'"
              >
                <div class="flex justify-between items-center text-[10px]">
                  <span class="font-mono font-bold text-[#174C43]">#{{ node.driver_id }}</span>
                  <span
                    class="px-1.5 py-0.5 rounded-full font-bold"
                    :class="node.is_available ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'"
                  >
                    {{ node.is_available ? 'Available' : 'Busy' }}
                  </span>
                </div>
                <div class="font-bold text-xs text-[#26332E] truncate">{{ node.driver_name }}</div>
                <div class="text-[10px] text-[#77817B] truncate">{{ node.vehicle_number }}</div>
                <div class="pt-1 border-t border-gray-200 text-[9px] text-[#77817B] font-mono">
                  next: {{ idx < linkedListNodes.length - 1 ? '#' + linkedListNodes[idx + 1].driver_id : 'NULL' }}
                </div>
              </div>
              <span class="text-[#174C43] font-bold">→</span>
            </template>

            <div class="px-3 py-2 rounded-xl bg-gray-200 text-gray-700 text-xs font-mono font-bold">
              NULL
            </div>
          </div>
        </div>
      </div>

      <!-- Controls: Register New Driver Node + Search + Delete -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- Register New Driver Node Form (append / insert) -->
        <div class="lg:col-span-5 bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
          <h4 class="text-sm font-bold text-[#174C43] uppercase tracking-wider flex items-center gap-2">
            <span>+</span> Register Driver (Append Node)
          </h4>

          <form @submit.prevent="handleRegisterDriver" class="space-y-3">
            <div>
              <label class="block text-[11px] font-semibold text-[#77817B] mb-1">Full Name</label>
              <input
                v-model="newDriverForm.driver_name"
                required
                type="text"
                placeholder="e.g. Asma Noreen"
                class="w-full text-xs rounded-xl border border-gray-200 p-2.5 focus:outline-none focus:border-[#174C43]"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[11px] font-semibold text-[#77817B] mb-1">Phone Number</label>
                <input
                  v-model="newDriverForm.phone_number"
                  required
                  type="text"
                  placeholder="+92 300 1234567"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 focus:outline-none"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-[#77817B] mb-1">Vehicle Plate</label>
                <input
                  v-model="newDriverForm.vehicle_number"
                  required
                  type="text"
                  placeholder="KHI-BK-9999"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 focus:outline-none"
                />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-[11px] font-semibold text-[#77817B] mb-1">Latitude</label>
                <input
                  v-model.number="newDriverForm.current_latitude"
                  required
                  type="number"
                  step="0.0001"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 focus:outline-none"
                />
              </div>
              <div>
                <label class="block text-[11px] font-semibold text-[#77817B] mb-1">Longitude</label>
                <input
                  v-model.number="newDriverForm.current_longitude"
                  required
                  type="number"
                  step="0.0001"
                  class="w-full text-xs rounded-xl border border-gray-200 p-2.5 focus:outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              class="w-full py-2.5 bg-[#174C43] hover:bg-[#113932] text-white font-bold text-xs rounded-xl transition-colors shadow-sm cursor-pointer"
            >
              Insert New Node into Linked List
            </button>
          </form>
        </div>

        <!-- Search & Delete Driver Node -->
        <div class="lg:col-span-7 bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <h4 class="text-sm font-bold text-[#174C43] uppercase tracking-wider">
              Search & Node Management
            </h4>
            <div class="flex items-center gap-2">
              <input
                v-model.number="searchIdInput"
                type="number"
                placeholder="Driver ID (e.g. 102)"
                class="text-xs rounded-xl border border-gray-200 p-2 focus:outline-none w-36"
              />
              <button
                @click="handleSearchDriver"
                class="px-3 py-2 bg-[#A9BDAE] text-[#174C43] font-bold text-xs rounded-xl hover:bg-[#98ac9d] transition-colors cursor-pointer"
              >
                Search
              </button>
            </div>
          </div>

          <div v-if="searchResult" class="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-xs flex justify-between items-center">
            <div>
              <span class="font-bold text-emerald-900">Found Driver #{{ searchResult.driver_id }}:</span>
              <span class="ml-1 text-emerald-800">{{ searchResult.driver_name }} ({{ searchResult.vehicle_number }})</span>
              <span class="block text-[11px] text-emerald-700">Coords: {{ searchResult.current_latitude }}, {{ searchResult.current_longitude }}</span>
            </div>
            <button
              @click="searchResult = null"
              class="text-emerald-700 hover:text-emerald-950 font-bold"
            >
              ✕
            </button>
          </div>

          <!-- Drivers Table -->
          <div class="overflow-x-auto border border-gray-100 rounded-xl">
            <table class="w-full text-left text-xs">
              <thead class="bg-[#F2F5F1] text-[#77817B] font-semibold border-b border-gray-200">
                <tr>
                  <th class="p-2.5">ID</th>
                  <th class="p-2.5">Name</th>
                  <th class="p-2.5">Vehicle</th>
                  <th class="p-2.5">Status</th>
                  <th class="p-2.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="node in linkedListNodes" :key="node.driver_id" class="hover:bg-gray-50/70">
                  <td class="p-2.5 font-mono font-bold text-[#174C43]">#{{ node.driver_id }}</td>
                  <td class="p-2.5 font-bold text-[#26332E]">{{ node.driver_name }}</td>
                  <td class="p-2.5 text-[#77817B]">{{ node.vehicle_number }}</td>
                  <td class="p-2.5">
                    <button
                      @click="handleToggleNodeAvailability(node)"
                      class="px-2 py-0.5 rounded-full text-[10px] font-bold cursor-pointer"
                      :class="node.is_available ? 'bg-emerald-100 text-emerald-800 hover:bg-emerald-200' : 'bg-amber-100 text-amber-800 hover:bg-amber-200'"
                    >
                      {{ node.is_available ? 'Available (Toggle)' : 'Busy (Toggle)' }}
                    </button>
                  </td>
                  <td class="p-2.5 text-right">
                    <button
                      @click="handleDeleteDriver(node.driver_id)"
                      class="text-rose-600 hover:text-rose-800 font-bold text-xs cursor-pointer"
                    >
                      Delete Node
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 2: QUEUE DEMONSTRATION (FIFO) -->
    <!-- ============================================================== -->
    <div v-else-if="activeTab === 'queue'" class="space-y-6">
      <div class="bg-white rounded-2xl p-5 border-l-4 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 class="text-sm font-bold text-[#174C43]">Data Structure 2: FIFO Queue (Ride Request Management)</h3>
          <p class="text-xs text-[#77817B] mt-0.5">
            Stores incoming passenger ride requests. Oldest request at the front is processed first (<code class="text-emerald-700 font-mono">dequeue()</code>).
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-center px-4 py-2 bg-[#F2F5F1] rounded-xl border border-[#A9BDAE]/40">
            <span class="text-[10px] uppercase font-bold text-[#77817B] block">Queue Size</span>
            <span class="text-lg font-black text-[#174C43]">{{ queueData?.size || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Queue Visualization -->
      <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
        <div class="flex items-center justify-between">
          <h4 class="text-xs font-bold text-[#174C43] uppercase tracking-wider">FIFO Queue Order (Front → Rear)</h4>
          <div class="flex items-center gap-2">
            <button
              @click="handleEnqueueDemo"
              class="px-3 py-1.5 bg-[#174C43] text-white text-xs font-bold rounded-xl hover:bg-[#113932] transition-colors cursor-pointer"
            >
              + Enqueue Demo Request
            </button>
          </div>
        </div>

        <div v-if="!queueData?.items || queueData.items.length === 0" class="p-8 text-center text-xs text-[#77817B] bg-[#F2F5F1] rounded-xl border border-dashed border-[#A9BDAE]">
          Queue is currently empty. Click "+ Enqueue Demo Request" or request a ride from Passenger view to see elements enter.
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="(item, idx) in queueData.items"
            :key="idx"
            class="p-4 rounded-xl border border-[#A9BDAE]/50 bg-[#F2F5F1] flex items-center justify-between text-xs"
          >
            <div class="flex items-center gap-3">
              <span class="w-8 h-8 rounded-full bg-[#174C43] text-white font-bold flex items-center justify-center text-xs">
                {{ idx === 0 ? 'FRONT' : '#' + (idx + 1) }}
              </span>
              <div>
                <span class="font-bold text-[#26332E]">Passenger #{{ item.passenger_id }}</span>
                <span class="text-[#77817B] ml-2">From: {{ item.pickup_location }} → To: {{ item.destination }}</span>
                <span class="block text-[11px] text-[#77817B]">Distance: {{ item.distance_km }} km | Fare: PKR {{ item.fare }}</span>
              </div>
            </div>
            <span class="text-[11px] font-mono text-[#174C43] font-bold">
              {{ idx === 0 ? 'Next in Line to Process' : 'Queued' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 3: PRIORITY QUEUE DEMONSTRATION (MIN-HEAP) -->
    <!-- ============================================================== -->
    <div v-else-if="activeTab === 'priority_queue'" class="space-y-6">
      <div class="bg-white rounded-2xl p-5 border-l-4 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 class="text-sm font-bold text-[#174C43]">Data Structure 3: Binary Min-Heap Priority Queue (Driver Matchmaking)</h3>
          <p class="text-xs text-[#77817B] mt-0.5">
            Extracts available drivers from the Linked List and builds a custom binary min-heap keyed by <code class="text-emerald-700 font-mono">eta_minutes</code> (with distance as tie-breaker).
            The root always contains the optimal driver!
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-center px-4 py-2 bg-[#F2F5F1] rounded-xl border border-[#A9BDAE]/40">
            <span class="text-[10px] uppercase font-bold text-[#77817B] block">Heap Size</span>
            <span class="text-lg font-black text-[#174C43]">{{ priorityQueueData?.size || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Coordinate Picker for Min-Heap Inspection -->
      <div class="bg-white rounded-2xl p-5 border border-[#A9BDAE]/40 shadow-sm flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="text-xs font-bold text-[#26332E]">Reference Pickup Point:</span>
          <select
            v-model="selectedPqPreset"
            @change="handlePqPresetChange"
            class="text-xs rounded-xl border border-[#A9BDAE] bg-[#F2F5F1] p-2 focus:outline-none"
          >
            <option v-for="(loc, idx) in PRESET_LOCATIONS" :key="idx" :value="loc">
              {{ loc.label }}
            </option>
          </select>
        </div>
        <span class="text-xs text-[#77817B]">
          Current Coords: ({{ pqRefLat }}, {{ pqRefLon }})
        </span>
      </div>

      <!-- Priority Order Cards -->
      <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
        <h4 class="text-xs font-bold text-[#174C43] uppercase tracking-wider">
          Drivers Ranked by Min-Heap Priority (Lowest ETA First)
        </h4>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="(driver, idx) in (priorityQueueData?.sorted_priority_order || [])"
            :key="driver.driver_id"
            class="p-4 rounded-xl border shadow-sm space-y-2"
            :class="idx === 0 ? 'border-2 border-emerald-500 bg-emerald-50/50' : 'border-gray-200 bg-white'"
          >
            <div class="flex justify-between items-center">
              <span class="text-xs font-black px-2 py-0.5 rounded-full" :class="idx === 0 ? 'bg-emerald-600 text-white' : 'bg-gray-100 text-[#77817B]'">
                {{ idx === 0 ? '★ ROOT (1st Priority)' : '#' + (idx + 1) }}
              </span>
              <span class="font-bold text-sm text-[#174C43]">{{ driver.eta_minutes }} min ETA</span>
            </div>

            <div>
              <h5 class="font-bold text-sm text-[#26332E]">{{ driver.driver_name }}</h5>
              <p class="text-[11px] text-[#77817B]">ID: #{{ driver.driver_id }} | {{ driver.vehicle_number }}</p>
            </div>

            <div class="pt-2 border-t border-gray-100 flex justify-between text-[11px] text-[#77817B]">
              <span>Distance to Pickup:</span>
              <span class="font-bold text-[#26332E]">{{ driver.distance_km }} km</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 4: STACK DEMONSTRATION (LIFO) -->
    <!-- ============================================================== -->
    <div v-else-if="activeTab === 'stack'" class="space-y-6">
      <div class="bg-white rounded-2xl p-5 border-l-4 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 class="text-sm font-bold text-[#174C43]">Data Structure 4: LIFO Stack (Ride Activity History)</h3>
          <p class="text-xs text-[#77817B] mt-0.5">
            Maintains real-time event trace. The most recent action is pushed to the <code class="text-emerald-700 font-mono">top</code> and displayed first.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-center px-4 py-2 bg-[#F2F5F1] rounded-xl border border-[#A9BDAE]/40">
            <span class="text-[10px] uppercase font-bold text-[#77817B] block">Stack Depth</span>
            <span class="text-lg font-black text-[#174C43]">{{ stackData?.size || 0 }}</span>
          </div>
        </div>
      </div>

      <!-- Visual Stack Container -->
      <div class="bg-white rounded-2xl p-6 border border-[#A9BDAE]/40 shadow-sm space-y-4">
        <h4 class="text-xs font-bold text-[#174C43] uppercase tracking-wider">
          Event Audit Trail (Top of Stack ↓ Oldest)
        </h4>

        <div class="space-y-3">
          <div
            v-for="(act, idx) in (stackData?.items || [])"
            :key="idx"
            class="p-4 rounded-xl border border-[#A9BDAE]/40 bg-[#F2F5F1] flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
            :class="idx === 0 ? 'border-2 border-[#174C43] bg-teal-50/40' : ''"
          >
            <div class="flex items-start gap-3">
              <span class="px-2 py-1 rounded-md text-[10px] font-mono font-bold" :class="idx === 0 ? 'bg-[#174C43] text-white' : 'bg-gray-200 text-gray-700'">
                {{ idx === 0 ? 'TOP' : '#' + (idx + 1) }}
              </span>
              <div>
                <span class="font-bold text-[#174C43]">{{ act.event }}</span>
                <p class="text-[#26332E] mt-0.5">{{ act.description }}</p>
              </div>
            </div>
            <span class="text-[10px] font-mono text-[#77817B] self-end sm:self-auto">{{ act.timestamp }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- TAB 5: MATCHMAKING SIMULATION -->
    <!-- ============================================================== -->
    <div v-else-if="activeTab === 'matchmaking'" class="space-y-6">
      <div class="bg-white rounded-2xl p-5 border-l-4 border-[#174C43] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 class="text-sm font-bold text-[#174C43]">Matchmaking Algorithm: Linked List ➔ Priority Queue Connection</h3>
          <p class="text-xs text-[#77817B] mt-0.5">
            Step-by-step walkthrough showing how available drivers in the Linked List are evaluated via Haversine distance and prioritized in the Min-Heap.
          </p>
        </div>
        <button
          @click="runSimulation"
          class="px-4 py-2 bg-[#174C43] hover:bg-[#113932] text-white text-xs font-bold rounded-xl transition-colors shadow-sm cursor-pointer"
        >
          Re-Run Simulation ↻
        </button>
      </div>

      <div v-if="simulationData" class="space-y-6">
        <!-- Steps Walkthrough -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-3">
          <div
            v-for="s in simulationData.steps"
            :key="s.step"
            class="bg-white p-4 rounded-xl border border-[#A9BDAE]/40 shadow-sm space-y-1.5"
          >
            <span class="text-[10px] font-bold text-[#174C43] uppercase tracking-wider block">Step {{ s.step }}</span>
            <h5 class="text-xs font-bold text-[#26332E]">{{ s.action }}</h5>
            <p class="text-[11px] text-[#77817B]">{{ s.detail }}</p>
          </div>
        </div>

        <!-- Selected Driver Winner Card -->
        <div v-if="simulationData.selected_driver" class="bg-emerald-50 rounded-2xl p-6 border-2 border-emerald-400 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span class="text-xs uppercase font-bold text-emerald-800 tracking-wider">Algorithm Winner (Optimal Match)</span>
            <h4 class="text-xl font-bold text-emerald-950 mt-1">
              {{ simulationData.selected_driver.driver_name }} (#{{ simulationData.selected_driver.driver_id }})
            </h4>
            <p class="text-xs text-emerald-800 mt-1">
              Vehicle: {{ simulationData.selected_driver.vehicle_number }} | Distance: {{ simulationData.selected_driver.distance_km }} km | ETA: {{ simulationData.selected_driver.eta_minutes }} mins
            </p>
          </div>
          <div class="text-right">
            <span class="text-xs font-bold px-3 py-1 bg-emerald-600 text-white rounded-xl shadow-sm">
              Lowest ETA Selected
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  deleteDriver,
  getDriver,
  getLinkedListDemo,
  getPriorityQueueDemo,
  getQueueDemo,
  getStackDemo,
  registerDriver,
  simulateMatchmaking,
  updateDriverAvailability,
} from '../../services/api'

const tabs = [
  { id: 'linked_list', label: '1. Linked List', icon: '🔗' },
  { id: 'queue', label: '2. FIFO Queue', icon: '📥' },
  { id: 'priority_queue', label: '3. Priority Queue', icon: '⭐' },
  { id: 'stack', label: '4. LIFO Stack', icon: '📚' },
  { id: 'matchmaking', label: '5. Matchmaking Flow', icon: '⚡' },
]

const activeTab = ref('linked_list')

// Karachi Landmarks
const PRESET_LOCATIONS = [
  { label: 'Saddar Empress Market', lat: 24.8615, lon: 67.0099 },
  { label: 'Clifton Beach / Seaview', lat: 24.8138, lon: 67.0300 },
  { label: 'Tariq Road PECHS', lat: 24.8719, lon: 67.0594 },
  { label: 'Gulshan-e-Iqbal Block 6', lat: 24.9180, lon: 67.0971 },
]

// Linked list state
const linkedListNodes = ref([])
const linkedListSize = ref(0)
const searchIdInput = ref('')
const searchResult = ref(null)

const newDriverForm = ref({
  driver_name: '',
  phone_number: '',
  vehicle_number: '',
  current_latitude: 24.8615,
  current_longitude: 67.0099,
  is_available: true,
})

// Queue, PQ, Stack, Simulation state
const queueData = ref(null)
const priorityQueueData = ref(null)
const stackData = ref(null)
const simulationData = ref(null)

const selectedPqPreset = ref(PRESET_LOCATIONS[0])
const pqRefLat = ref(24.8615)
const pqRefLon = ref(67.0099)

onMounted(async () => {
  await fetchAllDsa()
})

async function fetchAllDsa() {
  await fetchLinkedList()
  await fetchQueue()
  await fetchPriorityQueue()
  await fetchStack()
  await runSimulation()
}

async function fetchLinkedList() {
  try {
    const res = await getLinkedListDemo()
    linkedListNodes.value = res.nodes || []
    linkedListSize.value = res.size || 0
  } catch (err) {
    console.error(err)
  }
}

async function fetchQueue() {
  try {
    queueData.value = await getQueueDemo()
  } catch (err) {
    console.error(err)
  }
}

async function fetchPriorityQueue() {
  try {
    priorityQueueData.value = await getPriorityQueueDemo(pqRefLat.value, pqRefLon.value)
  } catch (err) {
    console.error(err)
  }
}

async function fetchStack() {
  try {
    stackData.value = await getStackDemo()
  } catch (err) {
    console.error(err)
  }
}

async function runSimulation() {
  try {
    simulationData.value = await simulateMatchmaking(pqRefLat.value, pqRefLon.value)
  } catch (err) {
    console.error(err)
  }
}

async function handleRegisterDriver() {
  try {
    await registerDriver(newDriverForm.value)
    alert('Driver node appended successfully to Linked List!')
    newDriverForm.value = {
      driver_name: '',
      phone_number: '',
      vehicle_number: '',
      current_latitude: 24.8615,
      current_longitude: 67.0099,
      is_available: true,
    }
    await fetchLinkedList()
    await fetchPriorityQueue()
  } catch (err) {
    alert('Error registering driver: ' + (err.response?.data?.detail || err.message))
  }
}

async function handleSearchDriver() {
  if (!searchIdInput.value) return
  try {
    searchResult.value = await getDriver(searchIdInput.value)
  } catch {
    alert(`Driver ID ${searchIdInput.value} not found in Linked List.`)
    searchResult.value = null
  }
}

async function handleDeleteDriver(driverId) {
  if (!confirm(`Delete Driver #${driverId} node from Linked List?`)) return
  try {
    await deleteDriver(driverId)
    await fetchLinkedList()
    await fetchPriorityQueue()
  } catch (err) {
    alert('Error deleting driver: ' + err.message)
  }
}

async function handleToggleNodeAvailability(node) {
  try {
    await updateDriverAvailability(node.driver_id, !node.is_available)
    await fetchLinkedList()
    await fetchPriorityQueue()
  } catch (e) {
    alert('Error updating status: ' + e.message)
  }
}

function handlePqPresetChange() {
  if (selectedPqPreset.value) {
    pqRefLat.value = selectedPqPreset.value.lat
    pqRefLon.value = selectedPqPreset.value.lon
    fetchPriorityQueue()
  }
}

function handleEnqueueDemo() {
  alert('To enqueue a ride request, use the Passenger booking form on the Passenger page!')
}
</script>
