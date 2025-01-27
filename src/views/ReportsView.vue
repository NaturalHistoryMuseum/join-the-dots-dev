<template>
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
</style>
