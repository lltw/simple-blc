<template>
  <h4>Chi-squared Goodness of Fit Test</h4>
  <hr>
  <p v-if="fileID">Chi-squared statistic: {{ chiSquaredStatistic }}</p>
  <p v-if="fileID">p-value: {{ chiSquaredPvalue }}</p>

</template>

<script>
import axios from 'axios';

export default {
  props: {
    fileID: String
  },
  data() {
    return {
      chiSquaredStatistic: '',
      chiSquaredPvalue: ''
    };
  },
  watch: {
    fileID: function() {
      const statsPath = 'http://localhost:5000/chi-squared-results';

      if (this.fileID) {
        axios
          .get(statsPath, {
            params: {
              fileID: this.fileID
            }
          })
          .then(res => {
            this.chiSquaredStatistic = res.data.chiSquaredStatistic;
            this.chiSquaredPvalue = res.data.chiSquaredPvalue;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    }
  }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>


