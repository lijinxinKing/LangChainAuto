<script setup lang="ts">
import PageHeader from "./components/PageHeader.vue";
</script>

<template>
  <section class="page-layout">
    <header class="page-layout-header">
      <div class="page-layout-row">
        <PageHeader />
      </div>
    </header>
    <main class="page-layout-content">
      <section class="starter-content">
        <div class="page-layout-row">
          <RouterView />
        </div>
      </section>
    </main>
  </section>
</template>

<style lang="scss" scoped>
.page-layout {
  background: #eee;
  display: flex;
  flex-direction: column;

  .page-layout-row {
    width: 1440px;
    display: flex;
    flex-direction: column;
  }

  .page-layout-header {
    display: flex;
    justify-content: center;
    min-width: 760px;
    height: 66px;
    background: #fff;
    border-bottom: 1px solid #eee;
    box-shadow: 0 2px 8px 0 rgba(2, 24, 42, 0.1);
  }

  .page-layout-content {
    flex: 1;
  }

  .starter-content {
    height: calc(100vh - 66px); // 66px是 page-layout-header 的高度
    display: flex;
    justify-content: center;
    overflow-y: scroll;

    &::-webkit-scrollbar {
      width: 8px;
      height: 8px;
    }

    &::-webkit-scrollbar-thumb {
      border-radius: 6px;
      border: 2px solid transparent;
      background-clip: content-box;
      background-color: rgba(0, 0, 0, 10%);
    }
  }
}
</style>
