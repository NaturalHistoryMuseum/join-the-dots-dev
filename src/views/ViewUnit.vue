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
  <div v-if="unit_create_success" class="main-page">
    <zoa-flash kind="success" header="Unit Successfully Created">
      <p>
        The unit <strong>{{ unit.unit_name }}</strong> has been successfully
        created with ID: <strong>{{ this.new_unit_id }}</strong>
      </p>
      <zoa-button label="Go to Unit" @click="navNewUnit()" />
    </zoa-flash>
  </div>
  <div v-else class="main-page">
    <div class="main-header">
      <div class="row" v-if="(unit && unit_id) || !add_unit_mode">
        <div class="col-md-4">
          <h1>View{{ allow_edit ? ' / Edit' : '' }} Unit</h1>
          <p>Unit ID: {{ unit_id }}</p>
        </div>
        <div class="col-md-8" v-if="allow_edit">
          <ActionsBtnGroup>
            <DeleteModal :selected_units="[unit]" :navigate_on_success="true" />
            <SplitModal :selected_unit="unit" :navigate_on_success="true" />
          </ActionsBtnGroup>
        </div>
      </div>
      <div v-else class="row">
        <div class="col-md-6">
          <h1>Add New Unit</h1>
          <p>
            Please fill out all required units (<span style="color: red">*</span
            >) and the scoring page to create this unit.
          </p>
        </div>
        <div class="col-md-3">
          <div class="required-message">
            Required fields completion:
            <div class="round-prog-bar">
              <RoundProgressBar :progress="countRequiredFields()" />
            </div>
          </div>
          <div class="required-message">
            Scoring completion:
            <div class="round-prog-bar">
              <RoundProgressBar :progress="scores_percentage" />
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <!-- Button to create unit - only visible when unit is ready -->
          <zoa-button
            v-if="scores_percentage == 100 && countRequiredFields() == 100"
            label="Create Unit"
            @click="submitUnit()"
          />
        </div>
      </div>
      <!-- {{ this.unit }} -->
      <TopTabs
        :tabs="unit_sections"
        :active_tab="active_tab"
        :changeTabFunc="changeTab"
      >
        <div v-if="(unit && unit_id) || add_unit_mode">
          <!-- Unit Details -->
          <!-- <div v-if="active_tab == 0" class="content row">
            <DetailsTab
              :unit="unit"
              :department_id="current_section.department_id"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div> -->
          <!-- Section -->
          <!-- <div v-if="active_tab == 1" class="content row">
            <SectionTab
              :unit="unit"
              :current_section="current_section"
              :section_options="section_options"
              :setCurrentSection="setCurrentSection"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div> -->
          <!-- Properties -->
          <!-- <div v-if="active_tab == 2" class="content row">
            <PropertiesTab
              :unit="unit"
              :department_id="current_section.department_id"
              :handleFieldChange="handleFieldChange"
              :allow_edit="allow_edit"
            />
          </div> -->
          <!-- Storage -->
          <!-- <div v-if="active_tab == 3" class="content row">
            <StorageTab
              :unit="unit"
              :handleFieldChange="handleFieldChange"
              :errors="errors"
              :allow_edit="allow_edit"
            />
          </div> -->
          <!-- Scores -->
          <!-- <div v-show="active_tab == 4" class="content row">
            <ScoresTab
              :unit="unit"
              :unit_id="unit_id"
              :add_unit_mode="add_unit_mode"
              @update:scores_percentage="scores_percentage = $event"
              @new_unit="scored_unit = $event"
            />
          </div> -->
          <!-- Comments -->
          <!-- <div v-if="active_tab == 5" class="content row">
            <CommentsTab :unit="unit" />
          </div> -->
          <div v-if="unit_sections.length > 0">
            <div
              v-for="section in unit_sections"
              :key="section.section_id"
              class="content row"
              v-show="active_tab == section.section_id"
            >
              <!-- <h4 class="subheading">{{ section.section_name }}</h4> -->
              <div
                v-if="section.sub_sections && section.sub_sections.length > 0"
              >
                <div
                  v-for="sub in section.sub_sections"
                  :key="sub.sub_section_id"
                >
                  <h4 class="subheading">{{ sub.sub_section_name }}</h4>
                  <div
                    v-if="sub.fields && sub.fields.length > 0"
                    class="fields-box"
                  >
                    <div
                      v-for="field in sub.fields"
                      :key="field.field_name"
                      class="custom-field"
                    >
                      <CustomField
                        :field="field"
                        :value="unit[field.field_name]"
                        :allow_edit="allow_edit"
                        @dataChange="handleFieldChange"
                        @updateValue="unit[field.field_name] = $event"
                      />
                    </div>
                  </div>
                  <div
                    v-else-if="
                      sub.component == 'edit-editors' &&
                      curators_options.length > 0 &&
                      allow_edit
                    "
                    class=""
                  >
                    <zoa-input
                      class="field-container"
                      zoa-type="multiselect"
                      label="Please select editors"
                      v-model="assinged_users"
                      @change="handleEditorChange(true)"
                      help="The users who will be able to edit this unit"
                      help-position="right"
                      :config="{
                        options: curators_options,
                        itemName: 'Curator',
                        itemNamePlural: 'Curators',
                        placeholder: 'Please select....',
                        enableSearch: true,
                      }"
                    />
                    <div class="fields-box">
                      <div
                        v-for="user_id in assinged_users"
                        :key="user_id.value"
                        class="field-editor"
                      >
                        <div>
                          <div class="editor-title">
                            {{
                              curators_options.find((u) => u.value == user_id)
                                .label
                            }}
                          </div>
                          <div class="editor-title">
                            {{
                              curators_options.find((u) => u.value == user_id)
                                .email
                            }}
                          </div>
                        </div>
                        <div v-if="user_id != unit.responsible_curator_id">
                          <zoa-button
                            class="remove-btn"
                            @click="removeEditor(user_id)"
                          >
                            <i class="bi bi-x-lg"></i>
                          </zoa-button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else>
                <ScoresTab
                  :unit="unit"
                  :unit_id="unit_id"
                  :add_unit_mode="add_unit_mode"
                  @update:scores_percentage="scores_percentage = $event"
                  @new_unit="scored_unit = $event"
                />
              </div>
            </div>
          </div>
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
import ActionsBtnGroup from '@/components/ActionsBtnGroup.vue';
import SmallMessages from '@/components/SmallMessages.vue';
// import DetailsTab from '@/components/unit sections/DetailsTab.vue';
// import PropertiesTab from '@/components/unit sections/PropertiesTab.vue';
import ScoresTab from '@/components/unit sections/ScoresTab.vue';
// import SectionTab from '@/components/unit sections/SectionTab.vue';
// import StorageTab from '@/components/unit sections/StorageTab.vue';
import { currentUser } from '@/services/authService';

