<template>
  <h4>Distribution of first significant digits</h4>
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
      plotUrl: ''
    };
  },
  created() {
    const plotPath = 'http://localhost:5000/test-results-plot';

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
</style>


