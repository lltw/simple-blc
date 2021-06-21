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
          <UserFileUpload @file-uploaded="onFileUploaded" />
        </div>
      </div>

      <div class="col-sm-12 col-xl-8 gy-4">
        <div class="p-3 border bg-light ">
          <ResultsChiSquaredTest :fileID="fileID" />
        </div>

        <div>
          <p></p>
        </div>

        <div class="p-3 border bg-light ">
          <ResultsPlot :fileID="fileID" />
        </div>
      </div>

    </div>
  </div>

</template>

<script>
import UserFileUpload from './components/UserFileUpload.vue';
import ResultsChiSquaredTest from './components/ResultsChiSquaredTest.vue';
import ResultsPlot from './components/ResultsPlot.vue';

export default {
  name: 'App',
  components: {
    UserFileUpload,
    ResultsChiSquaredTest,
    ResultsPlot
  },
  data() {
    return {
      fileID: ''
    };
  },
  methods: {
    onFileUploaded(fileID) {
      this.fileID = fileID;
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>


