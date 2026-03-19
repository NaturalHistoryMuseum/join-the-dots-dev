<template>
  <div>
    <p>Please see below a list of open rescore sessions.</p>
    <b-table
      id="unit-table"
      class="unit-table"
      striped
      hover
      responsive
      :items="rescores"
      :fields="rescore_fields"
    >
      <template #cell(edit_rescore)="row">
        <zoa-button label="Edit Rescore" @click="navRescore(row.item)" />
      </template>
    </b-table>
  </div>
</template>

<script>
import { getGeneric } from '@/services/dataService';

export default {
  name: 'ManageRescores',
  components: {},
  data() {
    return {
      rescores: [],
      rescore_fields: [
        {
          key: 'rescore_session_id',
          label: 'Rescore ID',
          thStyle: { width: '20%' },
        },
        {
          key: 'curator_name',
          label: 'Curator',
          thStyle: { width: '20%' },
        },
        {
          key: 'unit_count',
          label: 'Number of units',
          thStyle: { width: '20%' },
        },
        {
          key: 'created_at',
          label: 'Rescore Started',
          thStyle: { width: '20%' },
        },
        {
          key: 'edit_rescore',
          label: '',
          thStyle: { width: '20%' },
        },
      ],
    };
  },
  created() {
    this.getRescores();
  },
  methods: {
    async getRescores() {
      const resp = await getGeneric('all-open-rescores');
      this.rescores = resp.map((rescore) => ({
        ...rescore,
        created_at: new Date(rescore.created_at).toISOString().split('T')[0],
      }));
    },
    navRescore(rescore) {
      this.$router.push({
        path: '/rescore',
        query: {
          rescore_session_id: rescore.rescore_session_id,
        },
      });
    },
  },
};
</script>
