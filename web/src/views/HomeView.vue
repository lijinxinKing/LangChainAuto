<script setup lang="ts">
import { ref } from "vue";

const calendarValue = ref(new Date());
</script>

<template>
  <main class="home-view">
    <div class="calendar-box">
      <el-calendar v-model="calendarValue" />
    </div>
  </main>
</template>

<style lang="scss" scoped>
.home-view {
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;

  .calendar-box {
    .el-calendar {
      width: 600px;
      border-radius: 10px;
    }
  }
}
</style>
