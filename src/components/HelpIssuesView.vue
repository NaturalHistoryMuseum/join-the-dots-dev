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
        <template #cell(date_added)="row">
          {{ new Date(row.item.date_added).toISOString().split('T')[0] }}
        </template>
        <template #cell(completed)="row">
          {{ row.item.completed ? 'Resolved' : 'Open' }}
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
    <div>
      <p>
        Please see below a list of functionality actively being worked on for
        the app.
      </p>
      <b-table
        id="unit-table"
        class="unit-table"
        striped
        hover
        responsive
        :items="enhancements_data"
        :fields="enhancements_fields"
      >
      </b-table>
    </div>
  </AccordionGeneric>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import { getGeneric } from '@/services/dataService';

export default {
  name: 'HelpIssuesView',
  components: { AccordionGeneric, TableCheckbox },
  data() {
    return {
      expanded_accordion: null,
      issues: [],
      issue_fields: [
        { key: 'issue_id', label: 'ID', thStyle: { width: '10%' } },
        { key: 'issue', label: 'Issue', thStyle: { width: '70%' } },
        { key: 'date_added', label: 'Date Added', thStyle: { width: '10%' } },
        { key: 'completed', label: 'Status', thStyle: { width: '10%' } },
      ],
      enhancements_fields: [
        { key: 'ticket_id', label: 'Ticket ID', thStyle: { width: '20%' } },
        {
          key: 'description',
          label: 'Description',
          thStyle: { width: '60%' },
        },
        { key: 'exp_date', label: 'Exp Date', thStyle: { width: '20%' } },
      ],
      enhancements_data: [
        {
          ticket_id: 30,
          description: 'The ability to add Draft units.',
          exp_date: 'Dec 2025',
        },
        { ticket_id: 25, description: 'Data exports', exp_date: 'Dec 2025' },
        {
          ticket_id: 24,
          description: 'Personalised home page statistics / reminders',
          exp_date: 'Jan 2026',
        },
        {
          ticket_id: 74,
          description:
            'See only fields that are relevent to respective division',
          exp_date: 'Jan 2026',
        },
      ],
    };
  },
  created() {
    this.getIssueData();
  },
  methods: {
    async getIssueData() {
      const resp = await getGeneric('all-issues');
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
