<template>
  <h4>Chi-squared Goodness of Fit Test</h4>
  <hr>
  <p>Chi-squared statistic: {{ chiSquaredStatistic }}</p>
  <p>p-value: {{ chiSquaredPvalue }}</p>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      chiSquaredStatistic: '',
      chiSquaredPvalue: ''
    };
  },
  created() {
    const statsPath = 'http://localhost:5000/test-results-stats';

    axios
      .get(statsPath)
      .then(res => {
        this.chiSquaredStatistic = res.data.chiSquaredStatistic;
        this.chiSquaredPvalue = res.data.chiSquaredPvalue;
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
  }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>


