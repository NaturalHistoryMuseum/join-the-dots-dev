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
        <div
          v-for="accordion in section.accordions"
          :key="accordion.accordion_id"
        >
          <AccordionGeneric
            :accordion_open="expanded_accordion === accordion.accordion_id"
            :accordion_title="accordion.header"
            :accordion_open_function="toggleAccordion"
            :accordion_eror="false"
            :accordion_id="accordion.accordion_id"
          >
            <div v-if="accordion.content" v-html="accordion.content"></div>
          </AccordionGeneric>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import TopTabs from '@/components/TopTabs.vue';
import { marked } from 'marked';

export default {
  name: 'HelpView',
  components: { TopTabs, AccordionGeneric },
  data() {
    return {
      page_data: [],
      active_tab: 0,
      expanded_accordion: 0,
    };
  },
  created() {
    this.setPageData();
  },
  methods: {
    async setPageData() {
      const data = await import('../utils/help_page.json');
      this.page_data = data.default;
      this.setAccContent();
    },
    async setAccContent() {
      // Load the markdown files
      for (const section of this.page_data) {
        if (section.accordions) {
          for (const acc of section.accordions) {
            if (acc.file) {
              const md = await fetch(
                `../../public/help_page/content/${acc.file}`,
              ).then((r) => r.text());
              // Convert Markdown to HTML
              acc.content = marked(md);
            }
          }
        }
      }
    },
    changeTab(index) {
      this.active_tab = index;
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
