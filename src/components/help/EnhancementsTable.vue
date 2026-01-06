<template>
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
      <template #cell(expected_date)="row">
        {{ new Date(row.item.expected_date).toISOString().split('T')[0] }}
      </template>
    </b-table>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'EnhancementsTable',
  components: {},
  data() {
    return {
      enhancements: [],
      enhancements_fields: [
        {
          key: 'enhancement_id',
          label: 'Enhancement ID',
          thStyle: { width: '20%' },
        },
        {
          key: 'description',
          label: 'Description',
          thStyle: { width: '60%' },
        },
        {
          key: 'expected_date',
          label: 'Expected Date',
          thStyle: { width: '20%' },
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
      this.enhancements = resp;
    },
  },
};
</script>
