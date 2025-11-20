<template>
  <OverlayMessage />
  <p v-if="edit_mode">
    Please note all changes will be immediately reflected in the application.
  </p>
  <div class="guidance-control" v-if="edit_mode">
    <zoa-button
      label="Add New Guidance"
      @click="addTempGuidance"
      v-if="!edit_guidance"
    />
  </div>
  <div v-if="guidance_data.length > 0">
    <div
      v-for="guidance in guidance_data.sort(
        (a, b) => a.guidance_id - b.guidance_id,
      )"
      :key="guidance.guidance_id"
    >
      <AccordionGeneric
        :accordion_open="expanded_accordion === guidance.guidance_id"
        :accordion_title="guidance.header"
        :accordion_open_function="toggleAccordion"
        :accordion_eror="false"
        :accordion_id="guidance.guidance_id"
      >
        <div v-if="!edit_guidance">
          <div class="guidance-control" v-if="edit_mode">
            <zoa-button @click="edit_guidance = true">Edit Guidance</zoa-button>
            <zoa-button @click="deleteGuidance" class="confirm-btn">
              Delete Guidance
            </zoa-button>
          </div>
          <div v-html="guidance.guidance"></div>
        </div>
        <div v-else>
          <div class="guidance-control">
            <zoa-button @click="saveGuidance(guidance)">
              {{
                guidance.guidance_id === 0 ? 'Create Guidance' : 'Save Changes'
              }}
            </zoa-button>
            <zoa-button @click="resetGuidanceTab">
              {{
                guidance.guidance_id === 0
                  ? 'Dicard Guidance'
                  : 'Dicard Changes'
              }}
            </zoa-button>
          </div>
          <div class="field-container guidance-field">
            <zoa-input
              v-model="guidance.header"
              zoa-type="textbox"
              label="Guidance Header"
            />
          </div>
          <div class="field-container">
            <zoa-input
              zoa-type="empty"
              label="Guidance Content"
              class="comments-title"
            />
          </div>
          <RichEditor
            :model_value="guidance.guidance"
            @update:model_value="
              (new_guidance) => (guidance.guidance = new_guidance)
            "
          />
        </div>
      </AccordionGeneric>
    </div>
  </div>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import OverlayMessage from '@/components/OverlayMessage.vue';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { useMessagesStore } from '@/stores/messages';
import RichEditor from '../RichEditor.vue';

export default {
  name: 'GuidanceView',
  props: { edit_mode: { type: Boolean, default: false } },
  components: { AccordionGeneric, RichEditor, OverlayMessage },
  data() {
    return {
      guidance_data: '',
      expanded_accordion: null,
      edit_guidance: false,
      delete_guidance: false,
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  mounted() {
    this.fetchGuidance();
  },
  methods: {
    async fetchGuidance() {
      const resp = await getGeneric('all-guidance');
      this.guidance_data = resp;
    },
    resetGuidanceTab() {
      this.fetchGuidance();
      this.edit_guidance = false;
    },
    async saveGuidance(guidance) {
      this.edit_guidance = false;
      let resp = null;
      // Add new guidance if it is temp - Edit otherwise
      if (guidance.guidance_id === 0) {
        resp = await submitDataGeneric('add-guidance', guidance);
      } else {
        resp = await submitDataGeneric('update-guidance', guidance);
      }
      // Add save message if successful
      if (resp) {
        this.store.handleChangeResponse(resp);
      }
      // Refresh guidance data
      this.fetchGuidance();
    },
    toggleAccordion(accord_id) {
      this.edit_guidance = false;
      if (this.expanded_accordion === accord_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accord_id;
      }
    },
    addTempGuidance() {
      this.guidance_data.push({
        guidance_id: 0,
        header: 'New Guidance Header',
        guidance: '<p>New guidance content here...</p>',
      });
      this.expanded_accordion = 0;
      this.edit_guidance = true;
    },
    async deleteGuidance() {
      const resp = await submitDataGeneric('remove-guidance', {
        guidance_id: this.expanded_accordion,
      });
      // Add save message if successful
      if (resp) {
        this.store.handleChangeResponse(resp);
      }
      // Refresh guidance data
      this.fetchGuidance();
    },
  },
};
</script>

<style>
.guidance-control {
  margin: 1rem 0;
  display: flex;
  justify-content: space-between;
}

.guidance-field {
  margin-bottom: 1rem;
}
</style>
