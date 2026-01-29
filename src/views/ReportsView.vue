<template>
  <div class="main-page">
    <div class="main-header">
      <h1 class="h1-style">Power BI Report</h1>
      <iframe
        title="Join The Dots Data"
        class="powerbi-frame"
        src="https://app.powerbi.com/reportEmbed?reportId=d640bea6-f574-4bab-a2e7-0cd37d3fba39&autoAuth=true&ctid=73a29c01-4e78-437f-a0d4-c8553e1960c1&actionBarEnabled=true"
        frameborder="0"
        allowFullScreen="true"
      ></iframe>
      <!-- <p>For now, use the following link</p> -->
      <p>
        <a
          href="https://app.powerbi.com/links/kVh2Sta1yX?ctid=73a29c01-4e78-437f-a0d4-c8553e1960c1&pbi_source=linkShare"
          target="_blank"
          >Power Bi Report</a
        >
      </p>
      <!-- <h1 class="h1-style">Exports</h1>
      <div class="row">
        <p>Coming soon...</p> -->
      <!-- <div class="col-md-4">
          <SelectComp
            :options="[
              { value: 'vw_unit_rescore_form', label: 'Rescore View' },
              {
                value: 'vw_collections_hierarchy',
                label: 'Collections Hierarchy',
              },
            ]"
            label="View"
            :onChangeFunc="handleViewSelect"
            :multi="false"
          />
        </div> -->
      <!-- <div class="col-md-4">
          <SelectComp
            :options="[
              { value: 'vw_unit_rescore_form', label: 'Rescore View' },
              { value: 'vw_collections_hierarchy', label: 'Collections Hierarchy' },
            ]"
            label="Section"
            :onChangeFunc="handleViewSelect"
            :multi="false"
          />
        </div> -->
      <!-- <div class="col-md-4">
          <zoa-button
            label="Download export to csv (only press once)"
            @click="downloadScoreView"
            :disabled="!viewVal"
          />
        </div> -->
      <!-- </div> -->

      <!-- <p class="h1-style">LtC Export</p>
      <div class="row">
        <div class="col-md-4">
          <zoa-button label="JSON LtC Export" @click="downloadLtcExport" />
        </div>
      </div> -->
      <ExportFilters />
    </div>
  </div>
</template>

<script>
// import SelectComp from '@/components/SelectComp.vue';
import ExportFilters from '@/components/ExportFilters.vue';
import { downloadCSV, downloadLtCjson } from '@/services/dataService';
import { useLoadingStore } from '@/stores/loadingStore';

export default {
  components: {
    // SelectComp,
    ExportFilters,
  },
  data() {
    return {
      viewVal: '',
      sectionVal: '',
    };
  },
  methods: {
    async downloadScoreView() {
      const loadingStore = useLoadingStore();
      try {
        loadingStore.startLoading();
        await downloadCSV(this.viewVal);
      } catch (error) {
        console.error('Error downloading CSV:', error);
      } finally {
        loadingStore.stopLoading();
      }
    },
    handleViewSelect(value) {
      this.viewVal = value;
    },
    handleSectionSelect(value) {
      this.sectionVal = value;
    },
    async downloadLtcExport() {
      const loadingStore = useLoadingStore();
      try {
        loadingStore.startLoading();
        await downloadLtCjson();
      } catch (error) {
        console.error('Error downloading LtC export:', error);
      } finally {
        loadingStore.stopLoading();
      }
    },
  },
};
</script>

<style scoped>
.powerbi-frame {
  width: 100%;
  height: 70vh;
}
</style>

<!-- <template>
  <div>
    <PowerBIReportEmbed
      :embedConfig="embedConfig"
      :cssClassName="'reportClass'"
      :phasedEmbedding="false"
      :eventHandlers="eventHandlers"
    ></PowerBIReportEmbed>

    <PowerBIReportEmbed
      :embedConfig="embedConfig"
      :cssClassName="'reportClass'"
      :phasedEmbedding="false"
      :eventHandlers="eventHandlers"
    ></PowerBIReportEmbed>
  </div>
</template>

<script>
import { PowerBIReportEmbed } from 'powerbi-client-vue-js'
import * as pbi from 'powerbi-client'

export default {
  components: {
    PowerBIReportEmbed,
  },
  data() {
    return {
      embedConfig: {
        type: 'report',
        id: 'e617e09b-0285-442d-b16c-cbfff8c5db22',
        embedUrl:
          'https://app.powerbi.com/reportEmbed?reportId=e617e09b-0285-442d-b16c-cbfff8c5db22&autoAuth=true&ctid=73a29c01-4e78-437f-a0d4-c8553e1960c1',
        accessToken: undefined, // Keep as empty string, null or undefined
        tokenType: pbi.models.TokenType.Embed,
        hostname: 'https://app.powerbi.com',
      },
    }
  },
}
</script>

<style>
.reportClass {
  width: 100%;
  height: 100vh;
}
</style> -->
<!--
<template>
  <div>
    <h2 class="h2-style">Power BI Embedded Report</h2>
    <div ref="reportContainer" style="width: 800px; height: 600px"></div>
  </div>
</template>

<script>
import * as powerbi from 'powerbi-client'

export default {
  async mounted() {
    try {
      const response = await fetch('http://localhost:5000/api/report/get-embed-url')
      const { embedUrl, accessToken } = await response.json()

      const embedConfig = {
        type: 'report',
        tokenType: powerbi.models.TokenType.Aad,
        accessToken: accessToken,
        embedUrl: embedUrl,
        settings: {
          filterPaneEnabled: false,
          navContentPaneEnabled: false,
        },
      }

      const powerbiService = new powerbi.service.Service(
        powerbi.factories.hpmFactory,
        powerbi.factories.wpmpFactory,
        powerbi.factories.routerFactory,
      )

      const reportContainer = this.$refs.reportContainer
      powerbiService.embed(reportContainer, embedConfig)
    } catch (error) {
      console.error('Error embedding Power BI report:', error)
    }
  },
}
</script> -->
