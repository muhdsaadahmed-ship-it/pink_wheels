import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Driver & Linked List APIs
export const getDrivers = () => client.get('/api/drivers').then(r => r.data)
export const registerDriver = (data) => client.post('/api/drivers/register', data).then(r => r.data)
export const getDriver = (id) => client.get(`/api/drivers/${id}`).then(r => r.data)
export const deleteDriver = (id) => client.delete(`/api/drivers/${id}`).then(r => r.data)
export const updateDriverAvailability = (id, isAvailable) =>
  client.patch(`/api/drivers/${id}/availability`, { is_available: isAvailable }).then(r => r.data)

// DSA Demonstration APIs
export const getLinkedListDemo = () => client.get('/api/dsa/linked-list').then(r => r.data)
export const getQueueDemo = () => client.get('/api/dsa/queue').then(r => r.data)
export const getPriorityQueueDemo = (lat = 24.8615, lon = 67.0099) =>
  client.get('/api/dsa/priority-queue', { params: { lat, lon } }).then(r => r.data)
export const getStackDemo = () => client.get('/api/dsa/stack').then(r => r.data)
export const simulateMatchmaking = (lat = 24.8615, lon = 67.0099) =>
  client.post('/api/dsa/matchmaking', { pickup_latitude: lat, pickup_longitude: lon }).then(r => r.data)

// Ride & Fare APIs
export const estimateFare = (pickupLat, pickupLon, destLat, destLon, vehicleType = 'Bike') =>
  client.post('/api/rides/estimate-fare', {
    pickup_latitude: pickupLat,
    pickup_longitude: pickupLon,
    destination_latitude: destLat,
    destination_longitude: destLon,
    vehicle_type: vehicleType,
  }).then(r => r.data)

export const requestRide = (rideData) => client.post('/api/rides/request', rideData).then(r => r.data)
export const listRides = (status) => client.get('/api/rides', { params: status ? { status } : {} }).then(r => r.data)
export const getRide = (id) => client.get(`/api/rides/${id}`).then(r => r.data)
export const acceptRide = (rideId, driverId) => client.post(`/api/rides/${rideId}/accept`, { driver_id: driverId }).then(r => r.data)
export const rejectRide = (rideId, driverId) => client.post(`/api/rides/${rideId}/reject`, { driver_id: driverId }).then(r => r.data)
export const completeRide = (rideId) => client.post(`/api/rides/${rideId}/complete`).then(r => r.data)
export const cancelRide = (rideId) => client.post(`/api/rides/${rideId}/cancel`).then(r => r.data)

// Passengers API
export const getPassengers = () => client.get('/api/passengers').then(r => r.data)

export default client
