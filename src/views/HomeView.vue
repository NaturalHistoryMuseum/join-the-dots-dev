<template>
  <div class="home">
    <div class="home-header">
      <h1>Join the Dots Portal</h1>
      <p>
        Sed dictum tincidunt dolor quis finibus. Donec in tincidunt augue. Curabitur dapibus vel
        mauris nec varius. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
        inceptos himenaeos. Nunc cursus auctor dui, vel cursus nunc cursus a. Aenean eu sem et dui
      </p>
    </div>
  </div>
</template>

<style>
.home {
  /* display: flex; */
  align-items: center;
  padding: 0.5rem 2rem;
}
.home-header {
  margin: 2rem 6rem;
  text-align: left;
}

@media (max-width: 768px) {
  .home {
    padding: 0.5rem 1rem;
  }
  .home-header {
    margin: 2rem 2rem;
  }
}

@media (max-width: 480px) {
  .home {
    padding: 0.5rem 0.5rem;
  }
  .home-header {
    margin: 2rem 1rem;
  }
}
</style>
