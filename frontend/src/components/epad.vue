<template>
  <prism-editor class="my-editor" v-model="code" :highlight="highlighter" line-numbers>
  </prism-editor>
</template>

<script>
  // import Prism Editor
  import { PrismEditor } from 'vue-prism-editor';
  import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere

  // import highlighting library (you can use any library you want just return html string)
  import { highlight, languages } from 'prismjs/components/prism-core';
  import 'prismjs/components/prism-clike';
  import 'prismjs/components/prism-javascript';
  import 'prismjs/themes/prism-tomorrow.css'; // import syntax highlighting styles

  import initCode from '!raw-loader!../assets/init_code.gs';
  import axios from 'axios';

  export default {
    components: {
      PrismEditor,
    },
    data: () => ({ code: initCode }),
    methods: {
      highlighter(code) {
        return highlight(code, languages.js); // languages.<insert language> to return html with markup
      },
      runCode() {
        const path = 'http://localhost:5000/submitCode';
        axios.post(path, {"code": this.code})
          .then((res) => {
            console.log(res);
          })
          .catch((error) => {
            console.error(error);
          });
        this.code
      },
    },
  };
</script>

<style>
  /* required class */
  .my-editor {
    /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
    background: rgb(35, 35, 35);
    color: #ccc;

    /* you must provide font-family font-size line-height. Example: */
    font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    /* padding: 5px; */
  }

  /* optional class for removing the outline */
  .prism-editor__textarea:focus {
    outline: none;
  }
  .prism-editor-wrapper{
    overflow-y: scroll;
  }
</style>
