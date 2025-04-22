<template>
  <div class="main-header">
    <h1>Manage Rescore</h1>
    <h5>Last Rescore:</h5>
    <p>05/04/25</p>
  </div>
  <div class="">
    <zoa-input zoa-type="textbox" label="Section to rescore (temp)" v-model="sectionId" />
    <zoa-button label="Start Rescore" @click="navigateRescore()" />
  </div>
</template>

<script>
export default {
  name: 'ManageRescoreView',
  components: {},
  setup() {},
  data() {
    return { sectionId: 1 }
  },
  mounted() {},
  methods: {
    navigateRescore() {
      this.$router.push({
        name: 'rescore',
        query: {
          sectionId: this.sectionId,
        },
      })
    },
  },
}
</script>

<style></style>
