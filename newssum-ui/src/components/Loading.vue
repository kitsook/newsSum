<template>
  <div class="d-flex justify-content-center">
    <div class="p-1 spinner-border spinner-border-sm m-2" role="status" aria-hidden="true">
      <span class="sr-only"></span>
    </div>
    <div class="p-1">Loading...</div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Loading extends Vue {
}
</script>