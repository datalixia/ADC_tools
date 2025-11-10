<script setup>
import { get_runs, get_dag, pause_dag, trigger_dag, get_tasks, get_xcom, fetchSources, get_mapped_task } from "@apis";

const dag = ref(null);
const isDagActive = ref(false);
const runs = ref(null);
const tasks = ref(null);
const runs_progress = ref(0);
const loading = ref(true)
const sources = ref([]);
const sources_status = ref([]);
const sources_articles_count = ref([]);
const checked_sources = ref(null)
const dag_run_id = ref(null)
let interval;



const fetchData = async () => {

    loading.value = true
    // get dag infos
    const dag_response = await get_dag();
    if (dag_response == null) {
        alert.value.show = true
        alert.value.message = "cant request collect API, please try again"
        alert.value.color = "error"
        loading.value = false
        return
    }

    dag.value = dag_response;
    isDagActive.value = dag.value?.is_paused == true ? false : true

    // get dag runs 
    const response = await get_runs();
    if (response == null) {
        alert.value.show = true
        alert.value.message = "cant request collect API, please try again"
        alert.value.color = "error"
        loading.value = false
        return
    }
    runs.value = response;
    dag_run_id.value = response.dag_run_id;

    if (response?.state == "failed") {
        alert.value.show = true
        alert.value.message = "Last run failed, try run now, if failed multiple times please contact admin"
        alert.value.color = "error"
    }


    // get all tasks
    const tasks_response = await get_tasks(dag_run_id.value);
    if (tasks_response == null) {
        alert.value.show = true
        alert.value.message = "cant request collect API, please try again"
        alert.value.color = "error"
        loading.value = false
        return
    }
    tasks.value = tasks_response;

    // calculate progress
    const task_instances = tasks_response.task_instances;
    const total_tasks = task_instances.length;
    const finishedStates = ['success', 'failed', 'skipped', 'upstream_failed'];
    const completed = task_instances.filter(t => finishedStates.includes(t.state)).length;
    runs_progress.value = Math.round((completed / total_tasks) * 100);


    // get sources
    sources.value = await fetchSources();
    if (task_instances != undefined && task_instances.find(item => item.task_id == "check_sources")) {
        // get sources  
        const checked_sources_response = await get_xcom(dag_run_id.value, 'check_sources');
        if (checked_sources_response == null) {
            alert.value.show = true
            alert.value.message = "cant request collect API, please try again"
            alert.value.color = "error"
            loading.value = false
            return
        }
        if(checked_sources_response != false){
            checked_sources.value = string_to_json(checked_sources_response.value);
            // get sources_status
            sources_status.value = []
            for (const key in sources.value) {
                let source = sources.value[key]
                const state = await (get_source_status(source.id));
                sources_status.value.push({
                    id: source.id,
                    state: state == null ? 'success' : state
                })
            }
            
        }
        
    }



    loading.value = false
}

const get_source_status = async (source_id) => {
    const map_index = checked_sources.value.findIndex(item => item.id === source_id);
    if (map_index == -1) {
        return null
    }
    const response = await get_mapped_task(dag_run_id.value, "scraper", map_index);
    return response.state;
}



onUnmounted(() => {
    clearInterval(interval);
});

onMounted(() => {
    fetchData()
    interval = setInterval(fetchData, 10000);

});


const toggleDag = async () => {
    const response = await pause_dag(!isDagActive.value);

    if (response == null) {
        alert.value.show = true
        alert.value.message = "cant request collect API, please try again"
        alert.value.color = "error"
        return
    }

    isDagActive.value = response?.is_paused == true ? false : true

    alert.value.show = true
    alert.value.message = "Collector status changed to " + (isDagActive.value == true ? "active" : "paused")
    alert.value.color = "success"
}

const run_dag = async () => {
    if (isDagActive.value == false) {
        alert.value.show = true
        alert.value.message = "You need to activate the collector first"
        alert.value.color = "error"
        return
    }
    if (runs.value.state == 'running') {
        alert.value.show = true
        alert.value.message = "Collector already running"
        alert.value.color = "warning"
        return
    }
    const response = await trigger_dag();
    if (response == null) {
        alert.value.show = true
        alert.value.message = "cant trigger the run dag"
        alert.value.color = "error"
        return
    }
    await fetchData()
}



