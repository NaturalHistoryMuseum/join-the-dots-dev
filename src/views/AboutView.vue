<!-- <script s>
// import { RouterLink, RouterView } from 'vue-router'
</script> -->

<script>
// import axios from 'axios'

// export default {
//   data() {
//     return {
//       data: [],
//     }
//   },
//   mounted() {
//     axios
//       .get('http://localhost:5000/api/data/category')
//       .then((response) => {
//         this.data = response.data
//         console.log(this.data)
//       })
//       .catch((error) => {
//         console.error('There was an error fetching the data!', error)
//       })
//   },
// }
</script>

<template>
  <!-- <div class="sub-header-bar"> -->
  <!-- <nav>
      <RouterLink to="/about">Intro</RouterLink>
      <RouterLink to="/about">About</RouterLink>
      <RouterLink to="/about">User Guide</RouterLink>
    </nav> -->
  <!-- </div> -->
  <div class="main-page">
    <div class="main-header">
      <h2>What is Join the Dots?</h2>
      <p>
        Join the Dots (JTD) is a cross–disciplinary collections assessment framework. It is based on
        a methodology called ‘Move the Dots’, which was developed by the Smithsonian National Museum
        of Natural History in 2009. Join the Dots quantifies collections and captures information
        across 4 assessment categories: Condition, Importance, Information, and Outreach. These
        categories are divided into 17 more detailed criteria.
      </p>
      <h2>Why has Join the Dots been implemented?</h2>
      <p>
        The Natural History Museum has a responsibility to provide the best possible care and access
        to its collections. The development and implementation of new collection management systems
        and methodologies is integral to this ongoing duty of care. The NHM strategy crosses
        disciplines, and integrates research agendas with public engagement outputs. Capturing the
        state of collections items is necessary for effective resource planning across the Museum.
        The design of Join the Dots reflects the often holistic nature of curation and collections
        planning, particularly at large museums, whilst setting standards and measuring improvements
        where possible.
      </p>
      <h2>Join the Dots - User Mannual</h2>
      <!-- Embed in future -->
      <p>
        <a
          href="https://naturalhistorymuseum.sharepoint.com/sites/Intranet/Projects/digital/join-the-dots/Shared%20Documents/Join%20the%20Dots%20User%20Manual.pdf"
          target="_blank"
          >User Manual</a
        >
      </p>
      <h2>Cabinet Scoring Document</h2>
      <p>
        <a
          href="https://naturalhistorymuseum.sharepoint.com/sites/Intranet/Projects/digital/join-the-dots/Shared%20Documents/Cabinetry%20Scoring%20Document.pdf"
          target="_blank"
          >Scoring Doc</a
        >
      </p>
    </div>
  </div>
</template>

<style>
.about-header {
  margin: 2rem 10rem;
  text-align: left;
}
.sub-header-bar {
  /* top: 0; */
  height: 3rem;
  background-color: var(--secondary-col);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 2rem;
}

@media (min-width: 1024px) {
}
</style>
