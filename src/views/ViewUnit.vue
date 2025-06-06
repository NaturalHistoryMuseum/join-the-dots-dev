<template>
  <div class="main-page">
    <div class="main-header">
      <h1>View Unit</h1>
      <p>Unit ID: {{ unitId }}</p>
      <TopTabs :tabs="tabs" :active_tab="active_tab" :changeTabFunc="changeTab">
        <div v-if="unit">
          <!-- <div
            v-if="
              active_tab !== 4 &&
              active_tab !== 5 &&
              active_tab !== 3 &&
              active_tab !== 1 &&
              active_tab !== 2
            "
            class="content row"
          >
            <div v-for="(field, key) in filteredFields" :key="key" class="col-md-4 field">
              <zoa-input
                zoa-type="textbox"
                :label="fieldNameCalc(key)"
                v-model="filteredFields[key]"
              />
            </div>
          </div> -->
          <!-- Unit Details -->
          <div v-if="active_tab == 0" class="content row">
            <div class="row">
              <h4 class="subheading">Unit Details</h4>
              <div class="col-md-4 field">
                <zoa-input zoa-type="textbox" label="Unit Name" v-model="unit.unit_name" />
              </div>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="textbox"
                  label="Public Unit Name"
                  v-model="unit.public_unit_name"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="textbox"
                  label="Named Collection"
                  v-model="unit.named_collection"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="textbox"
                  label="Archives Fond Ref"
                  v-model="unit.archives_fond_ref"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="number" label="Sort Order" v-model="unit.sort_order" />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Unit Active?" class="comments-title" />
                <zoa-input
                  zoa-type="checkbox"
                  :label="
                    unit.unit_active != null
                      ? unit.unit_active.charAt(0).toUpperCase() + unit.unit_active.slice(1)
                      : 'No'
                  "
                  label-position="right"
                  v-model="unitIsActive"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Publish Unit?" class="comments-title" />
                <zoa-input
                  zoa-type="checkbox"
                  :label="
                    unit.publish_flag != null
                      ? unit.publish_flag.charAt(0).toUpperCase() + unit.publish_flag.slice(1)
                      : 'No'
                  "
                  label-position="right"
                  v-model="publishFlag"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Type Collection?" class="comments-title" />
                <zoa-input
                  zoa-type="checkbox"
                  :label="
                    unit.type_collection_flag != null
                      ? unit.type_collection_flag.charAt(0).toUpperCase() +
                        unit.type_collection_flag.slice(1)
                      : 'No'
                  "
                  label-position="right"
                  v-model="typeCollectionFlag"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="ES Recent Specimen?" class="comments-title" />
                <zoa-input
                  zoa-type="checkbox"
                  :label="
                    unit.es_recent_specimen_flag != null
                      ? unit.es_recent_specimen_flag.charAt(0).toUpperCase() +
                        unit.es_recent_specimen_flag.slice(1)
                      : 'No'
                  "
                  label-position="right"
                  v-model="recentSpecimenFlag"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="empty"
                  label="Count Curatorial Units?"
                  class="comments-title"
                />
                <zoa-input
                  zoa-type="checkbox"
                  :label="
                    unit.count_curatorial_units_flag != null
                      ? unit.count_curatorial_units_flag.charAt(0).toUpperCase() +
                        unit.count_curatorial_units_flag.slice(1)
                      : 'No'
                  "
                  label-position="right"
                  v-model="countCuratorialUnitsFlag"
                />
              </div>
            </div>

            <div class="row">
              <h4 class="subheading">Responsible Curator</h4>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Curator Name" class="comments-title" />
                <p class="view-field">{{ unit.responsible_curator }}</p>
              </div>
            </div>
            <div class="row">
              <h4 class="subheading">Curtorial Unit Definition</h4>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="dropdown"
                  label="Curatorial Unit Definition"
                  :config="{ options: curatorial_def_options }"
                  v-model="unit.curatorial_unit_definition_id"
                  @change="setCurrentCuratorialDef"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Item Type" class="comments-title" />
                <p class="view-field">{{ current_curatorial_def.item_type }}</p>
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Bibliographic Level" class="comments-title" />
                <p class="view-field">{{ current_curatorial_def.bibliographic_level }}</p>
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Preservation Method" class="comments-title" />
                <p class="view-field">{{ current_curatorial_def.preservation_method }}</p>
              </div>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="empty"
                  label="Items Unestimatable Flag"
                  class="comments-title"
                />
                <p class="view-field">{{ current_curatorial_def.items_unestimatable_flag }}</p>
              </div>
            </div>
            <div v-if="current_section.department_id == 2" class="row">
              <h4 class="subheading">Library and Archives Function</h4>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="dropdown"
                  label="Library and Archives Function"
                  :config="{ options: lib_function_options }"
                  v-model="unit.library_and_archives_function_id"
                  @change="setCurrentLibFunction"
                />
              </div>
            </div>
          </div>
          <!-- Section -->
          <div v-if="active_tab == 1" class="content row">
            <div class="col-md-4 field">
              <zoa-input
                zoa-type="dropdown"
                label="Section Name"
                :config="{ options: section_options }"
                v-model="unit.section_id"
                @change="setCurrentSection"
              />
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Division Name" class="comments-title" />
              <p class="view-field">{{ current_section.division_name }}</p>
            </div>
            <div class="col-md-4 field">
              <zoa-input zoa-type="empty" label="Department Name" class="comments-title" />
              <p class="view-field">{{ current_section.department_name }}</p>
            </div>
          </div>
          <!-- Properties -->
          <div v-if="active_tab == 2" class="content row">
            <!-- Time Period From -->
            <!-- <div class="row">
              <h4 class="subheading">Time Period From</h4>
              <div class="col-md-4 field">
                <zoa-input
                  zoa-type="dropdown"
                  label="Geological Time Period From"
                  :config="{ options: geological_time_period_options }"
                  v-model="unit.geological_time_period_from_id"
                  @change="setTimeFrom"
                />
              </div>
              <div class="col-md-4 field">
                <zoa-input zoa-type="empty" label="Time From Rank" class="comments-title" />
                <p class="view-field">{{ current_time_from.rank }}</p>
              </div>
            </div> -->
            <!-- Time Period To -->
            <div class="row">
              <div class="col-md-6">
                <div class="row">
                  <h4 class="subheading">Time Period To</h4>
                  <div class="col-md-6 field">
                    <zoa-input
                      zoa-type="dropdown"
                      label="Geological Time Period To"
                      :config="{ options: geological_time_period_options }"
                      v-model="unit.geological_time_period_to_id"
                      @change="setTimeTo"
                    />
                  </div>
                  <div class="col-md-6 field">
                    <zoa-input zoa-type="empty" label="Time To Rank" class="comments-title" />
                    <p class="view-field">{{ current_time_to.rank }}</p>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="row">
                  <h4 class="subheading">Time Period From</h4>
                  <div class="col-md-6 field">
                    <zoa-input
                      zoa-type="dropdown"
                      label="Geological Time Period From"
                      :config="{ options: geological_time_period_options }"
                      v-model="unit.geological_time_period_from_id"
                      @change="setTimeFrom"
                    />
                  </div>
                  <div class="col-md-6 field">
                    <zoa-input zoa-type="empty" label="Time From Rank" class="comments-title" />
                    <p class="view-field">{{ current_time_from.rank }}</p>
                  </div>
                </div>
              </div>
            </div>
            <div class="row">
              <h4 class="subheading">Geographic Origin</h4>
              <div class="col-md-3 field">
                <zoa-input
                  zoa-type="dropdown"
                  label="Geographic Origin Name"
                  :config="{ options: geographic_origin_options }"
                  v-model="unit.geographic_origin_id"
                  @change="setCurrentGeographicOrigin"
                />
              </div>
              <div class="col-md-3 field">
                <zoa-input zoa-type="empty" label="Region Type" class="comments-title" />
                <p class="view-field">{{ current_geographic_origin.region_type }}</p>
              </div>
            </div>
            <!-- Taxon -->
            <div class="row">
              <h4 class="subheading">Taxon</h4>
              <div class="col-md-3 field">
                <zoa-input zoa-type="textbox" label="Informal Taxon" v-model="unit.infomal_taxon" />
              </div>
              <div class="col-md-3 field">
                <zoa-input
                  zoa-type="dropdown"
                  label="Taxon Name"
                  :config="{ options: taxon_options }"
                  v-model="unit.taxon_id"
                  @change="setCurrentTaxon"
                />
              </div>
              <div class="col-md-3 field">
                <zoa-input zoa-type="empty" label="Taxon Rank" class="comments-title" />
                <p class="view-field">
                  {{ current_taxon.taxon_rank }}
                </p>
              </div>
              <div class="col-md-3 field">
                <zoa-input zoa-type="empty" label="External Ref Name" class="comments-title" />
                <p class="view-field">{{ current_taxon.external_ref_name }}</p>
              </div>
              <div class="col-md-3 field">
                <zoa-input zoa-type="empty" label="External Ref Id" class="comments-title" />
                <p class="view-field">{{ current_taxon.external_ref_id }}</p>
              </div>
            </div>
          </div>
          <!-- Storage -->
          <div v-if="active_tab == 3" class="content row">
            <h4 class="subheading">Storage Container</h4>
            <div class="col-md-4 field">
              <zoa-input
                zoa-type="dropdown"
                label="Storage Container"
                v-model="unit.storage_container_id"
                :config="{ options: container_options }"
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
            <h4 class="subheading">Room Info</h4>
            <div class="col-md-4 field">
              <zoa-input
                zoa-type="dropdown"
                label="Room Code"
                v-model="unit.storage_room_id"
                :config="{ options: room_options }"
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
          <!-- Scores -->
          <div v-if="active_tab == 4" class="content row">
            <div v-if="unit_scores.length > 0" class="">
              <UnitScores :unit="unit_scores[0]" :rescore="false" />
            </div>
            <div v-else class="content row centered">No scores recorded for this unit</div>
          </div>
          <!-- Comments -->
          <div v-if="active_tab == 5" class="content row">
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
import UnitScores from '@/components/UnitScores.vue'
import fieldNameCalc from '@/utils/utils'

