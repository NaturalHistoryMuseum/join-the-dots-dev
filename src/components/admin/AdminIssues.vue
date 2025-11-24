<template>
  <OverlayMessage />

  <TableCheckbox
    v-if="issues?.length > 0"
    :units="issues"
    :fields="issue_fields"
  >
    <template #cell(date_added)="row">
      {{ new Date(row.item.date_added).toISOString().split('T')[0] }}
    </template>
    <template #cell(status)="row">
      <zoa-input
        zoa-type="dropdown"
        v-model="row.item.status"
        label-position="none"
        :config="{ options: status_options }"
        @change="markEdited(row.item.issue_id)"
      />
    </template>
    <template #cell(visible)="row">
      <zoa-input
        zoa-type="checkbox"
        v-model="row.item.visible"
        :label="row.item.visible ? 'Yes' : 'No'"
        label-position="right"
        @change="markEdited(row.item.issue_id)"
      />
    </template>
  </TableCheckbox>
  <div v-else class="text-center">
    <p>No issues have been raised</p>
  </div>
</template>

<script>
import { getGeneric, submitDataGeneric } from '@/services/dataService';
import { useMessagesStore } from '@/stores/messages';
import OverlayMessage from '../OverlayMessage.vue';
import TableCheckbox from '../TableCheckbox.vue';
export default {
  name: 'GuidanceView',
  props: {},
  components: { TableCheckbox, OverlayMessage },
  data() {
    return {
      issues: [],
      issue_fields: [
        { key: 'issue_id', label: 'ID', thStyle: { width: '5%' } },
        { key: 'issue', label: 'Issue', thStyle: { width: '55%' } },

        { key: 'status', label: 'Status', thStyle: { width: '10%' } },
        {
          key: 'visible',
          label: 'Visible to Users',
          thStyle: { width: '10%' },
        },
        {
          key: 'date_added_formatted',
          label: 'Date Added',
          thStyle: { width: '10%' },
        },
        {
          key: 'date_resolved_formatted',
          label: 'Date Resolved',
          thStyle: { width: '10%' },
        },
      ],
      status_options: [
        { label: 'Raised', value: 'raised', order: 1 },
        { label: 'In-Progress', value: 'in-progress', order: 2 },
        { label: 'Resolved', value: 'resolved', order: 3 },
      ],
    };
  },
  setup() {
    const store = useMessagesStore();
    return { store };
  },
  mounted() {
    this.getIssueData();
  },
  methods: {
    async getIssueData() {
      const resp = await getGeneric('all-issues');
      this.issues = resp.map((issue) => {
        return {
          ...issue,
          visible: issue.visible === 1 ? true : false,
          date_resolved_formatted: issue.date_resolved
            ? new Date(issue.date_resolved).toISOString().split('T')[0]
            : null,
          date_added_formatted: issue.date_added
            ? new Date(issue.date_added).toISOString().split('T')[0]
            : null,
        };
      });
    },
    async saveChanges(issue) {
      const response = await submitDataGeneric('update-issue', {
        issue_id: issue.issue_id,
        status: issue.status,
        visible: issue.visible ? 1 : 0,
        date_resolved: issue.date_resolved,
      });
      this.store.handleChangeResponse(response);
    },
    markEdited(issue_id) {
      const issue = this.issues.find((i) => i.issue_id === issue_id);
      issue.edited = true;
      this.checkResolved(issue);
    },
    checkResolved(issue) {
      const resolved = issue.status === 'resolved';
      if (resolved && !issue.date_resolved) {
        issue.date_resolved = new Date();
        issue.date_resolved_formatted = new Date().toISOString().split('T')[0];
      } else if (!resolved) {
        issue.date_resolved = null;
        issue.date_resolved_formatted = null;
      }
      this.saveChanges(issue);
    },
  },
  computed: {
    hasEdits() {
      return this.issues.some((i) => i.edited);
    },
  },
};
</script>

<style></style>
