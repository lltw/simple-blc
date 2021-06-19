<template>

  <div class="container">
    <div class="row">
      <div class="col gy-5">
        <div class="p-3 border bg-light">
          <h1 class="display-5">Simple Benford's Law Checker</h1>
        </div>
      </div>
    </div>

    <div class="row align-items-start">

      <div class="col-sm-12 col-xl-4 gy-4">
        <div class="p-3 border bg-light">
          <UserFileUpload2 />
        </div>
      </div>

      <div class="col-sm-12 col-xl-8 gy-4">
        <div class="p-3 border bg-light ">
          <ResultsChiSquaredTest />
        </div>

        <div>
          <p></p>
        </div>

        <div class="p-3 border bg-light ">
          <ResultsPlotTest />
        </div>
      </div>

    </div>
  </div>

</template>

<script>
import UserFileUpload2 from './components/UserFileUpload2.vue';
import ResultsChiSquaredTest from './components/ResultsChiSquaredTest.vue';
import ResultsPlotTest from './components/ResultsPlotTest.vue';

export default {
  name: 'App',
  components: {
    UserFileUpload2,
    ResultsChiSquaredTest,
    ResultsPlotTest
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>