import DeleteModal from '@/components/modals/DeleteModal.vue';
import SplitModal from '@/components/modals/SplitModal.vue';
import RoundProgressBar from '@/components/RoundProgressBar.vue';
import CustomField from '@/components/unit sections/CustomField.vue';

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
    // CommentsTab,
    ScoresTab,
    // StorageTab,
    // PropertiesTab,
    // SectionTab,
    // DetailsTab,
    SmallMessages,
    ActionsBtnGroup,
    RoundProgressBar,
    CustomField,
    SplitModal,
    DeleteModal,
  },
  data() {
    return {
      unit: [],

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
      add_unit_mode: true,
      scores_percentage: 0,
      scored_unit: [],
      unit_create_success: false,
      unit_sections: [],
      assinged_users: [],
      curators_options: [],
    };
  },
  setup() {
    return { currentUser };
  },
  created() {
    this.setUnitSections();
    this.unit_id = this.$route.query.unit_id;
    if (this.unit_id == undefined || this.unit_id == null) {
      this.add_unit_mode = true;
      this.allow_edit = true;
      this.unit = {
        collection_unit_id: 0,
        unit_name: '',
        section_id: null,
        public_unit_name: '',
        storage_room_id: null,
        curatorial_unit_definition_id: null,
        publish_flag: 'yes',
        unit_active: 'yes',
      };
    } else {
      this.add_unit_mode = false;
      this.fetchUnitData();
    }
    this.fetchSectionOptions();
    this.fetchAssignedUsers();
    this.fetchAllCurators();
  },
  methods: {
    async setUnitSections() {
      const data = await import('../utils/unit_sections.json');
      this.unit_sections = data.default;
    },
    async fetchAssignedUsers() {
      const resp = await getGeneric(`all-assigned-users/${this.unit_id}`);
      this.assinged_users = resp.map((user) => user.user_id);
      console.log(this.assinged_users);
    },
    async fetchAllCurators() {
      this.curators_options = await getGeneric(`all-curators`);
    },
    async fetchUnitData() {
      if (!this.add_unit_mode && this.unit_id) {
        let unitData = await getGeneric(`full-unit/${this.unit_id}`);
        this.unit = unitData[0];
        this.handleEditorChange(false);
        // Check if the unit is assigned to the current user
        if (this.currentUser.assigned_units) {
          this.allow_edit = JSON.parse(
            this.currentUser.assigned_units,
          ).includes(this.unit.collection_unit_id);
        } else {
          this.allow_edit = false;
        }
      }
    },
    removeEditor(user_id) {
      this.assinged_users = this.assinged_users.filter(
        (user) => user != user_id,
      );
      this.handleEditorChange(true);
    },
    async handleEditorChange(submit = false) {
      if (!this.assinged_users.includes(this.unit.responsible_curator_id)) {
        this.assinged_users.push(this.unit.responsible_curator_id);
      }
      if (submit) {
        const response = await submitDataGeneric('submit-unit-assigned', {
          unit_id: this.unit.collection_unit_id,
          assinged_users: this.assinged_users,
        });
        if (response.success) {
          this.messages.push({
            message_text: 'Change saved!',
            message_type: 'success',
          });
          this.removeMessage();
        } else {
          this.messages.push({
            message_text: 'Change not saved!',
            message_type: 'error',
          });
          this.removeMessage();
        }
      }
    },
    fetchSectionOptions() {
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
    countRequiredFields() {
      let total_fields = this.required_fields.length;
      let filled_fields = 0;
      // Go through each key of the unit object
      for (const property in this.unit) {
        // Check if the property has data
        if (
          this.checkRequired(property) &&
          this.unit[property] !== null &&
          this.unit[property] !== ''
        ) {
          filled_fields++;
        }
      }
      // Return percentage of required fields completed
      return ((filled_fields / total_fields) * 100 || 0).toFixed(2);
    },
    checkRequired(field_name) {
      return this.required_fields.includes(field_name);
    },

    async handleFieldChange(field_name, new_value) {
      // If not allowed to edit or in add mode, do nothing
      this.countRequiredFields();
      if (!this.allow_edit || this.add_unit_mode) return;
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
          this.fetchUnitData();
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
    submitUnit() {
      // If not allowed to edit or in add mode, do nothing
      if (!this.allow_edit || !this.add_unit_mode) return;
      // Check if all required fields are filled
      if (this.countRequiredFields() < 100) {
        this.messages.push({
          message_text: 'Please fill all required fields',
          message_type: 'error',
        });
        this.removeMessage();
        return;
      }
      // Submit the unit data
      submitDataGeneric('submit-unit', {
        unit_data: this.unit,
        score_data: this.scored_unit,
      }).then((response) => {
        if (response.success) {
          this.unit_create_success = true;
          this.new_unit_id = response.collection_unit_id;
        } else {
          this.messages.push({
            message_text: 'Error saving unit',
            message_type: 'error',
          });
          this.removeMessage();
        }
      });
    },
    navNewUnit() {
      this.$router.push({
        path: '/view-unit',
        query: {
          unit_id: this.new_unit_id,
        },
      });
    },
  },
  computed: {},
};
</script>

<style>
.content {
  margin: 1rem !important;
}

.field {
  padding: 5px;
}

.fields-box {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  text-align: left;
  width: 100%;
}
.subheading {
  text-align: left;
  margin: 1rem 0;
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

.field-editor {
  margin: 0.5rem 0;
  padding: 0 0.5rem;
  width: 25vw;
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
}

.remove-btn {
  background-color: #ff5957 !important;
  color: white !important ;
}

.editor-title {
  margin: 0.5rem;
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
  position: fixed;
  /* padding-top: 30rem; */
  left: 85%;
  z-index: 1;
  pointer-events: none;
  gap: 1rem;
}

.required-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1rem;
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
