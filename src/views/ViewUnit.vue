<template>
  <div class="main-page">
    <div class="main-header">
      <h1>View Unit</h1>
      <p>Unit ID: {{ unit_id }}</p>
      <TopTabs :tabs="tabs" :active_tab="active_tab" :changeTabFunc="changeTab">
        <div v-if="unit && unit_id">
          <!-- Unit Details -->
          <div v-if="active_tab == 0" class="content row">
            <DetailsTab :unit="unit" :department_id="current_section.department_id" />
          </div>
          <!-- Section -->
          <div v-if="active_tab == 1" class="content row">
            <SectionTab
              :unit="unit"
              :current_section="current_section"
              :section_options="section_options"
              :setCurrentSection="setCurrentSection"
            />
          </div>
          <!-- Properties -->
          <div v-if="active_tab == 2" class="content row">
            <PropertiesTab :unit="unit" :department_id="current_section.department_id" />
          </div>
          <!-- Storage -->
          <div v-if="active_tab == 3" class="content row">
            <StorageTab :unit="unit" />
          </div>
          <!-- Scores -->
          <div v-show="active_tab == 4" class="content row">
            <ScoresTab :unit="unit" :unit_id="unit_id" />
          </div>
          <!-- Comments -->
          <div v-if="active_tab == 5" class="content row">
            <CommentsTab :unit="unit" />
            <!-- <div class="col-md-6 field">
              <zoa-input zoa-type="empty" label="Unit Comments" class="comments-title" />
              <textarea class="text-area" rows="7" v-model="unit.unit_comment"></textarea>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Date Comment Added" class="comments-title" />
              <p class="view-field">{{ unit.date_comment_added }}</p>
            </div> -->
          </div>
        </div>
      </TopTabs>
    </div>
  </div>
</template>

<script>
import TopTabs from '@/components/TopTabs.vue'
import { getGeneric } from '@/services/dataService'
import fieldNameCalc from '@/utils/utils'
import CommentsTab from '@/components/unit sections/CommentsTab.vue'
import ScoresTab from '@/components/unit sections/ScoresTab.vue'
import StorageTab from '@/components/unit sections/StorageTab.vue'
import PropertiesTab from '@/components/unit sections/PropertiesTab.vue'
import SectionTab from '@/components/unit sections/SectionTab.vue'
import DetailsTab from '@/components/unit sections/DetailsTab.vue'

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
    CommentsTab,
    ScoresTab,
    StorageTab,
    PropertiesTab,
    SectionTab,
    DetailsTab,
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
        { id: 5, label: 'Comments' },
      ],

      active_tab: 0,

      section_options: [],
      current_section: {},
      unit_id: null,
    }
  },
  created() {
    this.unit_id = this.$route.query.unit_id
    this.fetchData()
    console.log('call to get data')
  },
  methods: {
    async fetchData() {
      let unitData = await getGeneric(`full-unit/${this.unit_id}`)
      this.unit = unitData[0]
      console.log('there is a unit: ', this.unit)
      getGeneric(`all-sections`).then((response) => {
        this.section_options = response.map((section) => ({
          ...section,
          label: section.section_name,
          value: section.section_id,
        }))
        this.setCurrentSection()
      })
    },
    fieldNameCalc,
    changeTab(index) {
      this.active_tab = index
    },

    setCurrentSection() {
      if (this.unit.section_id == null) {
        this.current_section = {
          value: null,
          section_name: null,
          division_name: null,
          department_name: null,
        }
      } else {
        this.current_section = this.section_options.filter(
          (section) => section.section_id == this.unit.section_id,
        )[0]
      }
    },
  },
  computed: {},
}
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
  height: 1rem;
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
</style>
