<template>
  <div class="main-page">
    <div class="main-header">
      <h1 class="h1-style">Admin</h1>
      <TopTabs
        :tabs="page_data.sort((a, b) => a.section_id - b.section_id)"
        :active_tab="active_tab"
        :changeTabFunc="changeTab"
      />
      <div
        class="tab-content"
        v-for="section in page_data.filter((_, index) => index === active_tab)"
        :key="section.section_id"
      >
        <component
          v-if="section.component"
          :is="section.component"
          :edit_mode="true"
        />
      </div>
    </div>
  </div>
</template>

<script>
import RichEditor from '@/components/RichEditor.vue';
import TopTabs from '@/components/TopTabs.vue';
import AdminIssues from '@/components/admin/AdminIssues.vue';
import AdminPermissions from '@/components/admin/AdminPermissions.vue';
import GuidanceView from '@/components/admin/GuidanceView.vue';

export default {
  name: 'AdminView',
  components: { TopTabs, RichEditor },
  data() {
    return {
      page_data: [
        {
          section_id: 0,
          section_name: 'User Permissions',
          component: AdminPermissions,
        },
        {
          section_id: 1,
          section_name: 'Edit Guidance',
          component: GuidanceView,
        },
        {
          section_id: 2,
          section_name: 'Manage Issues',
          component: AdminIssues,
        },
      ],
      active_tab: 0,
    };
  },
  setup() {},
  methods: {
    changeTab(new_tab) {
      this.active_tab = new_tab;
    },
  },
};
</script>

<style scoped></style>
