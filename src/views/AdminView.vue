<template>
  <div class="main-page">
    <div class="main-header">
      <p class="h1-style">Admin</p>
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
import GuidanceView from '@/components/admin/GuidanceView.vue';

export default {
  name: 'AdminView',
  components: { TopTabs, RichEditor },
  data() {
    return {
      page_data: [
        {
          section_id: 1,
          section_name: 'Edit Guidance',
          component: GuidanceView,
        },
        {
          section_id: 0,
          section_name: 'Permissions',
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
