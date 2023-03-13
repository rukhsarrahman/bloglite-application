<template>
  <div>
    <p>{{ msg["msg"] }}</p>
  </div>
</template>

<script>
import CustomFetch from './CustomFetch';
/* eslint-disable */
export default {
  name: 'Ping',
  data() {
    return {
      msg: "HW",
    }
    },
    mounted() {
      this.getUser();
    },
    methods: {
      getUser() {
        CustomFetch('http://localhost:8080/test', {
          method: 'GET',
          mode: 'cors',
        })
        .then((res) => {
          this.msg = res;
        })
        .catch((error) => {
          console.error(error);
        });
      },
    } 
  }
</script>
