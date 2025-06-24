<template>
  <div class="unit-save-msg-container">
    <transition-group name="fade" tag="div" class="message-stack">
      <div v-for="(message, index) in messages" :key="index">
        <SmallMessages
          :message_text="message.message_text"
          :message_type="message.message_type"
          class="unit-save-msg"
        />
      </div>
    </transition-group>
  </div>
  <div class="main-page">
    <div class="main-header">
      <h1>View Unit</h1>
      <p>Unit ID: {{ unit_id }}</p>
      <TopTabs :tabs="tabs" :active_tab="active_tab" :changeTabFunc="changeTab">
        <div v-if="unit && unit_id">
          <!-- Unit Details -->
          <div v-if="active_tab == 0" class="content row">
            <DetailsTab
              :unit="unit"
              :department_id="current_section.department_id"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div>
          <!-- Section -->
          <div v-if="active_tab == 1" class="content row">
            <SectionTab
              :unit="unit"
              :current_section="current_section"
              :section_options="section_options"
              :setCurrentSection="setCurrentSection"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div>
          <!-- Properties -->
          <div v-if="active_tab == 2" class="content row">
            <PropertiesTab
              :unit="unit"
              :department_id="current_section.department_id"
              :handleFieldChange="handleFieldChange"
              :allow_edit="allow_edit"
            />
          </div>
          <!-- Storage -->
          <div v-if="active_tab == 3" class="content row">
            <StorageTab
              :unit="unit"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div>
          <!-- Scores -->
          <div v-show="active_tab == 4" class="content row">
            <ScoresTab :unit="unit" :unit_id="unit_id" />
          </div>
          <!-- Comments -->
          <!-- <div v-if="active_tab == 5" class="content row">
            <CommentsTab :unit="unit" />
          </div> -->
        </div>
      </TopTabs>
    </div>
  </div>
</template>

<script>
import TopTabs from '@/components/TopTabs.vue';
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import fieldNameCalc from '@/utils/utils';
// import CommentsTab from '@/components/unit sections/CommentsTab.vue'
import SmallMessages from '@/components/SmallMessages.vue';
import DetailsTab from '@/components/unit sections/DetailsTab.vue';
import PropertiesTab from '@/components/unit sections/PropertiesTab.vue';
import ScoresTab from '@/components/unit sections/ScoresTab.vue';
import SectionTab from '@/components/unit sections/SectionTab.vue';
import StorageTab from '@/components/unit sections/StorageTab.vue';
import { currentUser } from '@/services/authService';

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
    // CommentsTab,
    ScoresTab,
    StorageTab,
    PropertiesTab,
    SectionTab,
    DetailsTab,
    SmallMessages,
  },
  data() {
    return {
      unit: [],
      tabs: [
        { id: 0, label: 'Unit Details' },
        { id: 1, label: 'Section' },
        { id: 2, label: 'Properties' },
        { id: 3, label: 'Storage' },
        { id: 4, label: 'Scores' },
        // { id: 5, label: 'Comments' },
      ],

      active_tab: 0,

      section_options: [],
      current_section: {},
      unit_id: null,

      messages: [],
      errors: [],
      required_fields: [
        'unit_name',
        'section_id',
        'public_unit_name',
        'storage_room_id',
        'curatorial_unit_definition_id',
      ],
      allow_edit: false,
    };
  },
  setup() {
    return {currentUser};
  },
  created() {
    this.unit_id = this.$route.query.unit_id;
    this.fetchData();
  },
  methods: {
    async fetchData() {
      let unitData = await getGeneric(`full-unit/${this.unit_id}`);
      this.unit = unitData[0];
      // Check if the unit is assigned to the current user
      this.allow_edit = JSON.parse(this.currentUser.assigned_units).includes(this.unit.collection_unit_id)
      getGeneric(`all-sections`).then((response) => {
        this.section_options = response.map((section) => ({
          ...section,
          label: section.section_name,
          value: section.section_id,
        }));
        this.setCurrentSection();
      });
    },
    fieldNameCalc,
    changeTab(index) {
      this.active_tab = index;
    },

    setCurrentSection() {
      if (this.unit.section_id == null) {
        this.current_section = {
          value: null,
          section_name: null,
          division_name: null,
          department_name: null,
        };
      } else {
        this.current_section = this.section_options.filter(
          (section) => section.section_id == this.unit.section_id,
        )[0];
      }
    },

    checkRequired(field_name) {
      return this.required_fields.includes(field_name);
    },

    async handleFieldChange(field_name, new_value) {
      if (this.checkRequired(field_name) && !new_value) {
        this.errors.push({
          field: field_name,
          error: 'This field is required',
        });
        this.messages.push({
          message_text: 'Field is required! Not saved',
          message_type: 'error',
        });
        this.removeMessage();
      } else {
        try {
          // Set data for the field
          const data = {
            field_name: field_name,
            new_value: new_value,
            collection_unit_id: this.unit_id,
          };
          // Submit the data
          const resp = await submitDataGeneric('submit-field', data);
          // If the data is saved correctly
          if (resp.success) {
            this.messages.push({
              message_text: 'Change saved!',
              message_type: 'success',
            });
            this.removeMessage();
          } else {
            this.messages.push({
              message_text: 'Change not saved',
              message_type: 'error',
            });
            this.removeMessage();
          }
          this.fetchData();
        } catch (error) {
          console.error('Submission error:', error);

          this.messages.push({
            message_text: 'Error saving change. Please try again.',
            message_type: 'error',
          });
          this.removeMessage();
        }
      }
    },
    removeMessage() {
      setTimeout(() => {
        this.messages.shift();
      }, 3000);
    },
  },
  computed: {
    // allowEdit() {
    //   // Allow edit if the user is an admin or the unit is assigned to them
    //   return (
    //     this.currentUser.level > 3 ||
    //     JSON.parse(this.currentUser.assigned_units).includes(this.unit.collection_unit_id)
    //   )
    // }
  },
};
</script>

<style>
.content {
  margin: 1rem !important;
}

.field {
  padding: 5px;
}

.text-area {
  width: 100%;
  height: 50%;
  border-radius: 10px;
  padding: 8px 16px;
}

.view-field {
  margin: 0 1.5rem;
  min-height: 1rem;
}

.subheading {
  margin-top: 1rem;
}

.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.required-tag {
  color: red;
  margin-bottom: -1.5rem;
}

.error-field .zoa__textbox__input {
  border: 1px solid red !important;
  border-radius: 10px;
}
.error-field .zoa__dropdown__input {
  border: 1px solid red !important;
  border-radius: 10px;
}
.unit-save-msg {
  margin-top: 1rem;
  margin-bottom: -3rem;
}

.unit-save-msg-container {
  position: absolute;
  top: 20rem;
  left: 85%;
  z-index: 1;
  pointer-events: none;
  gap: 1rem;
}

.message-stack {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}
</style>
