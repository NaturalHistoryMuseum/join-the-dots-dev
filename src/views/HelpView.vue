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
          v-for="(accordion, index) in section.accordions"
          :key="accordion.accordion_id"
        >
          <AccordionGeneric
            :accordion_open="expanded_accordion === index"
            :accordion_title="accordion.header"
            :accordion_open_function="toggleAccordion"
            :accordion_eror="false"
            :accordion_id="index"
          >
            <!-- <div v-if="accordion.content" v-html="accordion.content"></div> -->
            <component v-if="accordion.component" :is="accordion.component" />
            <div
              v-else-if="accordion.rendered_html"
              v-html="rendered_html"
            ></div>
            <div v-else-if="accordion.issues_table">
              Please see below the current issues that have been raised.
              <TableCheckbox
                v-if="issues?.length > 0"
                :units="issues"
                :fields="issue_fields"
              >
                <template #cell(date_added)="row">
                  {{
                    new Date(row.item.date_added).toISOString().split('T')[0]
                  }}
                </template>
                <template #cell(completed)="row">
                  {{ row.item.completed ? 'Resolved' : 'Open' }}
                </template>
              </TableCheckbox>
            </div>
          </AccordionGeneric>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AccordionGeneric from '@/components/AccordionGeneric.vue';
import TableCheckbox from '@/components/TableCheckbox.vue';
import TopTabs from '@/components/TopTabs.vue';
import { getGeneric } from '@/services/dataService';
// import { marked } from 'marked';
export default {
  name: 'HelpView',
  components: { TopTabs, AccordionGeneric, TableCheckbox },
  data() {
    return {
      page_data: [],
      active_tab: 0,
      expanded_accordion: null,
      issues: [],
      issue_fields: [
        // { label: '', key: 'select', class: 'text-center' }, // Checkbox column
        { label: 'Issue ID', key: 'issue_id' },
        { label: 'Issue', key: 'issue' },
        { label: 'Date Raised', key: 'date_added' },
        { label: 'Status', key: 'completed' },
      ],
    };
  },
  created() {
    this.setPageData();
    this.getIssueData();
  },
  methods: {
    async setPageData() {
      const data = await import('../utils/help_page.json');
      this.page_data = data.default;
      this.setAccContent();
    },
    async setAccContent() {
      // Load the markdown files
      // for (const section of this.page_data) {
      //   if (section.accordions) {
      //     for (const acc of section.accordions) {
      //       if (acc.file) {
      //         const md = await import(
      //           `@/assets/help_page/content/${acc.file}`
      //         ).then((r) => r.text());
      //         // Convert Markdown to HTML
      //         acc.content = marked(md);
      //       }
      //     }
      //   }
      const all_components = import.meta.glob(
        '../components/help-content/*.vue',
      );

      this.page_data = await Promise.all(
        this.page_data.map(async (section) => {
          if (section.accordions) {
            section.accordions = await Promise.all(
              section.accordions.map(async (acc) => {
                if (acc.file) {
                  const comp_path = `../components/help-content/${acc.file}`;
                  if (all_components[comp_path]) {
                    const module = await all_components[comp_path]();
                    acc.component = module.default;
                  } else {
                    console.warn(`Component not found: ${comp_path}`);
                  }
                }
                return acc;
              }),
            );
          }
          return section;
        }),
      );
    },
    async getIssueData() {
      const resp = await getGeneric('all-issues');
      this.issues = resp;
    },
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
