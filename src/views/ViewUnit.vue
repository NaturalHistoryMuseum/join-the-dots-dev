<template>
  <div class="main-page">
    <div class="main-header">
      <h1>View Unit</h1>
      <p>Unit ID: {{ unitId }}</p>
      <TopTabs :tabs="tabs" :activeTab="activeTab" :changeTabFunc="changeTab">
        <div v-if="unit">
          <div v-if="activeTab !== 4 && activeTab !== 5 && activeTab !== 3" class="content row">
            <div v-for="(field, key) in filteredFields" :key="key" class="col-md-4 field">
              <zoa-input
                zoa-type="textbox"
                :label="fieldNameCalc(key)"
                v-model="filteredFields[key]"
              />
            </div>
          </div>
          <!-- <div v-if="activeTab == 1" class="content row">
            <div class="col-md-4 field">
              <zoa-input zoa-type="dropdown" label="Section" :options="section_options" />
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Division Name" class="comments-title" />
              <p class="view-field">{{}}</p>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Department Name" class="comments-title" />
              <p class="view-field">{{}}</p>
            </div>
          </div> -->
          <div v-if="activeTab == 3" class="content row">
            <h4 class="subheading">Storage Container</h4>
            <div class="col-md-4 field">
              <zoa-input
                zoa-type="dropdown"
                label="Room Code"
                v-model="unit.container_name"
                :options="{ options: container_options }"
                @change="setCurrentContainer"
              />
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Temperature" class="comments-title" />
              <p class="view-field">
                {{ current_container.temperature }}
              </p>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Relative Humidity" class="comments-title" />
              <p class="view-field">
                {{ current_container.relative_humidity }}
              </p>
            </div>
            <!-- <SelectComp
              :options="['room 1', 'room 2', 'room 3']"
              label="Room Code"
              help=""
              :multi="false"
              :value=""
            /> -->
            <h4 class="subheading">Room Info</h4>
            <div class="col-md-4 field">
              <zoa-input
                zoa-type="dropdown"
                label="Room Code"
                v-model="unit.room_code"
                :options="{ options: room_options }"
                @change="setCurrentRoom"
              />
            </div>
            <div v-for="field in room_fields" :key="field" class="col-md-4 field">
              <zoa-input zoa-type="empty" :label="fieldNameCalc(field)" class="comments-title" />
              <p class="view-field">
                {{ current_room[field] }}
              </p>
            </div>

            <h4 class="subheading">Site Info</h4>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Floor Name" class="comments-title" />
              <p class="view-field">
                {{ current_room.floor_name }}
              </p>
            </div>
            <!-- <div class="col-md-4 field">
              <zoa-input
                zoa-type="textbox"
                label="Floor Name"
                :disabled="true"
                v-model="room_data.filter((room) => room.room_code == unit.room_code)[0].floor_name"
              />
            </div> -->
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Building Name" class="comments-title" />
              <p class="view-field">
                {{ current_room.building_name }}
              </p>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Site Name" class="comments-title" />
              <p class="view-field">
                {{ current_room.site_name }}
              </p>
            </div>
          </div>
          <div v-if="activeTab == 4" class="content row">
            <div v-if="unit_scores.length > 0" class="">
              <RescoreCompV2 :unit="unit_scores[0]" :rescore="false" />
            </div>
            <div v-else class="">no scores</div>
          </div>
          <div v-if="activeTab == 5" class="content row">
            <div class="col-md-6 field">
              <zoa-input zoa-type="empty" label="Unit Comments" class="comments-title" />
              <textarea class="text-area" rows="7" v-model="unit.unit_comment"></textarea>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Date Comment Added" class="comments-title" />
              <p class="view-field">{{ formatDate(unit.date_comment_added) }}</p>
            </div>
          </div>
        </div>
      </TopTabs>
    </div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import TopTabs from '@/components/TopTabs.vue'
