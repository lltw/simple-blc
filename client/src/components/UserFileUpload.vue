<template>
  <h4>Submit File</h4>
  <hr>

  <form v-on:submit.prevent="submitFile">

    <div>
      <div class="mb-2">
        <label for="file">Choose a file to upload:</label>
        <input
          class="form-control mb-2"
          type="file"
          id="file"
          name="file"
          ref="file"
          accept=".txt, .csv, .tsv, .tab"
          required
          @change="handleFileUpload"
        >
      </div>

      <div class="mb-2">
        <label for="delimiter">Select one of accepted delimiters:</label>
        <select
          name="delimiter"
          id="delimiter"
          class="form-select form-select-sm"
          aria-label=".form-select-sm example"
          required
          v-model="delimiter"
        >
          <option
            selected
            disabled
          ></option>
          <option value="comma">comma (,)</option>
          <option value="semicolon">semicolon (;)</option>
          <option value="colon">colon (:)</option>
          <option value="tab">{Tab} (\t)</option>
          <option value="space">{space} ( )</option>
        </select>
      </div>

      <div class="mb-2">
        <label for="column">Is header present in your file?</label>

        <select
          name="is_header"
          id="is_header"
          class="form-select form-select-sm"
          aria-label=".form-select-sm example"
          required
          v-model="isHeader"
        >
          <option
            selected
            disabled
          ></option>
          <option value="true">yes</option>
          <option value="false">no</option>
        </select>
      </div>

      <div class="mb-2">
        <label for="column">Enter the number of column containing data to analyze: </label>
        <input
          type="number"
          name="column"
          id="column"
          min=1
          placeholder=">= 1"
          required
          v-model="columnNumber"
        >
      </div>

      <div class="mb-2">
        <input
          type="submit"
          value="Submit"
        >
      </div>

    </div>
  </form>

  <div
    class="alert alert-danger"
    role="alert"
    v-if="sumbissionError.isSubmissionError"
  >
    {{ sumbissionError.errorMessage }}
  </div>

</template>

<script>
import axios from 'axios';

export default {
  emits: ['file-uploaded'],
  data() {
    return {
      file: '',
      delimiter: null,
      isHeader: null,
      columnNumber: null,
      sumbissionError: {
        isSubmissionError: false,
        errorMessage: ''
      }
    };
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    submitFile() {
      this.sumbissionError.isSubmissionError = false;
      this.sumbissionError.errorMessage = '';

      const uploadPath = 'http://localhost:5000/upload-file';

      let formData = new FormData();

      formData.append('file', this.file);
      formData.append('delimiter', this.delimiter);
      formData.append('isHeader', this.isHeader);
      formData.append('columnNumber', this.columnNumber);

      //TODO: validate files
      axios
        .post(uploadPath, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(res => {
          console.log(res);

          let fileID = res.data.fileID;
          this.$emit('file-uploaded', fileID);
        })
        .catch(error => {
          // eslint-disable-next-line
          if (error.response) {
            // The request was made and the server responded with a status code
            // that falls out of the range of 2xx
            this.sumbissionError.isSubmissionError = true;
            if (error.response.data.message) {
              this.sumbissionError.errorMessage = error.response.data.message;
            } else {
              this.sumbissionError.errorMessage = error;
            }
          } else if (error.request) {
            // The request was made but no response was received
            // `error.request` is an instance of XMLHttpRequest in the browser and an instance of
            // http.ClientRequest in node.js
            console.log(error.request);
          } else {
            // Something happened in setting up the request that triggered an Error
            console.log('Error', error.message);
          }
          console.log(error.config);
        });
    }
  }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>



