<script setup>
import { ref } from 'vue';
import DropZone from './components/DropZone.vue';

const image = ref(null);
const previewImage = ref(null);
const loading = ref(false);
const resultImage = ref(null);

const onReceiveImage = file => {
  // check for type
  if(!file.type.includes('image')) {
    alert('Please upload an image file');
    return;
  }

  //check for size, max 5mb allowed
  if(file.size > 5 * 1024 * 1024) {
    alert('Please upload an image file smaller than 5mb');
    return;
  }

  image.value = file;
  previewImage.value = URL.createObjectURL(image.value);
}

const removeBackground = () => {
  if(image.value == null) {
    alert('Please upload an image first');
    return;
  }

  const formData = new FormData();
  formData.append('image', image.value);

  loading.value = true

  fetch('https://lambda_url.com', {
    method: 'POST',
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    body: formData
  })
  .then(response => response.blob())
  .then(blob => {
    resultImage.value = URL.createObjectURL(blob);
    loading.value = false;
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error removing background, Please try again!');
    loading.value = false;
  });
}

const saveResult = () => {
  if(resultImage.value == null) {
    alert('There is no result to save');
    return;
  }

  const a = document.createElement('a');
  a.href = resultImage.value;
  a.download = 'result.png';
  a.click();
}

const removeImage = () => {
  image.value = null;
  previewImage.value = null;
  resultImage.value = null;
  loading.value = false;
}

</script>

<template>
  <div class='container'>
    <div>
      <h1>Your Image</h1>

      <DropZone v-if="image===null" @files-dropped="onReceiveImage" #default="{ dropZoneActive }">
        <div class="drop-zone">
          <p v-if="dropZoneActive">Drop the image</p>
          <p v-else>Drag and drop the image here</p>
        </div>
      </DropZone>

      <div v-else-if="previewImage">
        <img :src="previewImage"/>
      </div>
      
      <div class="button-group">
        <input type="file" accept="image/jpeg;image/jpg;image/png" @change="e => onReceiveImage(e.target.files[0])" class="hidden" ref="file"/>
        <button @click="$refs.file.click()">
          Upload Image
        </button>
        <button @click="removeBackground">
          Remove Background
        </button>
        <button class="remove-image" @click="removeImage">
          Reset
        </button>
      </div>
      
    </div>

    <div>
      <h1>Result</h1>
      
      <div v-if="resultImage && !loading">
        <img :src="resultImage"/>
      </div>

      <div v-else class="result-image">
        <p v-if="loading">Loading...</p>
        <p v-else>Result will be shown here</p>
      </div>

      <div class="button-group">
        <button @click="saveResult">
          Save Image
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .container {
    display: flex;
    justify-content: space-around;
    height: 100vh
  }

  .container > div {
    display: flex;
    flex-direction: column;
    border: 4px solid white;
    border-radius: 10px;
    width: 100%;
    height: auto;
    margin: 1em;
    text-align: center;
  }
  
  .drop-zone {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 1em;
    min-height: 500px;
    border: 2px dashed white;
    border-radius: 10px;
    color: white;
  }
  
  .hidden {
    display: none;
  }

  .button-group {
    display: flex;
    justify-content: center;
    gap: 1em;
    margin: 1em;
  }

  .button-group > button {
    padding: 1em;
    border: none;
    border-radius: 10px;
    background-color: white;
    color: black;
    font-size: 1em;
    cursor: pointer;
  }

  .button-group > button:hover {
    filter: brightness(0.9);
  }

  .remove-image {
    background-color: brown!important;
    color: white!important;
  }

  .result-image {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 1em;
    min-height: 500px;
    border: 2px dashed white;
    border-radius: 10px;
    color: white;
  }

  .loading-screen {
    height: 500px;
  }

  img {
    max-width: 80%;
    height: 100%;
    max-height:70vh;
    object-fit: cover;
  }
</style>
