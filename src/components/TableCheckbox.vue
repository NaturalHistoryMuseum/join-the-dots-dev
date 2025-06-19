<template>
  <div v-if="selected_unit_ids.length > 0" class="selected-units">
    <slot></slot>
  </div>
  <b-table
    id="unit-table"
    class="unit-table"
    striped
    hover
    responsive
    :items="units"
    :fields="fields"
  >
    <!-- Header checkbox for selecting all rows -->
    <template #head(select)="">
      <zoa-input
        class="check"
        zoa-type="checkbox"
        label=""
        label-position="right"
        v-model="selectAll"
        @change="(newValue) => toggleSelectAll(newValue)"
      />
    </template>

    <!-- Row checkbox -->
    <template #cell(select)="row">
      <zoa-input
        class="check"
        zoa-type="checkbox"
        label-position="none"
        @change="(newValue) => handleCheckboxChange(newValue, row.item)"
        v-model="row.item.selected"
      />
    </template>

    <!-- Forward slot if custom slot exists, fallback to default - exclude the checkbox column -->
    <template
      v-for="field in fields.filter((col) => col.key != 'select')"
      v-slot:[`cell(${field.key})`]="row"
    >
      <template v-if="$slots[`cell(${field.key})`]">
        <slot :name="`cell(${field.key})`" v-bind="row"></slot>
      </template>
      <template v-else>
        {{ row.value }}
      </template>
    </template>
  </b-table>
</template>

<script>
export default {
  name: 'TableCheckbox',
  props: {
    units: Array,
    fields: Array,
  },
  data() {
    return {
      selected_unit_ids: [], // Array to hold selected unit IDs
    };
  },
  methods: {
    toggleSelectAll(newValue) {
      // Only update currently visible (filtered + paginated) rows
      this.units.forEach((unit) => {
        unit.selected = newValue;
      });
      this.updateSelectedUnits();
    },
    updateSelectedUnits() {
      this.selected_unit_ids = this.units
        .filter((unit) => unit.selected)
        .map((unit) => unit.collection_unit_id);
    },
    handleCheckboxChange(newValue, rowItem) {
      // Update the selected property directly
      rowItem.selected = newValue;

      if (newValue) {
        //Add the item to the selected_unit_ids array
        this.selected_unit_ids.push(rowItem.collection_unit_id);
      } else {
        //Remove the item from the selected_unit_ids array
        const indexOfVal = this.selected_unit_ids.indexOf(
          rowItem.collection_unit_id,
        );
        this.selected_unit_ids.splice(indexOfVal, 1);
      }
    },
    // Reset selection state for all units
    resetSelection() {
      this.units.forEach((unit) => {
        unit.selected = false;
      });
      this.updateSelectedUnits();
    },
  },
  computed: {
    // Handle the select all checkbox
    selectAll: {
      get() {
        return (
          this.units.length > 0 && this.units.every((unit) => unit.selected)
        );
      },
      set(newValue) {
        this.toggleSelectAll(newValue);
      },
    },
  },
};
</script>
