<template>
  <h2>Chi-squared Goodness of Fit Test</h2>
  <hr>
  <p>Chi-squared statistic: {{ chiSquaredStatistic }}</p>
  <p>p-value: {{ chiSquaredPvalue }}</p>

  <h2>Distribution of first significant digits</h2>
  <hr>
  <img
    class="img-fluid"
    :src="plotUrl"
    alt="test plot"
  />
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      chiSquaredStatistic: '',
      chiSquaredPvalue: '',
      plotUrl: ''
    };
  },
  created() {
    const statsPath = 'http://localhost:5000/test-results-stats';
    const plotPath = 'http://localhost:5000/test-results-plot';

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

    axios
      .get(plotPath, { responseType: 'blob' })
      .then(res => {
        this.plotUrl = window.URL.createObjectURL(new Blob([res.data]));
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>


