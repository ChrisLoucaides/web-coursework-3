<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "Pill",
  props: {
    textContent: {
      type: String,
      required: true
    },
    leftIcon: {
      type: String,
      required: false
    }
  }
})
</script>

<template>
  <div class="pill">
      <i v-if="leftIcon" :class="leftIcon"></i>
      <span>{{textContent}}</span>
  </div>
</template>

<style scoped lang="scss">
.pill {
  display: flex;
  flex-direction: row;
  background-color: #dddddd;
  border-radius: 1rem;
  box-shadow: rgba(100, 100, 111, 0.2) 0 7px 29px 0;
  justify-content: center;
  align-items: center;
  min-width: 5rem;
  width: fit-content;
  gap: 0.5rem;
}
</style>