<template>
  <div :data-active="active" @dragenter.prevent="setActive" @dragover.prevent="setActive" @dragleave.prevent="setInactive" @drop.prevent="onDrop">
    <slot :dropZoneActive="active"></slot>
  </div>
</template>
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['files-dropped'])
let active = ref(false)
let inActiveTimeout = null

function setActive() {
    active.value = true
    clearTimeout(inActiveTimeout)
}
function setInactive() {
    active.value = false
    inActiveTimeout = setTimeout(() => {
        active.value = false
    }, 50)
}

const onDrop = e => {
  setInactive()
  emit('files-dropped', e.dataTransfer.files[0])
}

const preventDefaults = e => {
  e.preventDefault()
}

const events = [
  'dragenter',
  'dragover',
  'dragleave',
  'drag'
]

onMounted(() => [
  events.forEach(event => {
    document.body.addEventListener(event, preventDefaults)
  })
])

onUnmounted(() => [
  events.forEach(event => {
    document.body.removeEventListener(event, preventDefaults)
  })
])
</script>