<template>
  <div class="main-page">
    <div class="main-header" v-if="page_data.length > 0">
      <p class="h2-style">Help / Info</p>
      <TopTabs
        :tabs="page_data"
        :active_tab="active_tab"
        :changeTabFunc="changeTab"
      />
      <div
        class="tab-content"
        v-for="section in page_data.filter((_, index) => index === active_tab)"
        :key="section.section_id"
      >
        <p v-if="section.section_desc">
          {{ section.section_desc }}
        </p>
        <component
          v-if="section.component"
          :is="section.component"
          :edit_mode="false"
        />
      </div>
    </div>
  </div>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import GuidanceView from '@/components/admin/GuidanceView.vue';
import ChangeLog from '@/components/help/ChangeLog.vue';
import HelpIssuesView from '@/components/help/HelpIssueView.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import TopTabs from '@/components/TopTabs.vue';
export default {
  name: 'HelpView',
  components: { TopTabs, AccordionGeneric, TableCheckbox },
  data() {
    return {
      active_tab: 0,
      expanded_accordion: null,
      issues: [],
      issue_fields: [
        { label: 'Issue ID', key: 'issue_id' },
        { label: 'Issue', key: 'issue' },
        { label: 'Date Raised', key: 'date_added' },
        { label: 'Status', key: 'completed' },
      ],
      page_data: [
        {
          section_id: 0,
          section_name: 'Guidance',
          section_desc:
            'Here you can find useful guidance about using the Join the Dots platform.',
          component: GuidanceView,
        },
        {
          section_id: 1,
          section_name: 'Issues / Enhancements',
          section_desc:
            'Here you can find information on what issues have been reported and what is currently being worked on.',
          component: HelpIssuesView,
        },
        {
          section_id: 1,
          section_name: 'Change Log',
          section_desc:
            'Here you can find information on recent changes and updates to this application.',
          component: ChangeLog,
        },
      ],
    };
  },

  methods: {
    changeTab(index) {
      this.active_tab = index;
      this.expanded_accordion = null;
    },
    toggleAccordion(accord_id) {
      if (this.expanded_accordion === accord_id) {
        this.expanded_accordion = null;
      } else {
        this.expanded_accordion = accord_id;
      }
    },
  },
};
</script>

<style>
.tab-content {
  margin: 1rem;
}
@media (min-width: 1024px) {
}
</style>
