<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "PillFilter",
  props: {
    textContent: {
      type: String,
      required: true
    },
    isActivated: {
      type: Boolean,
      required: false
    }
  }
})
</script>

<template>
  <div :class="isActivated ? 'pill active' : 'pill'">
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
  padding: 0.5rem;
  transition: 0.3s ease-in-out;
  cursor: pointer;
}

.active {
  background-color: #007AFF;
  color: white;
}

.pill:hover {
  transform: scale(1.1);
}

</style>