const date_format = (timestamp) => {

    const date = new Date(timestamp);

    const formatted =
        `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ` +
        `${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;

    return (formatted);
};

const timestamp_format = (timestamp, frequency) => {
    let ts;
    let frequ;
    if (frequency == 0) {
        if (timestamp == 0) {
            ts = null
        }
        else {
            ts = timestamp
        }

        frequ = 0
    }
    else {
        if (timestamp == 0) {
            ts = Date.now() / 1000
        }
        else {
            ts = timestamp
        }

        frequ = frequency
    }

    if (ts == null) {
        return null
    }


    const d = ts + frequ * 3600;
    const date = new Date(d * 1000); // Convert to milliseconds
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months start at 0
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

const string_to_json = (str) => {

    // Step 1: Replace single quotes with double quotes (naively)
    const jsonStr = str.replace(/'/g, '"').replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false');;

    // Step 2: Parse JSON
    let arr = [];
    try {
        arr = JSON.parse(jsonStr);
        return arr
    } catch (e) {
        console.error('Failed to parse JSON:', e);
    }
}

const source_logo = (source) => {
    const iconFileName = source + ".png";
    const iconName = "/src/assets/images/sources/" + iconFileName;
    const iconModule = new URL(iconName, import.meta.url).href;
    return iconModule || iconSocial;
};

const alert = ref({
    show: false,
    message: "",
    color: "success",
})

</script>

<template>

    <div>
        <v-snackbar :color="alert.color" v-model="alert.show">
            {{ alert.message }}

            <template v-slot:actions>
                <v-btn color="pink" variant="text" @click="alert.show = false">
                    Close
                </v-btn>
            </template>
        </v-snackbar>
        <div class="d-flex justify-space-between">
            <h1 class="text-4xl font-bold mb-4">Collect</h1>
            <div class="d-flex align-center" v-if="loading == true">
                <span class="me-4">Auto Refresh</span>
                <VProgressCircular class="my-5" :class="(loading == true) ? 'd-block' : 'd-none'" :size="30"
                    color="primary" indeterminate />
            </div>

        </div>

        <v-row>
            <v-col>
                <VCard>
                    <VCardText>
                        <div class="d-flex gap-4">
                            <div class="border-e-sm pe-4">
                                <div>
                                    <v-switch color="success" :label="isDagActive == true ? 'Active' : 'Paused'"
                                        v-model="isDagActive" @update:modelValue="toggleDag"></v-switch>
                                </div>
                            </div>
                            <div class="border-e-sm pe-4">
                                <div class="d-flex">
                                    <h4 class="me-3">Last Run : </h4>
                                    <span>{{ date_format(runs?.execution_date) }}</span>
                                </div>
                            </div>
                            <div class="border-e-sm pe-4">
                                <div class="d-flex">
                                    <h4 class="me-3">Next Run : </h4>
                                    <span>{{ date_format(dag?.next_dagrun) }}</span>
                                </div>
                            </div>
                            <div class="border-e-sm pe-4  me-auto">
                                <span class="me-4">Current status</span>
                                <v-chip v-if="runs?.state == 'running'" color="success">
                                    Running
                                </v-chip>
                                <v-chip v-if="runs?.state == 'success'" color="secondary">
                                    Scheduled
                                </v-chip>
                                <v-chip v-if="runs?.state == 'failed'" color="error">
                                    Failed
                                </v-chip>
                            </div>
                            <div class="pe-4">
                                <v-btn density="compact" color="info" @click="run_dag">Run now</v-btn>
                            </div>

                        </div>
                    </VCardText>
                    <v-progress-linear v-if="runs?.state == 'running'" v-model="runs_progress"
                        color="success"></v-progress-linear>
                </VCard>
            </v-col>
        </v-row>

        <v-row class="mt-5">
            <v-col>
                <VCard>
                    <VCardText class="py-0">
                        <v-list v-if="checked_sources != null">
                            <v-list-item v-for="(source, index) in sources" :class="{
                                'border-b-sm': index !== sources.length - 1,
                                'pa-4': true
                            }" :key="source.id" color="secondary">
                                <div class="d-flex mb-3">
                                    <VAvatar size="30" class="me-4">
                                        <VImg :src="source_logo(source.name)" />
                                    </VAvatar>
                                    <h2 class="font-weight-regular text-capitalize">
                                        {{ source.name }}
                                    </h2>
                                </div>
                                <div class="d-flex gap-4 mt-5">
                                    <div class="border-e-sm pe-4">
                                        <div class="d-flex gap-4">
                                            <v-chip v-if="source?.state == true" color="success">
                                                Active
                                            </v-chip>
                                            <v-chip v-if="source?.state == false" color="error">
                                                Deactive
                                            </v-chip>
                                        </div>
                                    </div>
                                    <div class="border-e-sm pe-4">
                                        <div class="d-flex">
                                            <h4 class="me-3">Last Run : </h4>
                                            <span>{{ source?.state == true ? timestamp_format(source?.last_execution, 0)
                                                : ''
                                                }}</span>
                                        </div>
                                    </div>
                                    <div class="border-e-sm pe-4">
                                        <div class="d-flex">
                                            <h4 class="me-3">Next Run : </h4>
                                            <span>{{ source?.state == true ?
                                                timestamp_format(source?.last_execution,source?.frequency): '' }}</span>
                                        </div>
                                    </div>
                                    <div class=" pe-4  me-auto">
                                        <span class="me-4">Current status</span>
                                        <v-chip
                                            v-if="sources_status.find(item => item.id === source?.id)?.state == 'running'"
                                            color="success">
                                            Running
                                        </v-chip>
                                        <v-chip
                                            v-if="sources_status.find(item => item.id === source?.id)?.state == 'success'"
                                            color="secondary">
                                            Scheduled
                                        </v-chip>
                                        <v-chip
                                            v-if="sources_status.find(item => item.id === source?.id)?.state == 'failed'"
                                            color="error">
                                            Failed
                                        </v-chip>
                                    </div>

                                </div>
                            </v-list-item>
                        </v-list>
                    </VCardText>
                </VCard>
            </v-col>
        </v-row>
    </div>



</template>