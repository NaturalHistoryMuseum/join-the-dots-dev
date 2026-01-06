<template>
  <div
    v-for="change in change_log"
    :key="change.change_log_id"
    class="change-log-entry"
  >
    <div v-html="change.log"></div>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'ChangeLog',
  components: {},
  data() {
    return {
      change_log: [],
    };
  },
  created() {
    this.getChangeLog();
  },
  methods: {
    async getChangeLog() {
      const resp = await getGeneric('change-log');
      this.change_log = resp;
    },
  },
};
</script>
