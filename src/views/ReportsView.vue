<template>
  <div class="main-page">
    <div class="main-header">
      <p class="h1-style">Reports</p>
      <p>Coming soon...</p>
      <p>For now, use the following link</p>
      <a
        href="https://app.powerbi.com/groups/00c58706-93bc-4ec1-84d9-0b51d7d6561e/reports/e617e09b-0285-442d-b16c-cbfff8c5db22/ReportSection?experience=power-bi"
        target="_blank"
        >Power Bi Reports</a
      >
      <p class="h1-style">Exports</p>
      <div class="row">
        <p>Coming soon...</p>
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
      </div>

      <!-- <p class="h1-style">LtC Export</p>
      <div class="row">
        <div class="col-md-4">
          <zoa-button label="JSON LtC Export" @click="downloadLtcExport" />
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
// import SelectComp from '@/components/SelectComp.vue';
import { downloadCSV, downloadLtCjson } from '@/services/dataService';
import { useLoadingStore } from '@/stores/loadingStore';

export default {
  components: {
    // SelectComp,
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

<style scoped></style>

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
    <p class="h2-style">Power BI Embedded Report</p>
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
