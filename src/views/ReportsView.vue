<template>
  <div class="main-page">
    <div class="main-header">
      <TopTabs
        :tabs="page_data"
        :active_tab="active_tab"
        :changeTabFunc="changeTab"
      />
      <div class="report-tabs">
        <ExportFilters v-if="active_tab == 1" />
        <div v-if="active_tab == 0">
          <!-- <h1 class="h1-style">Power BI Report</h1> -->
          <iframe
            title="Join The Dots Data"
            class="powerbi-frame"
            src="https://app.powerbi.com/reportEmbed?reportId=d640bea6-f574-4bab-a2e7-0cd37d3fba39&autoAuth=true&ctid=73a29c01-4e78-437f-a0d4-c8553e1960c1&actionBarEnabled=true"
            frameborder="0"
            allowFullScreen="true"
          ></iframe>
          <p>
            <a
              href="https://app.powerbi.com/links/kVh2Sta1yX?ctid=73a29c01-4e78-437f-a0d4-c8553e1960c1&pbi_source=linkShare"
              target="_blank"
              >Power Bi Report</a
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ExportFilters from '@/components/ExportFilters.vue';
import TopTabs from '@/components/TopTabs.vue';

export default {
  components: {
    ExportFilters,
    TopTabs,
  },
  data() {
    return {
      viewVal: '',
      sectionVal: '',
      page_data: [
        {
          section_id: 0,
          section_name: 'Power BI Report',
        },
        {
          section_id: 1,
          section_name: 'Export Data',
        },
      ],
      active_tab: 0,
    };
  },
  methods: {
    changeTab(new_tab) {
      this.active_tab = new_tab;
    },
  },
};
</script>

<style scoped>
.powerbi-frame {
  width: 100%;
  height: 70vh;
}
.report-tabs {
  margin: 1rem;
}
</style>
