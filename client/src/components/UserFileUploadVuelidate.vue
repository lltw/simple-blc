<template>
  <h4>Submit File</h4>
  <hr>

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
        @change="handleFileUpload"
      >
    </div>

    <div class="mb-2">
      <label
        for="delimiter"
        class="form-label"
      >Select a delimiter:</label>
      <select
        name="delimiter"
        id="delimiter"
        class="form-select form-select-sm"
        aria-label=".form-select-sm example"
        v-model="delimiter"
        required
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
      <div class="invalid-feedback">
        Please select a delimiter.
      </div>
    </div>

    <div class="mb-2">
      <label for="column">Is header present in your file?</label>

      <select
        name="is_header"
        id="is_header"
        class="form-select form-select-sm"
        aria-label=".form-select-sm example"
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
        @click="submitFile"
      >
    </div>

  </div>

</template>

<script>
import useVuelidate from '@vuelidate/core';
import { required } from '@vuelidate/validators';
import axios from 'axios';

export default {
  setup() {
    return {
      v$: useVuelidate()
    };
  },
  data() {
    return {
      file: '',
      delimiter: '',
      columnNumber: null,
      isHeader: null
    };
  },
  validations() {
    return {
      file: { required }, //, fileSizevalidation, filenameLengthValidation },
      delimiter: { required },
      columnNumber: { required },
      isHeader: { required }
    };
  },
  methods: {
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    validate() {
      //console.log(this.v$);
      //if (!this.v$.$error) {
      //  // if ANY fail validation
      //  console.log('validation ok');
      //} else {
      //  console.log('validation not ok');
      //
    },
    submitFile() {
      this.v$.$validate(); // checks all inputs

      const uploadPath = 'http://localhost:5000/test-upload';

      let formData = new FormData();

      formData.append('file', this.file);
      formData.append('columnNumber', this.columnNumber - 1);
      formData.append('delimiter', this.delimiter);
      formData.append('isHeader', this.isHeader);

      //TODO: validate files
      axios
        .post(uploadPath, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(res => {
          console.log(res);
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  }
};
</script>



<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>



