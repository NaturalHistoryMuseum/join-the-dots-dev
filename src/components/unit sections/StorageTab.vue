<template>
  <h4 class="subheading">Storage Container</h4>
  <div class="col-md-4 field">
    <zoa-input
      zoa-type="dropdown"
      label="Storage Container"
      v-model="unit_value.storage_container_id"
      :config="{ options: container_options }"
      @change="
        () => {
          setCurrentContainer()
          handleFieldChange('storage_container_id', unit_value.storage_container_id)
        }
      "
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
      v-model="unit_value.storage_room_id"
      :config="{ options: room_options }"
      @change="
        () => {
          setCurrentRoom()
          handleFieldChange('storage_room_id', unit_value.storage_room_id)
        }
      "
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
</template>

<script>
import { getGeneric } from '@/services/dataService'
import fieldNameCalc from '@/utils/utils'

export default {
  name: 'StorageTab',
  props: {
    unit: Object,
    handleFieldChange: Function,
  },
  data() {
    return {
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
      current_room: {},
      room_options: [],
      room_data: [],
      container_options: [],
      current_container: {},
    }
  },
  computed: {
    unit_value: {
      get() {
        return this.unit
      },
      set(value) {
        this.$emit('updateUnit', value)
      },
    },
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    fieldNameCalc,

    async fetchData() {
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
    setCurrentRoom() {
      this.current_room = this.room_data.filter(
        (room) => room.storage_room_id == this.unit.storage_room_id,
      )[0]
    },
  },
}
</script>

<style></style>
