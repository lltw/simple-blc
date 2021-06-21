<template>
  <h4>Distribution of first significant digits</h4>
  <hr>
  <img
    v-if="fileID"
    class="img-fluid"
    :src="plotUrl"
    alt="test plot"
  />
</template>

<script>
import axios from 'axios';

export default {
  props: {
    fileID: String
  },
  data() {
    return {
      plotUrl: ''
    };
  },
  watch: {
    fileID: function() {
      const plotPath = 'http://localhost:5000/plot';

      if (this.fileID) {
        axios
          .get(plotPath, {
            responseType: 'blob',
            params: {
              fileID: this.fileID
            }
          })
          .then(res => {
            this.plotUrl = window.URL.createObjectURL(new Blob([res.data]));
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


