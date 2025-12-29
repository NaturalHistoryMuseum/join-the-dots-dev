<template>
  <OverlayMessage />
  <zoa-button @click="addTempLog">Add New Change Log</zoa-button>
  <div
    v-for="change in change_log"
    :key="change.change_log_id"
    class="change-log-entry"
  >
    <AccordionGeneric
      :accordion_open="expanded_accordion === change.change_log_id"
      :accordion_title="change.title"
      :accordion_open_function="toggleAccordion"
      :accordion_eror="false"
      :accordion_id="change.change_log_id"
    >
      <div class="guidance-control">
        <zoa-button
          v-if="change.change_log_id > 0"
          @click="updateChangeLog(change)"
          >Save Changes</zoa-button
        >
        <zoa-button v-else @click="addChangeLog(change)"
          >Add Change Log</zoa-button
        >
        <zoa-button @click="refreshPage()">Discard Changes</zoa-button>
      </div>
      <div class="field-container">
        <div class="required-tag">*</div>
        <zoa-input
          v-model="change.title"
          zoa-type="textbox"
          label="Change Log Title"
        />
      </div>
      <RichEditor
        :model_value="change.log"
        @update:model_value="(new_log) => (change.log = new_log)"
      />
    </AccordionGeneric>
  </div>
</template>

<script>
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { useMessagesStore } from '@/stores/messages';
import AccordionGeneric from '../AccordionGeneric.vue';
import OverlayMessage from '../OverlayMessage.vue';
import RichEditor from '../RichEditor.vue';

export default {
  name: 'ChangeLog',
  components: { AccordionGeneric, RichEditor, OverlayMessage },
  data() {
    return {
      change_log: [],
      expanded_accordion: null,
      new_change_log: {
        change_log_id: 0,
        title: 'New Change Log Entry',
        log: '<h1>1.[VERSION]</h1><h2>[MONTH] 2026</h2><hr><p>[SUMMARY]</p><hr><h5>User Changes:</h5><ul><li><p>[change 1]</p></li><li><p>[change 2]</p></li><li><p>[change 3]</p></li></ul><h5>Technical Changes:</h5><ul><li><p>[change 1]</p></li><li><p>[change 2]</p></li><li><p>[change 3]</p></li></ul><p></p>',
      },
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  created() {
    this.getChangeLog();
  },
  methods: {
    refreshPage() {
      this.expanded_accordion = null;
      this.getChangeLog();
    },
    async getChangeLog() {
      const resp = await getGeneric('change-log');
      this.change_log = resp;
    },
    addTempLog() {
      this.change_log.unshift(this.new_change_log);
      this.expanded_accordion = 0;
    },
    async addChangeLog(change_log) {
      const resp = await submitDataGeneric('add-change-log', change_log);
      this.store.handleChangeResponse(resp);
      this.getChangeLog();
    },
    async updateChangeLog(change_log) {
      const resp = await submitDataGeneric('update-change-log', change_log);
      this.store.handleChangeResponse(resp);
      this.getChangeLog();
    },
    toggleAccordion(accord_id) {
      if (this.expanded_accordion === accord_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accord_id;
      }
    },
  },
};
</script>
