<template>
  <div class="main-page">
    <div class="main-header">
      <h1>Reports</h1>
      <p>Coming soon...</p>
    </div>
  </div>
</template>

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
    <h2>Power BI Embedded Report</h2>
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
