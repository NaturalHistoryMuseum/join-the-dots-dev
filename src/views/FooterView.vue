<template>
  <footer class="footer-bar">
    <div class="footer-header">
      <!-- Logo and footer-title -->
      <button @click="navigateHome" class="icon-container">
        <img
          alt="NHM logo"
          class="footer-logo"
          src="@/assets/nhm_white_logo.png"
        />
      </button>
      <div class="footer-title">
        <p>
          This is a development/testing environment, no data changes will affect
          JtD data.
        </p>
        <p>
          If you have any issues please reach out to: andrew.roberts@nhm.ac.uk
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterView',
};
</script>

<style>
.footer-bar {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  align-items: flex-end;
  padding: 2rem 2rem;
  /* margin-top: 3rem; */
  bottom: 0;
  /* position: fixed; */
  width: 100%;
  background-color: var(--secondary-col);
}

footer {
  line-height: 1.5;
  max-height: 100vh;
}

.footer-header {
  display: flex;
  width: 100%;
}

.nav-footer {
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  gap: 3rem;
  width: 100%;
}

.account-footer {
  display: flex;
  align-items: flex-start;
  justify-self: flex-end;
  margin-left: auto;
  gap: 3rem;
}

.footer-logo {
  height: 3.5rem;
  justify-self: flex-start;
}
.footer-title {
  align-self: center;
  color: white;
  margin: 0;
  margin-left: 3rem;
  /* font-size: 2.5rem; */
}

.icon-container {
  background-color: transparent;
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  margin: 0;
  display: flex;
  align-items: start;
}

@media (max-width: 768px) {
  .footer-bar {
    padding: 0.5rem 1rem;
    padding-bottom: 1rem;
  }
  .nav-footer {
    gap: 1rem;
  }
  .footer-logo {
    height: 2rem;
  }
  .footer-title {
    /* font-size: 1.8rem; */
    margin-left: 2rem;
  }
}
@media (max-width: 480px) {
  .footer-bar {
    padding: 0.5rem 1rem;
    padding-bottom: 0.7rem;
  }
  .footer-logo {
    height: 2rem;
  }
  .footer-title {
    /* font-size: 1.2rem; */
    margin-left: 1.5rem;
  }
}
</style>
