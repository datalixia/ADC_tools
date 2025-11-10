<script setup>
import { fetchSources, editSource } from "@apis";
const sources = ref([]);
onMounted(async () => {
  sources.value = await fetchSources();
});


const alert = ref({
  show: false,
  message: "",
  color: "success",
})


const source_logo = (source) => {
  const iconFileName = source + ".png";
  const iconName = "/src/assets/images/sources/" + iconFileName;
  const iconModule = new URL(iconName, import.meta.url).href;
  return iconModule || iconSocial;
};

const edit_source = async (source) => {
  console.log(source)
  if(source.frequency < 1 || source.frequency > 24){
    alert.value.show = true
    alert.value.message = "Frequency must be between 1 and 24 hours"
    alert.value.color = "error"
    return
  }

  const response = await editSource(source)
  if ('error' in response){
    alert.value.show = true
    alert.value.message = response.message
    alert.value.color = "error"
    return
  }
  else{
    alert.value.show = true
    alert.value.message = response.message
    alert.value.color = "success"
    return
  }


};

const delete_source = (source_id) => {
  sources.value = sources.value.filter((item) => item.id !== source_id);
};
</script>

<template>
  <div>
    <v-snackbar
    :color="alert.color"
      v-model="alert.show"
    >
      {{alert.message}}

      <template v-slot:actions>
        <v-btn
          color="pink"
          variant="text"
          @click="alert.show = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <h1 class="text-4xl font-bold mb-4">Sources</h1>
    <v-row>
      <v-col cols="3" v-for="source in sources">
        <v-card class="pa-5 mb-3">
          <div class="mb-5">
            <div class="d-flex mb-3">
              <VAvatar size="30" class="me-4">
              <VImg :src="source_logo(source.name)" />
            </VAvatar>
            <h2 class="font-weight-regular text-capitalize">
              {{ source.name }}
            </h2>
            </div>
            
            
            <a :href="source.url">{{ source.url }}</a>
          </div>
          <div class="mb-5">
            <h4 class="font-weight-regular mb-2">Frequency</h4>
            <v-text-field v-model="source.frequency" suffix="Hours">
            </v-text-field>
          </div>
          <div class="mb-5">
            <v-switch label="Active" v-model="source.state"></v-switch>
          </div>
          <div class="d-flex justify-end">
            <IconBtn color="success" variant="tonal" @click="edit_source(source)">
              <VIcon  color="success" icon="tabler-device-floppy" />
            </IconBtn>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>