import { getGeneric } from '@/services/dataService'
import RescoreCompV2 from '@/components/RescoreCompV2.vue'
import fieldNameCalc from '@/utils/utils'

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
    RescoreCompV2,
  },
  setup() {
    const route = useRoute()

    // Access query parameters
    const unitId = ref(null)
    const collection = ref(null)
    //const section = ref(null)

    onMounted(() => {
      unitId.value = route.query.unit_id
      collection.value = route.query.collection
      //section.value = route.query.section
    })

    return {
      unitId,
      collection,
      //section,
    }
  },
  data() {
    return {
      unit: [],
      unit_scores: [],
      tabs: [
        { id: 0, label: 'Unit Details' },
        { id: 1, label: 'Section' },
        { id: 2, label: 'Properties' },
        { id: 3, label: 'Storage' },
        { id: 4, label: 'Scores' },
        { id: 5, label: 'Comments' },
      ],
      unitTabMapping: [
        {
          tab_id: 0,
          fields: [
            'collection_unit_id',
            'unit_name',
            'public_unit_name',
            'item_type',
            'description',
            //only if lib and arch
            'function_name',
            'unit_active',
            'responsible_curator',
            'archives_fond_ref',
            'bibliographic_level',
            'count_curatorial_units_flag',
            'es_recent_specimen_flag',
            'items_unestimatable_flag',
            'named_collection',
            'preservation_method',
            'publish_flag',
            'sort_order',
            'type_collection_flag',
            'typical_item_count',
            'typical_item_count_range',
          ],
        },
        { tab_id: 1, fields: ['section_id', 'section_name', 'division_name', 'department_name'] },
        {
          tab_id: 2,
          fields: [
            'informal_taxon',
            'geographic_origin_id',
            'geographic_origin_name',
            'region_type',
            'geological_time_period_from_id',
            'from_period',
            'geological_time_period_to_id',
            'to_period',
            'ls_external_ref_name',
            'ls_taxon_name',
            'ls_taxon_rank',
            'pal_external_ref_name',
            'pal_taxon_name',
            'pal_taxon_rank',
          ],
        },
        {
          tab_id: 3,
          fields: [
            'container_name',
            'temperature',
            'relative_humidity',
            'room_name',
            'room_code',
            'floor_name',
            'building_name',
            'site_name',
          ],
        },
        {
          tab_id: 4,
          fields: [],
        },
        {
          tab_id: 5,
          fields: ['unit_comment', 'date_comment_added'],
        },
      ],
      activeTab: 0,
      room_options: [],
      room_data: [],
      current_room: [],
      room_fields: [
        'room_name',
        'circulation',
        'estates_division_code',
        'estates_room_area',
        'estates_room_type',
        'floorplan_area',
        'multi_room_split',
        'storage_footprint',
        'storage_room_id',
        'threshold_rh_max',
        'threshold_rh_min',
        'threshold_temp_max',
        'threshold_temp_min',
        'typical_height',
        'volume',
      ],
      container_options: [],
      current_container: [],
      section_options: [],
      current_section: [],
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    async fetchData() {
      let unitData = await getGeneric(`full-unit/${this.unitId}`)
      this.unit = unitData[0]
      // this.unit_scores = await getGeneric(`unit-scores/${this.unitId}`)
      getGeneric(`unit-scores/${this.unitId}`).then((response) => {
        this.unit_scores = response
      })
      getGeneric(`room-data`).then((response) => {
        this.room_options = response.map((room) => ({
          value: room.room_code,
          storage_room_id: room.storage_room_id,
        }))
        this.room_data = response
        this.setCurrentRoom()
      })
      getGeneric(`container-data`).then((response) => {
        this.container_options = response.map((container) => ({
          ...container,
          value: container.container_name,
        }))
        this.setCurrentContainer()
      })
      getGeneric(`all-sections`).then((response) => {
        this.section_options = response.map((section) => ({
          ...section,
          value: section.section_name,
          label: section.section_name,
        }))
      })
    },
    fieldNameCalc,
    changeTab(index) {
      this.activeTab = index
    },
    formatDate(date) {
      return new Date(date).toISOString().split('T')[0]
    },
    setCurrentRoom() {
      this.current_room = this.room_data.filter((room) => room.room_code == this.unit.room_code)[0]
    },
    setCurrentContainer() {
      console.log(this.current_container)
      this.current_container = this.container_options.filter(
        (container) => container.container_name == this.unit.container_name,
      )[0]
      console.log(this.current_container)
    },
  },
  computed: {
    filteredFields() {
      // Find the tab mapping for the active tab
      const mapping = this.unitTabMapping.find((item) => item.tab_id === this.activeTab)
      // Check if unit and mapping are not null
      if (mapping && this.unit) {
        // Create object for the fields that are in the mapping
        const mappingObj = Object.fromEntries(
          Object.entries(this.unit).filter(([key]) => mapping.fields.includes(key)),
        )
        //Sort by the unitTabMapping
        var sortedFields = {}
        mapping.fields.forEach((key) => {
          if (mappingObj) {
            sortedFields[key] = mappingObj[key]
          }
        })
        // Return the sorted filtered fields
        return sortedFields
      }
      return {}
    },
  },
}
</script>

<style scoped>
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
</style>
