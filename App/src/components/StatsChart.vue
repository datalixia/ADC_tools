<script setup>
import VueApexCharts from 'vue3-apexcharts'
import { useTheme } from 'vuetify'
import { hexToRgb } from '@layouts/utils'
const currentTab = ref(0)

const props = defineProps({
  data: {
    type: Array, // assuming 'data' is an array
    required: true // optional, if 'data' is mandatory
  }
})

const chart_data = ref(null)
const series = ref(null)
const categories = ref(null)
watch(
  () => props.data,  // Watch the `data` prop
  (newData, oldData) => {
    // You can perform any logic here that needs to occur when the data changes.
    // For example, reinitialize charts or reset internal state.
    // Example:
    if (newData !== oldData) {
        chart_data.value = newData
        currentTab.value++;
    }
  },
  { immediate: true }  // This ensures the watcher runs immediately on component mount
);

const vuetifyTheme = useTheme()

const refVueApexChart = ref()

const chartConfigs = computed(() => {
  const currentTheme = vuetifyTheme.current.value.colors
  const variableTheme = vuetifyTheme.current.value.variables
  const labelPrimaryColor = `rgba(${ hexToRgb(currentTheme.primary) },${ variableTheme['dragged-opacity'] })`
  const legendColor = `rgba(${ hexToRgb(currentTheme['on-background']) },${ variableTheme['high-emphasis-opacity'] })`
  const borderColor = `rgba(${ hexToRgb(String(variableTheme['border-color'])) },${ variableTheme['border-opacity'] })`
  const labelColor = `rgba(${ hexToRgb(currentTheme['on-surface']) },${ variableTheme['disabled-opacity'] })`


  const categories = chart_data.value ? chart_data.value.map(item => item.date) : [];
  const seriesData = chart_data.value ? chart_data.value.map(item => item.count) : [];
  console.log(seriesData)

  return [
    {
      title: 'Orders',
      icon: 'tabler-shopping-cart',
      chartOptions: {
        chart: {
          parentHeightOffset: 0,
          type: 'bar',
          toolbar: { show: false },
        },
        plotOptions: {
          bar: {
            columnWidth: '32%',
            startingShape: 'rounded',
            borderRadius: 4,
            distributed: true,
            dataLabels: { position: 'top' },
          },
        },
        grid: {
          show: false,
          padding: {
            top: 0,
            bottom: 0,
            left: -10,
            right: -10,
          },
        },
        colors: [
          labelPrimaryColor,
        ],
        dataLabels: {
          enabled: true,

          offsetY: -25,
          style: {
            fontSize: '15px',
            colors: [legendColor],
            fontWeight: '600',
            fontFamily: 'Public Sans',
          },
        },
        legend: { show: false },
        tooltip: { enabled: false },
        xaxis: {
          categories: categories,
          axisBorder: {
            show: true,
            color: borderColor,
          },
          axisTicks: { show: false },
          labels: {
            style: {
              colors: labelColor,
              fontSize: '13px',
              fontFamily: 'Public Sans',
            },
          },
        },
        yaxis: {
          labels: {
            offsetX: -15,

            style: {
              fontSize: '13px',
              colors: labelColor,
              fontFamily: 'Public Sans',
            },
            min: 0,
            max: 60000,
            tickAmount: 6,
          },
        },
        responsive: [
          {
            breakpoint: 1441,
            options: { plotOptions: { bar: { columnWidth: '41%' } } },
          },
          {
            breakpoint: 590,
            options: {
              plotOptions: { bar: { columnWidth: '61%' } },
              yaxis: { labels: { show: false } },
              grid: {
                padding: {
                  right: 0,
                  left: -20,
                },
              },
              dataLabels: {
                style: {
                  fontSize: '12px',
                  fontWeight: '400',
                },
              },
            },
          },
        ],
      },
      series: [{
        data: [...seriesData],
      }],
    },
    
  ]
})
</script>

<template>
  <VCard
    title="Daily articles"
    subtitle="number of articles by day"
  >

    <VCardText>

        <div v-if="chart_data && chart_data.length > 0">  
      <VueApexCharts
        ref="refVueApexChart"
        :key="currentTab"
        :options="chartConfigs[0].chartOptions"
        :series="chartConfigs[0].series"
        height="240"
        class="mt-3"
      />
    </div>
    </VCardText>
  </VCard>
</template>