export default {
  name: 'ViewUnit',
  components: {
    TopTabs,
    UnitScores,
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
      unit_tab_mapping: [
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
      active_tab: 0,
      room_options: [],
      room_data: [],
      current_room: {},
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
      current_container: {},
      section_options: [],
      current_section: {},
      geographic_origin_options: [],
      geological_time_period_options: [],
      current_geographic_origin: {},
      current_time_from: {},
      current_time_to: {},
      taxon_options: [],
      taxon_all_options: [],
      current_taxon: {
        value: null,
        taxon_name: null,
        taxon_rank: '',
        external_ref_name: null,
        external_ref_id: null,
      },
      curatorial_def_options: [],
      current_curatorial_def: {},
      lib_function_options: [],
      current_lib_function: {},
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
        this.unit_scores = response.map((unit) => {
          // Parse category tracking JSON
          unit.ranks_json = JSON.parse(unit.ranks_json)
          unit.metric_json = JSON.parse(unit.metric_json)
          return unit
        })
      })
      getGeneric(`room-data`).then((response) => {
        this.room_options = response.map((room) => ({
          ...room,
          value: room.storage_room_id,
          label: room.room_code,
        }))
        this.room_data = response
        this.setCurrentRoom()
      })
      getGeneric(`container-data`).then((response) => {
        this.container_options = response.map((container) => ({
          ...container,
          value: container.storage_container_id,
          label: container.container_name,
        }))
        this.setCurrentContainer()
      })
      getGeneric(`all-sections`).then((response) => {
        this.section_options = response.map((section) => ({
          ...section,
          label: section.section_name,
          value: section.section_id,
        }))
        this.setCurrentSection()
      })
      getGeneric(`all-geographic-origin`).then((response) => {
        this.geographic_origin_options = response.map((geographic_origin) => ({
          ...geographic_origin,
          label: geographic_origin.geographic_origin_name,
          value: geographic_origin.geographic_origin_id,
        }))
        this.setCurrentGeographicOrigin()
      })
      getGeneric(`all-geological-time-period`).then((response) => {
        this.geological_time_period_options = response.map((geological_time_period) => ({
          ...geological_time_period,
          value: geological_time_period.geological_time_period_id,
          label: geological_time_period.period_name,
        }))
        this.setTimeFrom()
        this.setTimeTo()
      })
      getGeneric(`all-taxon`).then((response) => {
        this.taxon_all_options = response.map((taxon) => ({
          ...taxon,
          value: taxon.taxon_id,
          label: `${taxon.taxon_name} (${taxon.taxon_rank})`,
        }))
        this.setCurrentTaxon()
        this.filterTaxonOptions()
      })
      getGeneric(`all-curtorial-definition`).then((response) => {
        this.curatorial_def_options = response.map((curatorial_def) => ({
          ...curatorial_def,
          value: curatorial_def.curatorial_unit_definition_id,
          label: curatorial_def.description,
        }))
        this.setCurrentCuratorialDef()
      })
      getGeneric(`all-lib-function`).then((response) => {
        this.lib_function_options = response.map((lib_function) => ({
          ...lib_function,
          value: lib_function.library_and_archives_function_id,
          label: lib_function.function_name,
        }))
        this.setCurrentLibFunction()
      })
    },
    fieldNameCalc,
    changeTab(index) {
      this.active_tab = index
    },
    formatDate(date) {
      return new Date(date).toISOString().split('T')[0]
    },
    setCurrentRoom() {
      this.current_room = this.room_data.filter(
        (room) => room.storage_room_id == this.unit.storage_room_id,
      )[0]
    },
    setCurrentContainer() {
      if (this.unit.storage_container_id == null) {
        this.current_container = {
          value: null,
          container_name: null,
          temperature: null,
          relative_humidity: null,
        }
      } else {
        this.current_container = this.container_options.filter(
          (container) => container.storage_container_id == this.unit.storage_container_id,
        )[0]
      }
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
      this.filterTaxonOptions()
    },
    setCurrentGeographicOrigin() {
      if (this.unit.geographic_origin_id == null) {
        this.current_geographic_origin = {
          value: null,
          geographic_origin_name: null,
          region_type: null,
        }
      } else {
        this.current_geographic_origin = this.geographic_origin_options.filter(
          (geographic_origin) =>
            geographic_origin.geographic_origin_id == this.unit.geographic_origin_id,
        )[0]
      }
    },
    setTimeFrom() {
      if (this.unit.geological_time_period_from_id == null) {
        this.current_time_from = {
          value: null,
          geological_time_period_from_id: null,
          period_name: null,
        }
      } else {
        this.current_time_from = this.geological_time_period_options.filter(
          (geological_time_period) =>
            geological_time_period.geological_time_period_id ==
            this.unit.geological_time_period_from_id,
        )[0]
      }
    },
    setTimeTo() {
      if (this.unit.geological_time_period_to_id == null) {
        this.current_time_to = {
          value: null,
          geological_time_period_to_id: null,
          period_name: null,
        }
      } else {
        this.current_time_to = this.geological_time_period_options.filter(
          (geological_time_period) =>
            geological_time_period.geological_time_period_id ==
            this.unit.geological_time_period_to_id,
        )[0]
      }
    },
    setCurrentTaxon() {
      if (this.unit.taxon_id == null) {
        this.current_taxon = {
          value: null,
          taxon_name: null,
          taxon_rank: null,
          external_ref_name: null,
          external_ref_id: null,
        }
      } else {
        this.current_taxon = this.taxon_all_options.filter(
          (taxon) => taxon.taxon_id == this.unit.taxon_id,
        )[0]
      }
    },
    filterTaxonOptions() {
      this.taxon_options = this.taxon_all_options.filter(
        (taxon) => taxon.department_id == this.current_section.department_id,
      )
    },
    setCurrentCuratorialDef() {
      if (this.unit.curatorial_unit_definition_id == null) {
        this.current_curatorial_def = {
          value: null,
          curatorial_definition_name: null,
        }
      } else {
        this.current_curatorial_def = this.curatorial_def_options.filter(
          (curatorial_def) =>
            curatorial_def.curatorial_unit_definition_id == this.unit.curatorial_unit_definition_id,
        )[0]
      }
    },
    setCurrentLibFunction() {
      if (this.unit.library_and_archives_function_id == null) {
        this.current_lib_function = {
          value: null,
          lib_function_name: null,
        }
      } else {
        this.current_lib_function = this.lib_function_options.filter(
          (lib_function) =>
            lib_function.library_and_archives_function_id ==
            this.unit.library_and_archives_function_id,
        )[0]
      }
    },
  },
  computed: {
    filteredFields() {
      // Find the tab mapping for the active tab
      const mapping = this.unit_tab_mapping.find((item) => item.tab_id === this.active_tab)
      // Check if unit and mapping are not null
      if (mapping && this.unit) {
        // Create object for the fields that are in the mapping
        const mappingObj = Object.fromEntries(
          Object.entries(this.unit).filter(([key]) => mapping.fields.includes(key)),
        )
        //Sort by the unit_tab_mapping
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
    unitIsActive: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.unit_active === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit.unit_active = val ? 'yes' : 'no'
        }
      },
    },
    publishFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.publish_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit.publish_flag = val ? 'yes' : 'no'
        }
      },
    },
    typeCollectionFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.type_collection_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit.type_collection_flag = val ? 'yes' : 'no'
        }
      },
    },
    recentSpecimenFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.es_recent_specimen_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit.es_recent_specimen_flag = val ? 'yes' : 'no'
        }
      },
    },
    countCuratorialUnitsFlag: {
      get() {
        // Map 'yes' to true, anything else (including 'no') to false
        return this.unit?.count_curatorial_units_flag === 'yes'
      },
      set(val) {
        // Map true/false back to 'yes'/'no'
        if (this.unit) {
          this.unit.count_curatorial_units_flag = val ? 'yes' : 'no'
        }
      },
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

.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
</style>
