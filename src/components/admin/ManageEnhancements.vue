<template>
  <EditEnhancementModal
    :getEnhancements="getEnhancements"
    :set_enhancement="new_enhancement"
    :add_mode="true"
  />

  <div>
    <p>
      Please see below a list of functionality actively being worked on for the
      app.
    </p>
    <b-table
      id="unit-table"
      class="unit-table"
      striped
      hover
      responsive
      :items="enhancements"
      :fields="enhancements_fields"
    >
      <template #cell(edit_unit)="row">
        <EditEnhancementModal
          :getEnhancements="getEnhancements"
          :set_enhancement="row.item"
          :add_mode="false"
      /></template>
    </b-table>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';
import EditEnhancementModal from '../modals/EditEnhancementModal.vue';

export default {
  name: 'ManageEnhancements',
  components: { EditEnhancementModal },
  data() {
    return {
      enhancements: [],
      new_enhancement: {
        enhancements_id: 0,
        description: '',
        expected_date: '',
      },
      enhancements_fields: [
        {
          key: 'enhancement_id',
          label: 'Enhancement ID',
          thStyle: { width: '10%' },
        },
        {
          key: 'description',
          label: 'Description',
          thStyle: { width: '60%' },
        },
        {
          key: 'expected_date',
          label: 'Expected Date',
          thStyle: { width: '15%' },
        },
        {
          key: 'edit_unit',
          label: '',
          thStyle: { width: '15%' },
        },
      ],
    };
  },
  created() {
    this.getEnhancements();
  },
  methods: {
    async getEnhancements() {
      const resp = await getGeneric('enhancements');
      this.enhancements = resp.map((enhancement) => ({
        ...enhancement,
        expected_date: new Date(enhancement.expected_date)
          .toISOString()
          .split('T')[0],
      }));
    },
  },
};
</script>
