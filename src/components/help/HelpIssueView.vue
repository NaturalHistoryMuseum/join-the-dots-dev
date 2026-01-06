<template>
  <AccordionGeneric
    :accordion_open="expanded_accordion === 1"
    accordion_title="Raised Issues"
    :accordion_open_function="toggleAccordion"
    :accordion_eror="false"
    :accordion_id="1"
  >
    <div>
      Please see below the current issues that have been raised.
      <TableCheckbox
        v-if="issues?.length > 0"
        :units="issues"
        :fields="issue_fields"
      >
        <template #cell(status)="row">
          {{
            row.item.status.charAt(0).toUpperCase() + row.item.status.slice(1)
          }}
        </template>
        <template #cell(date_added)="row">
          {{ new Date(row.item.date_added).toISOString().split('T')[0] }}
        </template>
        <template #cell(date_resolved)="row">
          {{
            row.item.date_resolved
              ? new Date(row.item.date_resolved).toISOString().split('T')[0]
              : ''
          }}
        </template>
      </TableCheckbox>
    </div>
  </AccordionGeneric>

  <AccordionGeneric
    :accordion_open="expanded_accordion === 2"
    accordion_title="Upcoming Enhancements"
    :accordion_open_function="toggleAccordion"
    :accordion_eror="false"
    :accordion_id="2"
  >
    <EnhancementsTable />
  </AccordionGeneric>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import { getGeneric } from '@/services/dataService';
import EnhancementsTable from './EnhancementsTable.vue';

export default {
  name: 'HelpIssuesView',
  components: { AccordionGeneric, TableCheckbox, EnhancementsTable },
  data() {
    return {
      expanded_accordion: null,
      issues: [],
      issue_fields: [
        { key: 'issue_id', label: 'ID', thStyle: { width: '5%' } },
        { key: 'issue', label: 'Issue', thStyle: { width: '65%' } },
        { key: 'status', label: 'Status', thStyle: { width: '10%' } },
        { key: 'date_added', label: 'Date Added', thStyle: { width: '10%' } },
        {
          key: 'date_resolved',
          label: 'Date Resolved',
          thStyle: { width: '10%' },
        },
      ],
    };
  },
  created() {
    this.getIssueData();
  },
  methods: {
    async getIssueData() {
      const resp = await getGeneric('visible-issues');
      this.issues = resp;
    },
    toggleAccordion(accordion_id) {
      if (this.expanded_accordion === accordion_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accordion_id;
      }
    },
  },
};
</script>
