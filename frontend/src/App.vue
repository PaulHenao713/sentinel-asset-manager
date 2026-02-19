<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

// --- ESTADO ---
const assets = ref([])
const error = ref('')

// Objeto del formulario
const newAsset = ref({
  hostname: '',
  ip_address: '',
  os_type: '',
  risk_level: 'Bajo'
})

// --- FUNCIONES ---

// 1. Cargar activos (Lectura)
const fetchAssets = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/assets/')
    assets.value = response.data
  } catch (err) {
    console.error("Error cargando:", err)
    error.value = 'No se pudo conectar con el servidor.'
  }
}

// 2. Crear activo (Escritura) - ¡CON DEBUGGING!
const createAsset = async () => {
  // ESTO IMPRIMIRÁ EN LA CONSOLA AL HACER CLIC
  console.log("¡Botón presionado! Intentando enviar datos:", newAsset.value)
  
  // Validación manual rápida
  if (!newAsset.value.hostname || !newAsset.value.ip_address) {
    alert("Por favor completa los campos obligatorios.")
    return
  }

  try {
    await axios.post('http://127.0.0.1:8000/assets/', newAsset.value)
    
    console.log("¡Envío exitoso!")
    alert('¡Servidor registrado correctamente!')
    
    // Limpiar y recargar
    newAsset.value = { hostname: '', ip_address: '', os_type: '', risk_level: 'Bajo' }
    fetchAssets()
    
  } catch (err) {
    console.error("Error enviando:", err)
    const mensaje = err.response?.data?.detail || err.message
    alert(' Error al guardar: ' + mensaje)
  }
}

import { onUnmounted } from 'vue'

let intervalo; // Variable para controlar el reloj

onMounted(() => {
  fetchAssets() // Carga inicial
  
  // ACTIVAR EL TIEMPO REAL: Actualizar cada 2000 milisegundos (2 segundos)
  intervalo = setInterval(() => {
    fetchAssets()
  }, 2000)
})

// Limpieza: Si cierras la pestaña o cambias de vista, paramos el reloj
onUnmounted(() => {
  clearInterval(intervalo)
})
</script>

<template>
  <div class="container">
    <header>
      <h1> Sentinel Asset Manager</h1>
    </header>

    <section class="control-panel">
      <h3> Registrar Nuevo Activo</h3>
      
      <div class="form-grid">
        <div class="input-group">
          <label>Hostname</label>
          <input v-model="newAsset.hostname" placeholder="Ej: DB-Server-01" />
        </div>
        
        <div class="input-group">
          <label>Dirección IP</label>
          <input v-model="newAsset.ip_address" placeholder="Ej: 192.168.1.50" />
        </div>

        <div class="input-group">
          <label>Sistema Operativo</label>
          <input v-model="newAsset.os_type" placeholder="Ej: Ubuntu 22.04" />
        </div>

        <div class="input-group">
          <label>Nivel de Riesgo</label>
          <select v-model="newAsset.risk_level">
            <option>Bajo</option>
            <option>Medio</option>
            <option>Alto</option>
            <option>Crítico</option>
          </select>
        </div>

        <button type="button" @click="createAsset" class="btn-save">
          Guardar Activo
        </button>
      </div>
    </section>

    <section class="table-container">
      <table>
        <thead>
          <tr>
            <th><center>ID</center></th>
            <th><center>Hostname</center></th>
            <th><center>IP</center></th>
            <th><center>OS</center></th> 
            <th><center>Riesgo</center></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="asset in assets" :key="asset.id">
            <td>#{{ asset.id }}</td>
            <td>{{ asset.hostname }}</td>
            <td class="mono">{{ asset.ip_address }}</td>
            <td>{{ asset.os_type }}</td> <td>
              <span class="badge" :class="asset.risk_level.toLowerCase()">
                {{ asset.risk_level }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>


<style scoped>
/* ESTILOS PROFESIONALES "DARK MODE" PARA CIBERSEGURIDAD */
.container { max-width: 800px; margin: 0 auto; padding: 20px; font-family: 'Segoe UI', sans-serif; color: #333; }
header { text-align: center; margin-bottom: 30px; }
h1 { color: #ffff; margin-bottom: 5px; }
.subtitle { color: #7f8c8d; margin-top: 0; }

/* Formulario */
.control-panel { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; margin-bottom: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; align-items: end; }
.input-group label { display: block; font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; color: #555; }
input, select { width: 100%; padding: 8px; border: 1px solid #ced4da; border-radius: 4px; }
.btn-save { background-color: #0d6efd; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; transition: background 0.2s; }
.btn-save:hover { background-color: #0b5ed7; }

/* Tabla */
table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th { background-color: #212529; color: white; text-align: left; padding: 12px; font-size: 0.9rem; }
td { padding: 12px; border-bottom: 1px solid #dee2e6; color: #444; }
.mono { font-family: monospace; color: #d63384; } /* IP en color distinto */

/* Badges de Riesgo */
.badge { padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: bold; color: white; }
.bajo { background-color: #198754; }    /* Verde */
.medio { background-color: #ffc107; color: black; } /* Amarillo */
.alto { background-color: #fd7e14; }    /* Naranja */
.crítico { background-color: #dc3545; } /* Rojo */

.alert-error { background: #f8d7da; color: #842029; padding: 10px; border-radius: 4px; margin-bottom: 20px; }
</style>